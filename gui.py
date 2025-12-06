"""
Interface Gráfica para Controle do Inversor de Frequência SENAI
Protocolo ModBus TCP
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from main import InversorControl


class InversorGUI:
    """Interface gráfica para controle do inversor"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Controle do Inversor de Frequência SENAI")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variáveis
        self.inversor = None
        self.conectado = False
        self.atualizando = False
        
        # Cores
        self.cor_verde = "#4CAF50"
        self.cor_vermelho = "#F44336"
        self.cor_azul = "#2196F3"
        self.cor_cinza = "#9E9E9E"
        
        self.criar_interface()
        
    def criar_interface(self):
        """Cria todos os componentes da interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # ========== SEÇÃO DE CONEXÃO ==========
        conexao_frame = ttk.LabelFrame(main_frame, text="Conexão", padding="10")
        conexao_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        conexao_frame.columnconfigure(1, weight=1)
        
        ttk.Label(conexao_frame, text="IP do Inversor:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(conexao_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.ip_entry.insert(0, "192.168.1.100")
        
        self.btn_conectar = ttk.Button(conexao_frame, text="Conectar", command=self.conectar)
        self.btn_conectar.grid(row=0, column=2, padx=5, pady=5)
        
        self.status_label = ttk.Label(conexao_frame, text="Desconectado", foreground="red")
        self.status_label.grid(row=0, column=3, padx=10, pady=5)
        
        # ========== SEÇÃO DE CONTROLE DO MOTOR ==========
        controle_frame = ttk.LabelFrame(main_frame, text="Controle do Motor", padding="10")
        controle_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Botões de controle
        btn_frame = ttk.Frame(controle_frame)
        btn_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.btn_ligar = ttk.Button(btn_frame, text="▶ Ligar Motor", command=self.ligar_motor, state="disabled")
        self.btn_ligar.grid(row=0, column=0, padx=5)
        
        self.btn_parar = ttk.Button(btn_frame, text="⏸ Parar Motor", command=self.parar_motor, state="disabled")
        self.btn_parar.grid(row=0, column=1, padx=5)
        
        self.btn_config_padrao = ttk.Button(btn_frame, text="⚙ Configuração Padrão", command=self.configuracao_padrao, state="disabled")
        self.btn_config_padrao.grid(row=0, column=2, padx=5)
        
        # Estado do motor
        estado_frame = ttk.Frame(controle_frame)
        estado_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(estado_frame, text="Estado:").grid(row=0, column=0, padx=5)
        self.estado_motor_label = ttk.Label(estado_frame, text="---", font=("Arial", 12, "bold"))
        self.estado_motor_label.grid(row=0, column=1, padx=5)
        
        # ========== SEÇÃO DE VELOCIDADE ==========
        velocidade_frame = ttk.LabelFrame(main_frame, text="Velocidade", padding="10")
        velocidade_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        velocidade_frame.columnconfigure(1, weight=1)
        
        ttk.Label(velocidade_frame, text="Velocidade (Hz):").grid(row=0, column=0, padx=5, pady=5)
        self.velocidade_var = tk.StringVar(value="30")
        velocidade_spin = ttk.Spinbox(velocidade_frame, from_=1, to=60, textvariable=self.velocidade_var, width=10)
        velocidade_spin.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.btn_definir_velocidade = ttk.Button(velocidade_frame, text="Definir Velocidade", command=self.definir_velocidade, state="disabled")
        self.btn_definir_velocidade.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(velocidade_frame, text="Velocidade Atual:").grid(row=1, column=0, padx=5, pady=5)
        self.velocidade_atual_label = ttk.Label(velocidade_frame, text="--- Hz", font=("Arial", 11))
        self.velocidade_atual_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # ========== SEÇÃO DE SENTIDO DE GIRO ==========
        sentido_frame = ttk.LabelFrame(main_frame, text="Sentido de Giro", padding="10")
        sentido_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.sentido_var = tk.StringVar(value="horario")
        ttk.Radiobutton(sentido_frame, text="Horário", variable=self.sentido_var, value="horario", command=self.definir_sentido).grid(row=0, column=0, padx=10, pady=5)
        ttk.Radiobutton(sentido_frame, text="Anti-horário", variable=self.sentido_var, value="anti_horario", command=self.definir_sentido).grid(row=0, column=1, padx=10, pady=5)
        
        # ========== SEÇÃO DE MONITORAMENTO ==========
        monitoramento_frame = ttk.LabelFrame(main_frame, text="Monitoramento", padding="10")
        monitoramento_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        monitoramento_frame.columnconfigure(0, weight=1)
        monitoramento_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Coluna esquerda
        left_col = ttk.Frame(monitoramento_frame)
        left_col.grid(row=0, column=0, padx=10, sticky=(tk.W, tk.E, tk.N))
        
        ttk.Label(left_col, text="Temperatura:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.temp_label = ttk.Label(left_col, text="--- °C", font=("Arial", 12, "bold"))
        self.temp_label.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(left_col, text="Corrente:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.corrente_label = ttk.Label(left_col, text="--- A", font=("Arial", 12, "bold"))
        self.corrente_label.grid(row=1, column=1, padx=5, pady=5)
        
        # Coluna direita
        right_col = ttk.Frame(monitoramento_frame)
        right_col.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E, tk.N))
        
        ttk.Label(right_col, text="Tensão:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.tensao_label = ttk.Label(right_col, text="--- V", font=("Arial", 12, "bold"))
        self.tensao_label.grid(row=0, column=1, padx=5, pady=5)
        
        # Botão de atualização automática
        atualizar_frame = ttk.Frame(monitoramento_frame)
        atualizar_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.btn_atualizar = ttk.Button(atualizar_frame, text="🔄 Atualizar Dados", command=self.atualizar_dados)
        self.btn_atualizar.grid(row=0, column=0, padx=5)
        
        self.btn_auto_atualizar = ttk.Button(atualizar_frame, text="⏸ Parar Atualização Automática", command=self.toggle_auto_atualizar)
        self.btn_auto_atualizar.grid(row=0, column=1, padx=5)
        
        # ========== SEÇÃO DE LOG ==========
        log_frame = ttk.LabelFrame(main_frame, text="Log de Operações", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=70, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para cores no log
        self.log_text.tag_config("sucesso", foreground="green")
        self.log_text.tag_config("erro", foreground="red")
        self.log_text.tag_config("info", foreground="blue")
        
    def log(self, mensagem, tipo="info"):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, f"{mensagem}\n", tipo)
        self.log_text.see(tk.END)
        
    def habilitar_controles(self, habilitar):
        """Habilita ou desabilita os controles"""
        estado = "normal" if habilitar else "disabled"
        self.btn_ligar.config(state=estado)
        self.btn_parar.config(state=estado)
        self.btn_definir_velocidade.config(state=estado)
        self.btn_config_padrao.config(state=estado)
        self.btn_atualizar.config(state=estado)
        
    def conectar(self):
        """Conecta ou desconecta do inversor"""
        if not self.conectado:
            ip = self.ip_entry.get().strip()
            if not ip:
                messagebox.showerror("Erro", "Digite o endereço IP do inversor")
                return
            
            try:
                self.inversor = InversorControl(ip)
                if self.inversor.conectar():
                    self.conectado = True
                    self.btn_conectar.config(text="Desconectar")
                    self.status_label.config(text="Conectado", foreground="green")
                    self.ip_entry.config(state="disabled")
                    self.habilitar_controles(True)
                    self.log(f"Conectado ao inversor em {ip}:502", "sucesso")
                    self.definir_sentido()  # Aplica sentido padrão
                else:
                    messagebox.showerror("Erro", "Não foi possível conectar ao inversor")
                    self.log("Erro ao conectar ao inversor", "erro")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao conectar: {str(e)}")
                self.log(f"Erro: {str(e)}", "erro")
        else:
            if self.inversor:
                self.inversor.desconectar()
            self.conectado = False
            self.btn_conectar.config(text="Conectar")
            self.status_label.config(text="Desconectado", foreground="red")
            self.ip_entry.config(state="normal")
            self.habilitar_controles(False)
            self.log("Desconectado do inversor", "info")
            self.atualizando = False
            self.btn_auto_atualizar.config(text="▶ Iniciar Atualização Automática")
            
    def ligar_motor(self):
        """Liga o motor"""
        if self.inversor:
            if self.inversor.ligar_motor():
                self.log("Motor ligado com sucesso", "sucesso")
                self.atualizar_dados()
            else:
                self.log("Erro ao ligar o motor", "erro")
                messagebox.showerror("Erro", "Não foi possível ligar o motor")
                
    def parar_motor(self):
        """Para o motor"""
        if self.inversor:
            if self.inversor.parar_motor():
                self.log("Motor parado com sucesso", "sucesso")
                self.atualizar_dados()
            else:
                self.log("Erro ao parar o motor", "erro")
                messagebox.showerror("Erro", "Não foi possível parar o motor")
                
    def definir_velocidade(self):
        """Define a velocidade do motor"""
        if self.inversor:
            try:
                velocidade = float(self.velocidade_var.get())
                if self.inversor.definir_velocidade(velocidade):
                    self.log(f"Velocidade definida: {velocidade} Hz", "sucesso")
                    self.atualizar_dados()
                else:
                    self.log("Erro ao definir velocidade", "erro")
                    messagebox.showerror("Erro", "Velocidade deve estar entre 1 e 60 Hz")
            except ValueError:
                messagebox.showerror("Erro", "Digite um número válido")
                
    def definir_sentido(self):
        """Define o sentido de giro"""
        if self.inversor and self.conectado:
            if self.sentido_var.get() == "horario":
                if self.inversor.definir_sentido_horario():
                    self.log("Sentido definido: Horário", "info")
            else:
                if self.inversor.definir_sentido_anti_horario():
                    self.log("Sentido definido: Anti-horário", "info")
                    
    def configuracao_padrao(self):
        """Aplica configuração padrão"""
        if self.inversor:
            if self.inversor.configuracao_padrao():
                self.velocidade_var.set("30")
                self.sentido_var.set("horario")
                self.log("Configuração padrão aplicada: 30Hz, Horário", "sucesso")
                self.atualizar_dados()
                
    def atualizar_dados(self):
        """Atualiza os dados de monitoramento"""
        if not self.inversor or not self.conectado:
            return
            
        try:
            # Estado do motor
            estado = self.inversor.verificar_estado_motor()
            if estado is not None:
                status_text = "Girando" if estado else "Parado"
                cor = self.cor_verde if estado else self.cor_cinza
                self.estado_motor_label.config(text=status_text, foreground=cor)
            
            # Velocidade atual
            velocidade = self.inversor.verificar_velocidade()
            if velocidade is not None:
                self.velocidade_atual_label.config(text=f"{velocidade} Hz")
            
            # Temperatura
            temp = self.inversor.verificar_temperatura()
            if temp is not None:
                self.temp_label.config(text=f"{temp} °C")
            
            # Corrente
            corrente = self.inversor.verificar_corrente()
            if corrente is not None:
                self.corrente_label.config(text=f"{corrente} A")
            
            # Tensão
            tensao = self.inversor.verificar_tensao()
            if tensao is not None:
                self.tensao_label.config(text=f"{tensao} V")
                
        except Exception as e:
            self.log(f"Erro ao atualizar dados: {str(e)}", "erro")
            
    def toggle_auto_atualizar(self):
        """Alterna atualização automática"""
        if not self.conectado:
            return
            
        self.atualizando = not self.atualizando
        
        if self.atualizando:
            self.btn_auto_atualizar.config(text="⏸ Parar Atualização Automática")
            self.auto_atualizar_loop()
        else:
            self.btn_auto_atualizar.config(text="▶ Iniciar Atualização Automática")
            
    def auto_atualizar_loop(self):
        """Loop de atualização automática"""
        if self.atualizando and self.conectado:
            self.atualizar_dados()
            self.root.after(2000, self.auto_atualizar_loop)  # Atualiza a cada 2 segundos
            
    def on_closing(self):
        """Função chamada ao fechar a janela"""
        if self.conectado and self.inversor:
            self.inversor.desconectar()
        self.root.destroy()


def main():
    """Função principal"""
    root = tk.Tk()
    app = InversorGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

