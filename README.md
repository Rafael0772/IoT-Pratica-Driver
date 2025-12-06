# Controle do Inversor de Frequência SENAI

Aplicação Python para controle de um Inversor de Frequência através do protocolo ModBus TCP.

## Funcionalidades

- ✅ Ligar o motor
- ✅ Parar o motor
- ✅ Definir a velocidade (1-60 Hz)
- ✅ Verificar temperatura
- ✅ Verificar corrente
- ✅ Verificar tensão
- ✅ Definir sentido de giro (Horário/Anti-horário)
- ✅ Verificar estado do motor
- ✅ Configuração padrão (30Hz, sentido horário)

## Requisitos

- Python 3.7 ou superior
- Anaconda Navigator (recomendado)
- Biblioteca uModBus 1.0.4

## Instalação

1. Instale o Anaconda Navigator: https://www.anaconda.com/

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

Ou instale diretamente:
```bash
pip install umodbus==1.0.4
```

## Uso

### Interface Gráfica (Recomendado)

Execute a interface gráfica:
```bash
python gui.py
```

A interface gráfica oferece:
- Conexão visual com indicador de status
- Controles intuitivos para todas as funcionalidades
- Monitoramento em tempo real dos parâmetros do motor
- Atualização automática dos dados
- Log de operações

### Interface de Linha de Comando

Execute o programa em modo texto:
```bash
python main.py
```

O programa solicitará o endereço IP do inversor. Após conectar, você terá acesso ao menu de controle.

## Especificações Técnicas

- **Protocolo**: ModBus TCP
- **Endereço Escravo**: 2
- **Porta Padrão**: 502
- **Velocidade Mínima**: 1 Hz
- **Velocidade Máxima**: 60 Hz
- **Velocidade Padrão**: 30 Hz

## Registradores ModBus

### Registradores Digitais de Saída
- **1100**: Ligar/Desligar motor (1=Ligado, 0=Desligado)
- **1101**: Sentido de giro (1=Anti-horário, 0=Horário)

### Registradores Digitais de Entrada
- **100**: Estado do motor (1=Girando, 0=Parado)

### Registradores Analógicos de Entrada
- **30400**: Velocidade atual (Hz)
- **30401**: Corrente (A)
- **30402**: Tensão (V)
- **30403**: Temperatura (°C)

### Registradores Analógicos de Saída
- **41400**: Velocidade setpoint (Hz)

## Estrutura do Projeto

```
IoT-Pratica-Driver/
├── main.py               # Código principal (CLI)
├── gui.py                # Interface gráfica
├── requirements.txt      # Dependências
└── README.md             # Documentação
```

## Desenvolvimento

Este projeto foi desenvolvido para o SENAI como parte de uma atividade de controle de inversor de frequência.

## Autor

Desenvolvido para o SENAI

