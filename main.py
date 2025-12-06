"""
Aplicação de Controle do Inversor de Frequência SENAI
Protocolo ModBus TCP
Endereço Escravo: 2
"""

from socket import create_connection
from umodbus import conf
from umodbus.client import tcp
import sys
import time


class InversorControl:
    """Classe para controlar o Inversor de Frequência via ModBus TCP"""
    
    # Endereços dos registradores
    REG_LIGAR_DESLIGAR = 1100
    REG_SENTIDO_GIRO = 1101
    REG_ESTADO_MOTOR = 100
    REG_VELOCIDADE_ATUAL = 30400
    REG_CORRENTE = 30401
    REG_TENSAO = 30402
    REG_TEMPERATURA = 30403
    REG_VELOCIDADE_SETPOINT = 41400
    
    # Endereço escravo
    SLAVE_ID = 2
    
    # Velocidade padrão
    VELOCIDADE_PADRAO = 30  # Hz
    VELOCIDADE_MIN = 1  # Hz
    VELOCIDADE_MAX = 60  # Hz
    
    def __init__(self, ip_address, port=502):
        """
        Inicializa a conexão com o inversor
        
        Args:
            ip_address: Endereço IP do inversor
            port: Porta ModBus TCP (padrão: 502)
        """
        self.ip_address = ip_address
        self.port = port
        self.sock = None
        conf.SIGNED_VALUES = True
        
    def conectar(self):
        """Estabelece conexão com o inversor"""
        try:
            self.sock = create_connection((self.ip_address, self.port))
            print(f"Conectado ao inversor em {self.ip_address}:{self.port}")
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """Fecha a conexão com o inversor"""
        if self.sock:
            self.sock.close()
            print("Conexão encerrada")
    
    def ler_registrador_coil(self, endereco):
        """Lê um registrador digital (coil)"""
        try:
            message = tcp.read_coils(self.SLAVE_ID, endereco, 1)
            response = tcp.send_message(message, self.sock)
            return response[0] if response else None
        except Exception as e:
            print(f"Erro ao ler registrador {endereco}: {e}")
            return None
    
    def escrever_registrador_coil(self, endereco, valor):
        """Escreve em um registrador digital (coil)"""
        try:
            message = tcp.write_single_coil(self.SLAVE_ID, endereco, valor)
            tcp.send_message(message, self.sock)
            return True
        except Exception as e:
            print(f"Erro ao escrever registrador {endereco}: {e}")
            return False
    
    def ler_registrador_holding(self, endereco):
        """Lê um registrador analógico de saída (holding register)"""
        try:
            message = tcp.read_holding_registers(self.SLAVE_ID, endereco, 1)
            response = tcp.send_message(message, self.sock)
            return response[0] if response else None
        except Exception as e:
            print(f"Erro ao ler registrador {endereco}: {e}")
            return None
    
    def escrever_registrador_holding(self, endereco, valor):
        """Escreve em um registrador analógico de saída (holding register)"""
        try:
            message = tcp.write_single_register(self.SLAVE_ID, endereco, int(valor))
            tcp.send_message(message, self.sock)
            return True
        except Exception as e:
            print(f"Erro ao escrever registrador {endereco}: {e}")
            return False
    
    def ler_registrador_input(self, endereco):
        """Lê um registrador analógico de entrada (input register)"""
        try:
            message = tcp.read_input_registers(self.SLAVE_ID, endereco, 1)
            response = tcp.send_message(message, self.sock)
            return response[0] if response else None
        except Exception as e:
            print(f"Erro ao ler registrador {endereco}: {e}")
            return None
    
    def ler_registrador_discrete_input(self, endereco):
        """Lê um registrador digital de entrada (discrete input)"""
        try:
            message = tcp.read_discrete_inputs(self.SLAVE_ID, endereco, 1)
            response = tcp.send_message(message, self.sock)
            return response[0] if response else None
        except Exception as e:
            print(f"Erro ao ler registrador {endereco}: {e}")
            return None
    
    def ligar_motor(self):
        """Liga o motor"""
        return self.escrever_registrador_coil(self.REG_LIGAR_DESLIGAR, True)
    
    def parar_motor(self):
        """Para o motor"""
        return self.escrever_registrador_coil(self.REG_LIGAR_DESLIGAR, False)
    
    def definir_velocidade(self, velocidade):
        """
        Define a velocidade do motor
        
        Args:
            velocidade: Velocidade em Hz (1-60)
        
        Returns:
            True se sucesso, False caso contrário
        """
        if velocidade < self.VELOCIDADE_MIN or velocidade > self.VELOCIDADE_MAX:
            print(f"Erro: Velocidade deve estar entre {self.VELOCIDADE_MIN} e {self.VELOCIDADE_MAX} Hz")
            return False
        return self.escrever_registrador_holding(self.REG_VELOCIDADE_SETPOINT, int(velocidade))
    
    def definir_sentido_horario(self):
        """Define o sentido de giro como horário"""
        return self.escrever_registrador_coil(self.REG_SENTIDO_GIRO, False)
    
    def definir_sentido_anti_horario(self):
        """Define o sentido de giro como anti-horário"""
        return self.escrever_registrador_coil(self.REG_SENTIDO_GIRO, True)
    
    def verificar_temperatura(self):
        """Retorna a temperatura do motor em graus Celsius"""
        return self.ler_registrador_input(self.REG_TEMPERATURA)
    
    def verificar_corrente(self):
        """Retorna a corrente do motor em Amperes"""
        return self.ler_registrador_input(self.REG_CORRENTE)
    
    def verificar_tensao(self):
        """Retorna a tensão do motor em Volts"""
        return self.ler_registrador_input(self.REG_TENSAO)
    
    def verificar_velocidade(self):
        """Retorna a velocidade atual do motor em Hz"""
        return self.ler_registrador_input(self.REG_VELOCIDADE_ATUAL)
    
    def verificar_estado_motor(self):
        """Retorna o estado do motor (True = Girando, False = Parado)"""
        return self.ler_registrador_discrete_input(self.REG_ESTADO_MOTOR)
    
    def configuracao_padrao(self):
        """Configura o motor com valores padrão: 30Hz e sentido horário"""
        print("Aplicando configuração padrão...")
        if self.definir_velocidade(self.VELOCIDADE_PADRAO):
            print(f"Velocidade definida: {self.VELOCIDADE_PADRAO} Hz")
        if self.definir_sentido_horario():
            print("Sentido de giro: Horário")
        return True


