"""
Interface Gráfica Profissional - Tema Escuro
Controle do Inversor de Frequência SENAI
Protocolo ModBus TCP
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from main import InversorControl


class InversorGUI:
    """Interface gráfica profissional com tema escuro"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SENAI - Sistema de Controle de Inversor")
        self.root.geometry("1200x900")
        self.root.resizable(True, True)
        
        # Variáveis
        self.inversor = None
        self.conectado = False
        self.atualizando = False
        
        # Cores do tema escuro profissional
        self.cor_fundo_escuro = "#1E1E1E"        # Fundo principal
        self.cor_fundo_card = "#2D2D2D"           # Fundo dos cards
        self.cor_fundo_input = "#3A3A3A"          # Fundo dos inputs
        self.cor_borda = "#404040"                 # Bordas
        self.cor_texto_primario = "#E0E0E0"       # Texto principal
        self.cor_texto_secundario = "#B0B0B0"     # Texto secundário
        self.cor_primaria = "#0D7377"             # Azul ciano profissional
        self.cor_primaria_hover = "#14A085"       # Hover primário
        self.cor_sucesso = "#4CAF50"               # Verde sucesso
        self.cor_erro = "#F44336"                  # Vermelho erro
        self.cor_aviso = "#FF9800"                 # Laranja aviso
        self.cor_info = "#2196F3"                  # Azul info
        self.cor_offline = "#757575"               # Cinza offline
        self.cor_ativo = "#00E676"                 # Verde ativo
        
        # Configurar fundo escuro
        self.root.configure(bg=self.cor_fundo_escuro)
        
        self.criar_interface()
        
    def criar_interface(self):
        """Cria todos os componentes da interface"""
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.cor_fundo_escuro, padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== CABEÇALHO PROFISSIONAL ==========
        header_frame = tk.Frame(main_container, bg=self.cor_fundo_card, height=70, relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Logo/Título à esquerda
        title_container = tk.Frame(header_frame, bg=self.cor_fundo_card)
        title_container.pack(side=tk.LEFT, padx=20, pady=15)
        
        title_label = tk.Label(title_container,
                              text="SENAI",
                              font=('Segoe UI', 20, 'bold'),
                              bg=self.cor_fundo_card,
                              fg=self.cor_primaria)
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_container,
                                text="Sistema de Controle de Inversor de Frequência",
                                font=('Segoe UI', 10),
                                bg=self.cor_fundo_card,
                                fg=self.cor_texto_secundario)
        subtitle_label.pack(anchor=tk.W)
        
        # Status à direita
        status_container = tk.Frame(header_frame, bg=self.cor_fundo_card)
        status_container.pack(side=tk.RIGHT, padx=20, pady=15)
        
        status_title = tk.Label(status_container,
                               text="Status do Sistema:",
                               font=('Segoe UI', 9),
                               bg=self.cor_fundo_card,
                               fg=self.cor_texto_secundario)
        status_title.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_indicator = tk.Label(status_container,
                                        text="●",
                                        font=('Segoe UI', 16),
                                        bg=self.cor_fundo_card,
                                        fg=self.cor_offline)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(status_container,
                                    text="OFFLINE",
                                    font=('Segoe UI', 11, 'bold'),
                                    bg=self.cor_fundo_card,
                                    fg=self.cor_offline)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # ========== LINHA SUPERIOR: CONEXÃO E CONTROLE ==========
        top_row = tk.Frame(main_container, bg=self.cor_fundo_escuro)
        top_row.pack(fill=tk.X, pady=(0, 15))
        
        # Card de Conexão
        conexao_card = self.criar_card(top_row, "Conexão", width=400)
        conexao_frame = conexao_card['frame']
        
        # IP Input
        ip_container = tk.Frame(conexao_frame, bg=self.cor_fundo_card)
        ip_container.pack(fill=tk.X, padx=15, pady=15)
        
        ip_label = tk.Label(ip_container,
                           text="Endereço IP:",
                           font=('Segoe UI', 10, 'bold'),
                           bg=self.cor_fundo_card,
                           fg=self.cor_texto_primario)
        ip_label.pack(anchor=tk.W, pady=(0, 8))
        
        input_frame = tk.Frame(ip_container, bg=self.cor_fundo_card)
        input_frame.pack(fill=tk.X)
        
        self.ip_entry = tk.Entry(input_frame,
                                 font=('Consolas', 11),
                                 bg=self.cor_fundo_input,
                                 fg=self.cor_texto_primario,
                                 insertbackground=self.cor_texto_primario,
                                 relief=tk.FLAT,
                                 borderwidth=0,
                                 highlightthickness=1,
                                 highlightbackground=self.cor_borda,
                                 highlightcolor=self.cor_primaria)
        self.ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipadx=10, ipady=8)
        self.ip_entry.insert(0, "192.168.1.100")
        
        self.btn_conectar = tk.Button(input_frame,
                                     text="CONECTAR",
                                     font=('Segoe UI', 9, 'bold'),
                                     bg=self.cor_primaria,
                                     fg='white',
                                     activebackground=self.cor_primaria_hover,
                                     activeforeground='white',
                                     relief=tk.FLAT,
                                     padx=20,
                                     pady=8,
                                     cursor='hand2',
                                     command=self.conectar)
        self.btn_conectar.pack(side=tk.LEFT, padx=(10, 0))
        
        # Card de Controle do Motor
        controle_card = self.criar_card(top_row, "Controle do Motor", width=780)
        controle_frame = controle_card['frame']
        
        # Botões de controle
        btn_container = tk.Frame(controle_frame, bg=self.cor_fundo_card)
        btn_container.pack(pady=20)
        
        self.btn_ligar = tk.Button(btn_container,
                                   text="▶ INICIAR",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.cor_sucesso,
                                   fg='white',
                                   activebackground="#45A049",
                                   activeforeground='white',
                                   relief=tk.FLAT,
                                   padx=30,
                                   pady=12,
                                   cursor='hand2',
                                   state=tk.DISABLED,
                                   command=self.ligar_motor)
        self.btn_ligar.pack(side=tk.LEFT, padx=8)
        
        self.btn_parar = tk.Button(btn_container,
                                   text="⏸ PARAR",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.cor_erro,
                                   fg='white',
                                   activebackground="#E53935",
                                   activeforeground='white',
                                   relief=tk.FLAT,
                                   padx=30,
                                   pady=12,
                                   cursor='hand2',
                                   state=tk.DISABLED,
                                   command=self.parar_motor)
        self.btn_parar.pack(side=tk.LEFT, padx=8)
        
        self.btn_config_padrao = tk.Button(btn_container,
                                          text="⚙ PADRÃO",
                                          font=('Segoe UI', 11, 'bold'),
                                          bg=self.cor_aviso,
                                          fg='white',
                                          activebackground="#FB8C00",
                                          activeforeground='white',
                                          relief=tk.FLAT,
                                          padx=30,
                                          pady=12,
                                          cursor='hand2',
                                          state=tk.DISABLED,
                                          command=self.configuracao_padrao)
        self.btn_config_padrao.pack(side=tk.LEFT, padx=8)
        
        # Estado do motor
        estado_container = tk.Frame(controle_frame, bg=self.cor_fundo_card)
        estado_container.pack(pady=15)
        
        estado_title = tk.Label(estado_container,
                                text="Estado Atual:",
                                font=('Segoe UI', 10),
                                bg=self.cor_fundo_card,
                                fg=self.cor_texto_secundario)
        estado_title.pack(side=tk.LEFT, padx=10)
        
        self.estado_motor_label = tk.Label(estado_container,
                                          text="OFFLINE",
                                          font=('Segoe UI', 16, 'bold'),
                                          bg=self.cor_fundo_card,
                                          fg=self.cor_offline)
        self.estado_motor_label.pack(side=tk.LEFT, padx=10)
        
        # ========== LINHA MÉDIA: CONFIGURAÇÃO ==========
        config_row = tk.Frame(main_container, bg=self.cor_fundo_escuro)
        config_row.pack(fill=tk.X, pady=(0, 15))
        
        # Card de Velocidade
        velocidade_card = self.criar_card(config_row, "Velocidade", width=580)
        velocidade_frame = velocidade_card['frame']
        
        vel_container = tk.Frame(velocidade_frame, bg=self.cor_fundo_card)
        vel_container.pack(fill=tk.X, padx=15, pady=15)
        
        vel_label = tk.Label(vel_container,
                             text="Velocidade Setpoint (Hz):",
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.cor_fundo_card,
                             fg=self.cor_texto_primario)
        vel_label.pack(anchor=tk.W, pady=(0, 10))
        
        vel_input_frame = tk.Frame(vel_container, bg=self.cor_fundo_card)
        vel_input_frame.pack(fill=tk.X)
        
        self.velocidade_var = tk.StringVar(value="30")
        velocidade_spin = tk.Spinbox(vel_input_frame,
                                     from_=1,
                                     to=60,
                                     textvariable=self.velocidade_var,
                                     font=('Consolas', 12, 'bold'),
                                     bg=self.cor_fundo_input,
                                     fg=self.cor_texto_primario,
                                     insertbackground=self.cor_texto_primario,
                                     buttonbackground=self.cor_primaria,
                                     buttonuprelief=tk.FLAT,
                                     buttondownrelief=tk.FLAT,
                                     relief=tk.FLAT,
                                     borderwidth=0,
                                     highlightthickness=1,
                                     highlightbackground=self.cor_borda,
                                     highlightcolor=self.cor_primaria,
                                     width=8)
        velocidade_spin.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_definir_velocidade = tk.Button(vel_input_frame,
                                               text="APLICAR",
                                               font=('Segoe UI', 9, 'bold'),
                                               bg=self.cor_primaria,
                                               fg='white',
                                               activebackground=self.cor_primaria_hover,
                                               activeforeground='white',
                                               relief=tk.FLAT,
                                               padx=20,
                                               pady=8,
                                               cursor='hand2',
                                               state=tk.DISABLED,
                                               command=self.definir_velocidade)
        self.btn_definir_velocidade.pack(side=tk.LEFT)
        
        vel_atual_container = tk.Frame(vel_container, bg=self.cor_fundo_card)
        vel_atual_container.pack(fill=tk.X, pady=(15, 0))
        
        vel_atual_label = tk.Label(vel_atual_container,
                                  text="Velocidade Atual:",
                                  font=('Segoe UI', 9),
                                  bg=self.cor_fundo_card,
                                  fg=self.cor_texto_secundario)
        vel_atual_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.velocidade_atual_label = tk.Label(vel_atual_container,
                                               text="--- Hz",
                                               font=('Consolas', 18, 'bold'),
                                               bg=self.cor_fundo_card,
                                               fg=self.cor_primaria)
        self.velocidade_atual_label.pack(side=tk.LEFT)
        
        # Card de Sentido de Giro
        sentido_card = self.criar_card(config_row, "Sentido de Giro", width=580)
        sentido_frame = sentido_card['frame']
        
        sentido_container = tk.Frame(sentido_frame, bg=self.cor_fundo_card)
        sentido_container.pack(fill=tk.X, padx=15, pady=15)
        
        sentido_label = tk.Label(sentido_container,
                                text="Direção de Rotação:",
                                font=('Segoe UI', 10, 'bold'),
                                bg=self.cor_fundo_card,
                                fg=self.cor_texto_primario)
        sentido_label.pack(anchor=tk.W, pady=(0, 15))
        
        self.sentido_var = tk.StringVar(value="horario")
        
        sentido_frame_radio = tk.Frame(sentido_container, bg=self.cor_fundo_card)
        sentido_frame_radio.pack(fill=tk.X)
        
        rb_horario = tk.Radiobutton(sentido_frame_radio,
                                    text="Horário ↻",
                                    variable=self.sentido_var,
                                    value="horario",
                                    font=('Segoe UI', 11),
                                    bg=self.cor_fundo_card,
                                    fg=self.cor_texto_primario,
                                    activebackground=self.cor_fundo_card,
                                    activeforeground=self.cor_primaria,
                                    selectcolor=self.cor_fundo_card,
                                    indicatoron=True,
                                    command=self.definir_sentido,
                                    cursor='hand2')
        rb_horario.pack(side=tk.LEFT, padx=20)
        
        rb_anti_horario = tk.Radiobutton(sentido_frame_radio,
                                        text="Anti-horário ↺",
                                        variable=self.sentido_var,
                                        value="anti_horario",
                                        font=('Segoe UI', 11),
                                        bg=self.cor_fundo_card,
                                        fg=self.cor_texto_primario,
                                        activebackground=self.cor_fundo_card,
                                        activeforeground=self.cor_primaria,
                                        selectcolor=self.cor_fundo_card,
                                        indicatoron=True,
                                        command=self.definir_sentido,
                                        cursor='hand2')
        rb_anti_horario.pack(side=tk.LEFT, padx=20)
        
        # ========== LINHA DE MONITORAMENTO ==========
        monitor_card = self.criar_card(main_container, "Monitoramento em Tempo Real")
        monitor_frame = monitor_card['frame']
        
        # Grid para métricas
        monitor_frame.columnconfigure(0, weight=1)
        monitor_frame.columnconfigure(1, weight=1)
        monitor_frame.columnconfigure(2, weight=1)
        
        # Cards de métricas
        temp_card = self.criar_metric_card_dark(monitor_frame, "TEMPERATURA", "---", "°C", 0, 0)
        self.temp_label = temp_card['value']
        
        corrente_card = self.criar_metric_card_dark(monitor_frame, "CORRENTE", "---", "A", 0, 1)
        self.corrente_label = corrente_card['value']
        
        tensao_card = self.criar_metric_card_dark(monitor_frame, "TENSÃO", "---", "V", 0, 2)
        self.tensao_label = tensao_card['value']
        
        # Controles de atualização
        atualizar_container = tk.Frame(monitor_frame, bg=self.cor_fundo_card)
        atualizar_container.grid(row=1, column=0, columnspan=3, pady=20, sticky=tk.X)
        
        self.btn_atualizar = tk.Button(atualizar_container,
                                      text="🔄 ATUALIZAR AGORA",
                                      font=('Segoe UI', 9, 'bold'),
                                      bg=self.cor_info,
                                      fg='white',
                                      activebackground="#1976D2",
                                      activeforeground='white',
                                      relief=tk.FLAT,
                                      padx=20,
                                      pady=10,
                                      cursor='hand2',
                                      command=self.atualizar_dados)
        self.btn_atualizar.pack(side=tk.LEFT, padx=10)
        
        self.btn_auto_atualizar = tk.Button(atualizar_container,
                                            text="▶ INICIAR MONITORAMENTO",
                                            font=('Segoe UI', 9, 'bold'),
                                            bg=self.cor_sucesso,
                                            fg='white',
                                            activebackground="#45A049",
                                            activeforeground='white',
                                            relief=tk.FLAT,
                                            padx=20,
                                            pady=10,
                                            cursor='hand2',
                                            command=self.toggle_auto_atualizar)
        self.btn_auto_atualizar.pack(side=tk.LEFT, padx=10)
        
        # ========== LOG ==========
        log_card = self.criar_card(main_container, "Log de Operações do Sistema")
        log_frame = log_card['frame']
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  height=10,
                                                  font=('Consolas', 9),
                                                  bg=self.cor_fundo_input,
                                                  fg=self.cor_texto_primario,
                                                  insertbackground=self.cor_texto_primario,
                                                  relief=tk.FLAT,
                                                  borderwidth=0,
                                                  highlightthickness=1,
                                                  highlightbackground=self.cor_borda)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configurar tags para cores no log
        self.log_text.tag_config("sucesso", foreground=self.cor_sucesso, font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("erro", foreground=self.cor_erro, font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("info", foreground=self.cor_info, font=('Consolas', 9))
        self.log_text.tag_config("timestamp", foreground=self.cor_texto_secundario, font=('Consolas', 8))
        
        # Mensagem inicial
        self.log("Sistema inicializado. Aguardando conexão com o inversor...", "info")
        
    def criar_card(self, parent, title, width=None):
        """Cria um card com título no tema escuro"""
        card_frame = tk.Frame(parent, bg=self.cor_fundo_card, relief=tk.FLAT, borderwidth=1, highlightbackground=self.cor_borda, highlightthickness=1)
        if width:
            card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        else:
            card_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Título do card
        title_frame = tk.Frame(card_frame, bg=self.cor_fundo_input, height=35)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame,
                              text=title,
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.cor_fundo_input,
                              fg=self.cor_texto_primario)
        title_label.pack(side=tk.LEFT, padx=12, pady=8)
        
        # Frame de conteúdo
        content_frame = tk.Frame(card_frame, bg=self.cor_fundo_card)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return {'frame': content_frame, 'card': card_frame}
        
    def criar_metric_card_dark(self, parent, title, value, unit, row, col):
        """Cria um card de métrica no tema escuro"""
        metric_frame = tk.Frame(parent, bg=self.cor_fundo_input, relief=tk.FLAT, borderwidth=1, highlightbackground=self.cor_borda, highlightthickness=1)
        metric_frame.grid(row=row, column=col, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N))
        metric_frame.columnconfigure(0, weight=1)
        
        title_label = tk.Label(metric_frame,
                              text=title,
                              font=('Segoe UI', 9, 'bold'),
                              bg=self.cor_fundo_input,
                              fg=self.cor_texto_secundario)
        title_label.pack(pady=(15, 10))
        
        value_label = tk.Label(metric_frame,
                              text=value,
                              font=('Consolas', 28, 'bold'),
                              bg=self.cor_fundo_input,
                              fg=self.cor_primaria)
        value_label.pack()
        
        unit_label = tk.Label(metric_frame,
                             text=unit,
                             font=('Segoe UI', 10),
                             bg=self.cor_fundo_input,
                             fg=self.cor_texto_secundario)
        unit_label.pack(pady=(5, 15))
        
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
                    self.btn_conectar.config(text="DESCONECTAR", bg=self.cor_erro, activebackground="#E53935")
                    self.status_indicator.config(fg=self.cor_ativo)
                    self.status_label.config(text="ONLINE", fg=self.cor_ativo)
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
            self.btn_conectar.config(text="CONECTAR", bg=self.cor_primaria, activebackground=self.cor_primaria_hover)
            self.status_indicator.config(fg=self.cor_offline)
            self.status_label.config(text="OFFLINE", fg=self.cor_offline)
            self.ip_entry.config(state=tk.NORMAL)
            self.habilitar_controles(False)
            self.estado_motor_label.config(text="OFFLINE", fg=self.cor_offline)
            self.log("Desconectado do inversor", "info")
            self.atualizando = False
            self.btn_auto_atualizar.config(text="▶ INICIAR MONITORAMENTO", bg=self.cor_sucesso, activebackground="#45A049")
            
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
                    self.estado_motor_label.config(text="GIRANDO", fg=self.cor_ativo)
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
            self.btn_auto_atualizar.config(text="⏸ PARAR MONITORAMENTO",
                                          bg=self.cor_erro,
                                          activebackground="#E53935")
            self.log("Monitoramento automático iniciado", "info")
            self.auto_atualizar_loop()
        else:
            self.btn_auto_atualizar.config(text="▶ INICIAR MONITORAMENTO",
                                          bg=self.cor_sucesso,
                                          activebackground="#45A049")
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
