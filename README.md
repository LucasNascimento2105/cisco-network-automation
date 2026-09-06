# 🚀 Cisco Network Automation & IaC (Python + Netmiko)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Netmiko](https://img.shields.io/badge/Netmiko-4.0+-brightgreen.svg)](https://github.com/ktbyers/netmiko)
[![Cisco DevNet](https://img.shields.io/badge/Cisco_DevNet-Sandbox-cyan.svg)](https://developer.cisco.com/)

> 🇺🇸 **English Version available:** Scroll down to the bottom of this page.

---

## 🇧🇷 Português

### 🎯 Sobre o Projeto
Este laboratório demonstra a implementação prática e profissional de **Infraestrutura como Código (IaC)** e **Automação de Redes** voltada para dispositivos Cisco IOS reais. O projeto valida a viabilidade de provisionar ativos de rede eliminando a incidência de falhas operacionais (Human Error) através de scripts interativos.

### 🧠 Como a Arquitetura Funciona
Para garantir um alto grau de fidelidade com o ambiente de produção corporativo, não utilizamos simuladores simplificados como Packet Tracer. A arquitetura foi desenhada da seguinte forma:

1. **Infraestrutura Real (Cloud / Hardware):** O script interage diretamente com servidores reais da Cisco hospedados na Califórnia (Cisco DevNet Sandbox) através da internet, ou diretamente em roteadores físicos conectados via porta Ethernet.
2. **Segurança (SSH2):** O protocolo Telnet (texto plano) foi descartado. A comunicação ocorre exclusivamente através de tunelamento **SSH versão 2**, garantindo a criptografia dos dados.
3. **O Motor de Execução (Netmiko):** A biblioteca `Netmiko` (uma abstração do Paramiko focada em redes) gerencia todo o I/O. Ela lida automaticamente com os *prompts* do Cisco IOS, transições para modo privilegiado (`enable`) e paginação do terminal.

### ⚙️ Funcionalidades Principais
Ao executar o script, um menu de linha de comando (CLI) interativo e estilizado é apresentado, fornecendo as seguintes *features*:

*   **🛡️ Backup Automatizado (Rollback Safenet):** Extrai a configuração rodando (`show running-config`) e salva localmente em um arquivo `.txt` com carimbo de data e hora (timestamp), permitindo *rollbacks* emergenciais em caso de falha sistêmica.
*   **👁️ Parsing Dinâmico de Interfaces (Regex):** O script não lê saídas de texto bruto de forma estática. Ele aplica Expressões Regulares (`re.findall`) na tabela de interfaces do roteador para mapear portas ativas (Fast, Gig, Serial) e consulta descrições atreladas.
*   **🧠 Lógica Condicional de Hardware:** Caso o usuário decida configurar uma porta "Serial", o script injeta autonomamente o comando `clock rate 64000` (necessário para interfaces DCE).
*   **📥 Deploy de Golden Configs (IaC):** O sistema permite carregar um arquivo `.txt` (Template) contendo centenas de comandos e os aplica de forma sequencial e ininterrupta.

### 📁 Estrutura de Arquivos
```text
/
├── automacao.py              # Script principal do robô
├── requisitos.txt            # (Opcional) Dependências do Python
└── README.md                 # Esta documentação
```

### 🚀 Como Executar
1. Instale o Python e a biblioteca Netmiko (`pip install netmiko`).
2. Acesse o [Cisco DevNet Sandbox](https://developer.cisco.com/sandbox/) para obter as credenciais atualizadas de um roteador Always-On.
3. Atualize o Dicionário `roteador` no script `automacao.py`.
4. Execute `python automacao.py` no terminal.

---

## 🇺🇸 English

### 🎯 About the Project
This lab demonstrates the practical and professional implementation of **Infrastructure as Code (IaC)** and **Network Automation** aimed at real Cisco IOS devices. The project validates the feasibility of provisioning network assets by eliminating human error through interactive scripts.

### 🧠 How the Architecture Works
To ensure a high degree of fidelity with corporate production environments, we do not use simplified simulators like Packet Tracer:

1. **Real Infrastructure:** The script interacts directly with real Cisco servers hosted in California (Cisco DevNet Sandbox) over the internet, or directly on physical routers connected via Ethernet.
2. **Security (SSH2):** The Telnet protocol was discarded. Communication occurs exclusively through **SSH version 2** tunneling.
3. **Execution Engine (Netmiko):** The `Netmiko` library manages all I/O, handling Cisco IOS prompts and privilege escalation automatically.

### ⚙️ Main Features
*   **🛡️ Automated Backup:** Extracts running-config and saves locally with timestamps for emergency rollbacks.
*   **👁️ Dynamic Interface Parsing (Regex):** Applies Regular Expressions to map active ports dynamically.
*   **🧠 Hardware Conditional Logic:** Autonomously injects `clock rate` commands if a Serial port is selected.
*   **📥 Golden Configs Deploy (IaC):** Sequentially deploys hundreds of commands from a `.txt` template file.