def exibir_menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("CONTROLE DO INVERSOR DE FREQUÊNCIA SENAI")
    print("="*50)
    print("1. Ligar motor")
    print("2. Parar motor")
    print("3. Definir velocidade")
    print("4. Verificar temperatura")
    print("5. Verificar corrente")
    print("6. Verificar tensão")
    print("7. Definir sentido de giro")
    print("8. Verificar estado do motor")
    print("9. Aplicar configuração padrão (30Hz, Horário)")
    print("10. Exibir informações completas")
    print("0. Sair")
    print("="*50)


def main():
    """Função principal"""
    print("Aplicação de Controle do Inversor de Frequência SENAI")
    print("Protocolo ModBus TCP")
    
    # Solicita o endereço IP
    ip = input("\nDigite o endereço IP do inversor: ").strip()
    
    if not ip:
        print("Erro: Endereço IP não fornecido")
        return
    
    # Cria instância do controlador
    inversor = InversorControl(ip)
    
    # Tenta conectar
    if not inversor.conectar():
        print("Não foi possível conectar ao inversor. Verifique o endereço IP.")
        return
    
    try:
        while True:
            exibir_menu()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "0":
                print("Encerrando aplicação...")
                break
            
            elif opcao == "1":
                if inversor.ligar_motor():
                    print("Motor ligado com sucesso!")
                else:
                    print("Erro ao ligar o motor")
            
            elif opcao == "2":
                if inversor.parar_motor():
                    print("Motor parado com sucesso!")
                else:
                    print("Erro ao parar o motor")
            
            elif opcao == "3":
                try:
                    velocidade = float(input(f"Digite a velocidade (1-60 Hz): "))
                    if inversor.definir_velocidade(velocidade):
                        print(f"Velocidade definida: {velocidade} Hz")
                    else:
                        print("Erro ao definir velocidade")
                except ValueError:
                    print("Erro: Digite um número válido")
            
            elif opcao == "4":
                temp = inversor.verificar_temperatura()
                if temp is not None:
                    print(f"Temperatura: {temp} °C")
                else:
                    print("Erro ao ler temperatura")
            
            elif opcao == "5":
                corrente = inversor.verificar_corrente()
                if corrente is not None:
                    print(f"Corrente: {corrente} A")
                else:
                    print("Erro ao ler corrente")
            
            elif opcao == "6":
                tensao = inversor.verificar_tensao()
                if tensao is not None:
                    print(f"Tensão: {tensao} V")
                else:
                    print("Erro ao ler tensão")
            
            elif opcao == "7":
                print("1. Horário")
                print("2. Anti-horário")
                sentido = input("Escolha o sentido: ").strip()
                if sentido == "1":
                    if inversor.definir_sentido_horario():
                        print("Sentido definido: Horário")
                    else:
                        print("Erro ao definir sentido")
                elif sentido == "2":
                    if inversor.definir_sentido_anti_horario():
                        print("Sentido definido: Anti-horário")
                    else:
                        print("Erro ao definir sentido")
                else:
                    print("Opção inválida")
            
            elif opcao == "8":
                estado = inversor.verificar_estado_motor()
                if estado is not None:
                    status = "Girando" if estado else "Parado"
                    print(f"Estado do motor: {status}")
                else:
                    print("Erro ao verificar estado do motor")
            
            elif opcao == "9":
                inversor.configuracao_padrao()
                print("Configuração padrão aplicada!")
            
            elif opcao == "10":
                print("\n--- INFORMAÇÕES DO MOTOR ---")
                estado = inversor.verificar_estado_motor()
                if estado is not None:
                    print(f"Estado: {'Girando' if estado else 'Parado'}")
                
                velocidade = inversor.verificar_velocidade()
                if velocidade is not None:
                    print(f"Velocidade: {velocidade} Hz")
                
                corrente = inversor.verificar_corrente()
                if corrente is not None:
                    print(f"Corrente: {corrente} A")
                
                tensao = inversor.verificar_tensao()
                if tensao is not None:
                    print(f"Tensão: {tensao} V")
                
                temperatura = inversor.verificar_temperatura()
                if temperatura is not None:
                    print(f"Temperatura: {temperatura} °C")
            
            else:
                print("Opção inválida! Tente novamente.")
            
            input("\nPressione Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\nAplicação interrompida pelo usuário")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
    finally:
        inversor.desconectar()


if __name__ == "__main__":
    main()

