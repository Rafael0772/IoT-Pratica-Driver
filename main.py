# ==========================================================
#   DRIVER MODBUS TCP 
#   Rafael Castro Gonçalves
#   Usando uModbus 1.0.4
# ==========================================================

import socket
from umodbus.client import tcp

# -----------------------------------------------------------
# CONFIGURAÇÕES
# -----------------------------------------------------------

IP = "192.168.0.101"   #IP do inversor
PORTA = 502     # porta padrão ModBus TCP
SLAVE = 2            # endereço escravo do PDF


# -----------------------------------------------------------
# FUNÇÃO PARA CONECTAR
# -----------------------------------------------------------

def conectar():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORTA))
        return sock
    except:
        print("❌ Não foi possível conectar ao inversor!")
        return None


# -----------------------------------------------------------
# REGISTRADORES DO PDF
# -----------------------------------------------------------

REG_LIGAR = 1100
REG_SENTIDO = 1101
REG_ESTADO = 100
REG_VELOC_ATUAL = 30400
REG_CORRENTE = 30401
REG_TENSAO = 30402
REG_TEMP = 30403
REG_SETPOINT = 41400


# -----------------------------------------------------------
# FUNÇÕES DE ESCRITA
# -----------------------------------------------------------

def ligar():
    sock = conectar()
    if sock:
        message = tcp.write_single_register(SLAVE, REG_LIGAR, 1)
        tcp.send_message(message, sock)
        sock.close()
        print("✔ Motor ligado!")


def parar():
    sock = conectar()
    if sock:
        message = tcp.write_single_register(SLAVE, REG_LIGAR, 0)
        tcp.send_message(message, sock)
        sock.close()
        print("✔ Motor desligado!")


def set_sentido():
    lado = input("Digite H (horário) ou A (anti-horário): ").upper()
    
    if lado == "H":
        valor = 0
    elif lado == "A":
        valor = 1
    else:
        print("Opção inválida!")
        return
    
    sock = conectar()
    if sock:
        message = tcp.write_single_register(SLAVE, REG_SENTIDO, valor)
        tcp.send_message(message, sock)
        sock.close()
        print("✔ Sentido definido!")


def set_velocidade():
    try:
        vel = int(input("Velocidade (1–60 Hz): "))
        if vel < 1 or vel > 60:
            print("A velocidade deve estar entre 1 e 60!")
            return
    except:
        print("Digite um número válido!")
        return

    sock = conectar()
    if sock:
        message = tcp.write_single_register(SLAVE, REG_SETPOINT, vel)
        tcp.send_message(message, sock)
        sock.close()
        print(f"✔ Velocidade definida para {vel} Hz")


# -----------------------------------------------------------
# FUNÇÕES DE LEITURA
# -----------------------------------------------------------

def ler_reg(reg):
    sock = conectar()
    if sock:
        message = tcp.read_holding_registers(SLAVE, reg, 1)
        response = tcp.send_message(message, sock)
        sock.close()
        return response[0]
    return None


def ver_estado():
    estado = ler_reg(REG_ESTADO)
    if estado == 1:
        print("✔ Motor está GIRANDO")
    elif estado == 0:
        print("✔ Motor está PARADO")
    else:
        print("❌ Erro ao ler estado")


def ver_medidas():
    print("Velocidade atual:", ler_reg(REG_VELOC_ATUAL), "Hz")
    print("Corrente:", ler_reg(REG_CORRENTE), "A")
    print("Tensão:", ler_reg(REG_TENSAO), "V")
    print("Temperatura:", ler_reg(REG_TEMP), "°C")


# -----------------------------------------------------------
# CONFIGURAÇÃO PADRÃO
# -----------------------------------------------------------

def config_padrao():
    print("Aplicando configuração padrão...")
    
    sock = conectar()
    if sock:
        message = tcp.write_single_register(SLAVE, REG_SETPOINT, 30)
        tcp.send_message(message, sock)
        message = tcp.write_single_register(SLAVE, REG_SENTIDO, 0)
        tcp.send_message(message, sock)
        message = tcp.write_single_register(SLAVE, REG_LIGAR, 1)
        tcp.send_message(message, sock)
        sock.close()

    print("✔ Configuração padrão aplicada!")


# -----------------------------------------------------------
# MENU
# -----------------------------------------------------------

def menu():
    while True:
        print("\n========= MENU PRINCIPAL =========")
        print("1 - Ligar motor")
        print("2 - Parar motor")
        print("3 - Definir velocidade")
        print("4 - Ver medidas (temp, corrente, tensão...)")
        print("5 - Definir sentido")
        print("6 - Ver estado do motor")
        print("7 - Iniciar com config padrão")
        print("0 - Sair")

        op = input("Opção: ")

        if op == "1":
            ligar()
        elif op == "2":
            parar()
        elif op == "3":
            set_velocidade()
        elif op == "4":
            ver_medidas()
        elif op == "5":
            set_sentido()
        elif op == "6":
            ver_estado()
        elif op == "7":
            config_padrao()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


# -----------------------------------------------------------
# INÍCIO
# -----------------------------------------------------------

print("Driver Modbus TCP iniciado!")
print("Conectando ao inversor na rede...")
menu()
