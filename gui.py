"""
Interface Gráfica Profissional para Controle do Inversor de Frequência SENAI
Protocolo ModBus TCP
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from main import InversorControl


class InversorGUI:
    """Interface gráfica profissional para controle do inversor"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SENAI - Controle de Inversor de Frequência")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Variáveis
        self.inversor = None
        self.conectado = False
        self.atualizando = False
        
        # Cores profissionais
        self.cor_primaria = "#1E88E5"      # Azul profissional
        self.cor_secundaria = "#43A047"    # Verde sucesso
        self.cor_perigo = "#E53935"        # Vermelho erro
        self.cor_aviso = "#FB8C00"         # Laranja aviso
        self.cor_fundo = "#F5F5F5"         # Cinza claro
        self.cor_texto = "#212121"         # Cinza escuro
        self.cor_borda = "#E0E0E0"         # Cinza borda
        self.cor_offline = "#9E9E9E"       # Cinza offline
        
        # Configurar fundo
        self.root.configure(bg=self.cor_fundo)
        
        self.criar_interface()
        
    def configurar_estilo(self):
        """Configura o estilo visual da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores dos botões
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
    def criar_interface(self):
        """Cria todos os componentes da interface"""
        
        # Container principal com padding
        main_container = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== CABEÇALHO ==========
        header_frame = tk.Frame(main_container, bg=self.cor_primaria, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="SENAI - Sistema de Controle de Inversor",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.cor_primaria,
                              fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        subtitle_label = tk.Label(header_frame,
                                text="Protocolo ModBus TCP",
                                font=('Segoe UI', 10),
                                bg=self.cor_primaria,
                                fg='white')
        subtitle_label.pack(side=tk.LEFT, padx=(0, 20), pady=20)
        
        # ========== SEÇÃO DE CONEXÃO ==========
        conexao_card = self.criar_card(main_container, "Conexão com o Inversor")
        conexao_frame = conexao_card['frame']
        
        # Grid para conexão
        conexao_frame.columnconfigure(1, weight=1)
        
        # IP Input
        ip_label = tk.Label(conexao_frame, text="Endereço IP:", 
                           font=('Segoe UI', 10, 'bold'),
                           bg='white', fg=self.cor_texto)
        ip_label.grid(row=0, column=0, padx=15, pady=15, sticky=tk.W)
        
        self.ip_entry = ttk.Entry(conexao_frame, font=('Segoe UI', 11), width=20)
        self.ip_entry.grid(row=0, column=1, padx=15, pady=15, sticky=(tk.W, tk.E))
        self.ip_entry.insert(0, "192.168.1.100")
        
        self.btn_conectar = tk.Button(conexao_frame,
                                     text="🔌 Conectar",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg=self.cor_primaria,
                                     fg='white',
                                     activebackground="#1565C0",
                                     activeforeground='white',
                                     relief=tk.FLAT,
                                     padx=20,
                                     pady=10,
                                     cursor='hand2',
                                     command=self.conectar)
        self.btn_conectar.grid(row=0, column=2, padx=15, pady=15)
        
        # Status indicator
        status_container = tk.Frame(conexao_frame, bg='white')
        status_container.grid(row=0, column=3, padx=15, pady=15)
        
        self.status_indicator = tk.Label(status_container,
                                        text="●",
                                        font=('Segoe UI', 20),
                                        bg='white',
                                        fg=self.cor_offline)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(status_container,
                                    text="Desconectado",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg='white',
                                    fg=self.cor_offline)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # ========== CONTROLE DO MOTOR ==========
        controle_card = self.criar_card(main_container, "Controle do Motor")
        controle_frame = controle_card['frame']
        
        # Botões de controle em linha
        btn_container = tk.Frame(controle_frame, bg='white')
        btn_container.pack(pady=20)
        
        self.btn_ligar = tk.Button(btn_container,
                                   text="▶ INICIAR MOTOR",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.cor_secundaria,
                                   fg='white',
                                   activebackground="#2E7D32",
                                   activeforeground='white',
                                   relief=tk.FLAT,
                                   padx=25,
                                   pady=15,
                                   cursor='hand2',
                                   state=tk.DISABLED,
                                   command=self.ligar_motor)
        self.btn_ligar.pack(side=tk.LEFT, padx=10)
        
        self.btn_parar = tk.Button(btn_container,
                                   text="⏸ PARAR MOTOR",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.cor_perigo,
                                   fg='white',
                                   activebackground="#C62828",
                                   activeforeground='white',
                                   relief=tk.FLAT,
                                   padx=25,
                                   pady=15,
                                   cursor='hand2',
                                   state=tk.DISABLED,
                                   command=self.parar_motor)
        self.btn_parar.pack(side=tk.LEFT, padx=10)
        
        self.btn_config_padrao = tk.Button(btn_container,
                                           text="⚙ CONFIGURAÇÃO PADRÃO",
                                           font=('Segoe UI', 11, 'bold'),
                                           bg=self.cor_aviso,
                                           fg='white',
                                           activebackground="#E65100",
                                           activeforeground='white',
                                           relief=tk.FLAT,
                                           padx=25,
                                           pady=15,
                                           cursor='hand2',
                                           state=tk.DISABLED,
                                           command=self.configuracao_padrao)
        self.btn_config_padrao.pack(side=tk.LEFT, padx=10)
        
        # Estado do motor
        estado_container = tk.Frame(controle_frame, bg='white')
        estado_container.pack(pady=20)
        
        estado_title = tk.Label(estado_container,
                               text="Status do Motor:",
                               font=('Segoe UI', 11),
                               bg='white',
                               fg=self.cor_texto)
        estado_title.pack(side=tk.LEFT, padx=10)
        
        self.estado_motor_label = tk.Label(estado_container,
                                          text="OFFLINE",
                                          font=('Segoe UI', 14, 'bold'),
                                          bg='white',
                                          fg=self.cor_offline)
        self.estado_motor_label.pack(side=tk.LEFT, padx=10)
        
        # ========== VELOCIDADE E SENTIDO ==========
        config_card = self.criar_card(main_container, "Configuração de Operação")
        config_frame = config_card['frame']
        
        # Grid para configuração
        config_frame.columnconfigure(0, weight=1)
        config_frame.columnconfigure(1, weight=1)
        
        # Velocidade
        velocidade_container = tk.Frame(config_frame, bg='white')
        velocidade_container.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))
        
        vel_label = tk.Label(velocidade_container,
                            text="Velocidade (Hz)",
                            font=('Segoe UI', 10, 'bold'),
                            bg='white',
                            fg=self.cor_texto)
        vel_label.pack(anchor=tk.W, pady=(0, 10))
        
        vel_input_frame = tk.Frame(velocidade_container, bg='white')
        vel_input_frame.pack(fill=tk.X)
        
        self.velocidade_var = tk.StringVar(value="30")
        velocidade_spin = ttk.Spinbox(vel_input_frame,
                                     from_=1,
                                     to=60,
                                     textvariable=self.velocidade_var,
                                     font=('Segoe UI', 12),
                                     width=10)
        velocidade_spin.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_definir_velocidade = tk.Button(vel_input_frame,
                                                text="Aplicar",
                                                font=('Segoe UI', 9, 'bold'),
                                                bg=self.cor_primaria,
                                                fg='white',
                                                activebackground="#1565C0",
                                                activeforeground='white',
                                                relief=tk.FLAT,
                                                padx=15,
                                                pady=8,
                                                cursor='hand2',
                                                state=tk.DISABLED,
                                                command=self.definir_velocidade)
        self.btn_definir_velocidade.pack(side=tk.LEFT)
        
        vel_atual_label = tk.Label(velocidade_container,
                                   text="Velocidade Atual:",
                                   font=('Segoe UI', 9),
                                   bg='white',
                                   fg=self.cor_texto)
        vel_atual_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.velocidade_atual_label = tk.Label(velocidade_container,
                                               text="--- Hz",
                                               font=('Segoe UI', 16, 'bold'),
                                               bg='white',
                                               fg=self.cor_primaria)
        self.velocidade_atual_label.pack(anchor=tk.W)
        
        # Sentido de giro
        sentido_container = tk.Frame(config_frame, bg='white')
        sentido_container.grid(row=0, column=1, padx=20, pady=20, sticky=(tk.W, tk.E))
        
        sentido_label = tk.Label(sentido_container,
                                text="Sentido de Giro",
                                font=('Segoe UI', 10, 'bold'),
                                bg='white',
                                fg=self.cor_texto)
        sentido_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.sentido_var = tk.StringVar(value="horario")
        
        sentido_frame = tk.Frame(sentido_container, bg='white')
        sentido_frame.pack(fill=tk.X)
        
        rb_horario = tk.Radiobutton(sentido_frame,
                                    text="Horário ↻",
                                    variable=self.sentido_var,
                                    value="horario",
                                    font=('Segoe UI', 11),
                                    bg='white',
                                    fg=self.cor_texto,
                                    activebackground='white',
                                    activeforeground=self.cor_primaria,
                                    selectcolor='white',
                                    command=self.definir_sentido,
                                    cursor='hand2')
        rb_horario.pack(side=tk.LEFT, padx=10)
        
        rb_anti_horario = tk.Radiobutton(sentido_frame,
                                        text="Anti-horário ↺",
                                        variable=self.sentido_var,
                                        value="anti_horario",
                                        font=('Segoe UI', 11),
                                        bg='white',
                                        fg=self.cor_texto,
                                        activebackground='white',
                                        activeforeground=self.cor_primaria,
                                        selectcolor='white',
                                        command=self.definir_sentido,
                                        cursor='hand2')
        rb_anti_horario.pack(side=tk.LEFT, padx=10)
        
        # ========== MONITORAMENTO ==========
        monitor_card = self.criar_card(main_container, "Monitoramento em Tempo Real")
        monitor_frame = monitor_card['frame']
        
        # Grid para monitoramento
        monitor_frame.columnconfigure(0, weight=1)
        monitor_frame.columnconfigure(1, weight=1)
        monitor_frame.columnconfigure(2, weight=1)
        
        # Card de Temperatura
        temp_card = self.criar_metric_card(monitor_frame, "🌡 Temperatura", "---", "°C", 0, 0)
        self.temp_label = temp_card['value']
        
        # Card de Corrente
        corrente_card = self.criar_metric_card(monitor_frame, "⚡ Corrente", "---", "A", 0, 1)
        self.corrente_label = corrente_card['value']
        
        # Card de Tensão
        tensao_card = self.criar_metric_card(monitor_frame, "🔌 Tensão", "---", "V", 0, 2)
        self.tensao_label = tensao_card['value']
        
        # Botões de atualização
        atualizar_container = tk.Frame(monitor_frame, bg='white')
        atualizar_container.grid(row=1, column=0, columnspan=3, pady=20)
        
        self.btn_atualizar = tk.Button(atualizar_container,
                                      text="🔄 Atualizar Agora",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg=self.cor_primaria,
                                      fg='white',
                                      activebackground="#1565C0",
                                      activeforeground='white',
                                      relief=tk.FLAT,
                                      padx=20,
                                      pady=10,
                                      cursor='hand2',
                                      command=self.atualizar_dados)
        self.btn_atualizar.pack(side=tk.LEFT, padx=5)
        
        self.btn_auto_atualizar = tk.Button(atualizar_container,
                                            text="▶ Iniciar Monitoramento Automático",
                                            font=('Segoe UI', 10, 'bold'),
                                            bg=self.cor_secundaria,
                                            fg='white',
                                            activebackground="#2E7D32",
                                            activeforeground='white',
                                            relief=tk.FLAT,
                                            padx=20,
                                            pady=10,
                                            cursor='hand2',
                                            command=self.toggle_auto_atualizar)
        self.btn_auto_atualizar.pack(side=tk.LEFT, padx=5)
        
        # ========== LOG ==========
        log_card = self.criar_card(main_container, "Log de Operações")
        log_frame = log_card['frame']
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  height=8,
                                                  font=('Consolas', 9),
                                                  bg='#FAFAFA',
                                                  fg=self.cor_texto,
                                                  relief=tk.FLAT,
                                                  borderwidth=1,
                                                  highlightthickness=1,
                                                  highlightbackground=self.cor_borda)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configurar tags para cores no log
        self.log_text.tag_config("sucesso", foreground="#2E7D32", font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("erro", foreground="#C62828", font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("info", foreground="#1565C0", font=('Consolas', 9))
        self.log_text.tag_config("timestamp", foreground="#757575", font=('Consolas', 8))
        
        # Mensagem inicial
        self.log("Sistema inicializado. Aguardando conexão...", "info")
        
    def criar_card(self, parent, title):
        """Cria um card com título"""
        card_frame = tk.Frame(parent, bg='white', relief=tk.FLAT, borderwidth=1)
        card_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Título do card
        title_frame = tk.Frame(card_frame, bg=self.cor_primaria, height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame,
                              text=title,
                              font=('Segoe UI', 12, 'bold'),
                              bg=self.cor_primaria,
                              fg='white')
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Frame de conteúdo
        content_frame = tk.Frame(card_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        return {'frame': content_frame, 'card': card_frame}
        
    def criar_metric_card(self, parent, title, value, unit, row, col):
        """Cria um card de métrica"""
        metric_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=1)
        metric_frame.grid(row=row, column=col, padx=15, pady=15, sticky=(tk.W, tk.E, tk.N))
        metric_frame.columnconfigure(0, weight=1)
        
        title_label = tk.Label(metric_frame,
                              text=title,
                              font=('Segoe UI', 10),
                              bg='white',
                              fg=self.cor_texto)
        title_label.pack(pady=(15, 5))
        
        value_label = tk.Label(metric_frame,
                              text=value,
                              font=('Segoe UI', 24, 'bold'),
                              bg='white',
                              fg=self.cor_primaria)
        value_label.pack()
        
        unit_label = tk.Label(metric_frame,
                             text=unit,
                             font=('Segoe UI', 10),
                             bg='white',
                             fg=self.cor_texto)
        unit_label.pack(pady=(0, 15))
        
        return {'value': value_label, 'unit': unit_label}
        
    def log(self, mensagem, tipo="info"):
        """Adiciona mensagem ao log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{mensagem}\n", tipo)
        self.log_text.see(tk.END)
        
    def habilitar_controles(self, habilitar):
        """Habilita ou desabilita os controles"""
        estado = tk.NORMAL if habilitar else tk.DISABLED
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
                messagebox.showerror("Erro de Conexão", "Por favor, digite o endereço IP do inversor")
                return
            
            try:
                self.inversor = InversorControl(ip)
                if self.inversor.conectar():
                    self.conectado = True
                    self.btn_conectar.config(text="🔌 Desconectar", bg=self.cor_perigo, activebackground="#C62828")
                    self.status_indicator.config(fg=self.cor_secundaria)
                    self.status_label.config(text="Conectado", fg=self.cor_secundaria)
                    self.ip_entry.config(state=tk.DISABLED)
                    self.habilitar_controles(True)
                    self.log(f"Conectado ao inversor em {ip}:502", "sucesso")
                    self.definir_sentido()
                    self.atualizar_dados()
                else:
                    messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao inversor.\nVerifique o endereço IP e a conexão de rede.")
                    self.log("Falha na conexão com o inversor", "erro")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao conectar: {str(e)}")
                self.log(f"Erro: {str(e)}", "erro")
        else:
            if self.inversor:
                self.inversor.desconectar()
            self.conectado = False
            self.btn_conectar.config(text="🔌 Conectar", bg=self.cor_primaria, activebackground="#1565C0")
            self.status_indicator.config(fg=self.cor_offline)
            self.status_label.config(text="Desconectado", fg=self.cor_offline)
            self.ip_entry.config(state=tk.NORMAL)
            self.habilitar_controles(False)
            self.estado_motor_label.config(text="OFFLINE", fg=self.cor_offline)
            self.log("Desconectado do inversor", "info")
            self.atualizando = False
            self.btn_auto_atualizar.config(text="▶ Iniciar Monitoramento Automático", bg=self.cor_secundaria, activebackground="#2E7D32")
            
    def ligar_motor(self):
        """Liga o motor"""
        if self.inversor:
            if self.inversor.ligar_motor():
                self.log("Motor iniciado com sucesso", "sucesso")
                self.atualizar_dados()
            else:
                self.log("Falha ao iniciar o motor", "erro")
                messagebox.showerror("Erro", "Não foi possível iniciar o motor")
                
    def parar_motor(self):
        """Para o motor"""
        if self.inversor:
            if self.inversor.parar_motor():
                self.log("Motor parado com sucesso", "sucesso")
                self.atualizar_dados()
            else:
                self.log("Falha ao parar o motor", "erro")
                messagebox.showerror("Erro", "Não foi possível parar o motor")
                
    def definir_velocidade(self):
        """Define a velocidade do motor"""
        if self.inversor:
            try:
                velocidade = float(self.velocidade_var.get())
                if self.inversor.definir_velocidade(velocidade):
                    self.log(f"Velocidade configurada: {velocidade} Hz", "sucesso")
                    self.atualizar_dados()
                else:
                    self.log("Velocidade fora do intervalo permitido (1-60 Hz)", "erro")
                    messagebox.showerror("Erro", "A velocidade deve estar entre 1 e 60 Hz")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, digite um número válido")
                
    def definir_sentido(self):
        """Define o sentido de giro"""
        if self.inversor and self.conectado:
            if self.sentido_var.get() == "horario":
                if self.inversor.definir_sentido_horario():
                    self.log("Sentido de giro: Horário", "info")
            else:
                if self.inversor.definir_sentido_anti_horario():
                    self.log("Sentido de giro: Anti-horário", "info")
                    
    def configuracao_padrao(self):
        """Aplica configuração padrão"""
        if self.inversor:
            if self.inversor.configuracao_padrao():
                self.velocidade_var.set("30")
                self.sentido_var.set("horario")
                self.log("Configuração padrão aplicada: 30 Hz, Sentido Horário", "sucesso")
                self.atualizar_dados()
                
    def atualizar_dados(self):
        """Atualiza os dados de monitoramento"""
        if not self.inversor or not self.conectado:
            return
            
        try:
            # Estado do motor
            estado = self.inversor.verificar_estado_motor()
            if estado is not None:
                if estado:
                    self.estado_motor_label.config(text="GIRANDO", fg=self.cor_secundaria)
                else:
                    self.estado_motor_label.config(text="PARADO", fg=self.cor_offline)
            
            # Velocidade atual
            velocidade = self.inversor.verificar_velocidade()
            if velocidade is not None:
                self.velocidade_atual_label.config(text=f"{velocidade} Hz")
            
            # Temperatura
            temp = self.inversor.verificar_temperatura()
            if temp is not None:
                self.temp_label.config(text=f"{temp}")
            
            # Corrente
            corrente = self.inversor.verificar_corrente()
            if corrente is not None:
                self.corrente_label.config(text=f"{corrente}")
            
            # Tensão
            tensao = self.inversor.verificar_tensao()
            if tensao is not None:
                self.tensao_label.config(text=f"{tensao}")
                
        except Exception as e:
            self.log(f"Erro ao atualizar dados: {str(e)}", "erro")
            
    def toggle_auto_atualizar(self):
        """Alterna atualização automática"""
        if not self.conectado:
            messagebox.showwarning("Aviso", "Conecte-se ao inversor primeiro")
            return
            
        self.atualizando = not self.atualizando
        
        if self.atualizando:
            self.btn_auto_atualizar.config(text="⏸ Parar Monitoramento Automático",
                                          bg=self.cor_perigo,
                                          activebackground="#C62828")
            self.log("Monitoramento automático iniciado", "info")
            self.auto_atualizar_loop()
        else:
            self.btn_auto_atualizar.config(text="▶ Iniciar Monitoramento Automático",
                                          bg=self.cor_secundaria,
                                          activebackground="#2E7D32")
            self.log("Monitoramento automático pausado", "info")
            
    def auto_atualizar_loop(self):
        """Loop de atualização automática"""
        if self.atualizando and self.conectado:
            self.atualizar_dados()
            self.root.after(2000, self.auto_atualizar_loop)  # Atualiza a cada 2 segundos
            
    def on_closing(self):
        """Função chamada ao fechar a janela"""
        if self.conectado and self.inversor:
            self.inversor.desconectar()
            self.log("Sistema encerrado", "info")
        self.root.destroy()


def main():
    """Função principal"""
    root = tk.Tk()
    app = InversorGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
