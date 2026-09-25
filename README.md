# 🚀 Cisco Network Automation & IaC (Python + Netmiko)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Netmiko](https://img.shields.io/badge/Netmiko-4.0+-brightgreen.svg)](https://github.com/ktbyers/netmiko)
[![Cisco DevNet](https://img.shields.io/badge/Cisco_DevNet-Sandbox-cyan.svg)](https://developer.cisco.com/)

> 🇺🇸 **English Version available:** Scroll down to the bottom of this page.

---

## 🇧🇷 Português

### 🎯 Sobre o Projeto
Este laboratório demonstra a implementação prática e profissional de **Infraestrutura como Código (IaC)** e **Automação de Redes** voltada para dispositivos Cisco IOS reais. O projeto valida a viabilidade de provisionar ativos de rede eliminando a incidência de falhas operacionais através de scripts interativos e mecanismos de auditoria avançados.

### 🧠 Como a Arquitetura Funciona
Para garantir um alto grau de fidelidade com o ambiente corporativo real, a arquitetura foi desenhada da seguinte forma:

1. **Infraestrutura Real (Cloud / Hardware):** O script interage diretamente com servidores reais da Cisco hospedados na nuvem (Cisco DevNet Sandbox) através da internet, ou diretamente em roteadores físicos via Ethernet.
2. **Segurança (SSH2):** O protocolo Telnet em texto plano foi descartado para o canal principal. A comunicação ocorre exclusivamente através de tunelamento **SSH versão 2**.
3. **O Motor de Execução (Netmiko):** A biblioteca `Netmiko` gerencia todo o I/O, lidando automaticamente com os *prompts* do Cisco IOS, transições para modo privilegiado (`enable`) e paginação.

### ⚙️ Funcionalidades Principais (Arquitetura Sênior)
* **🔒 Segurança Zero-Trust:** Tela de login embarcada no Python exigindo credenciais de administrador antes do handshake SSH.
* **⏪ Máquina do Tempo (Rollback Local):** Sistema de versionamento que identifica arquivos antigos de backup e permite reverter configurações quebradas da NVRAM do roteador em segundos.
* **🛡️ Painel de Auditoria Nativo:** Consulta dinâmica ao `Syslog` do roteador Cisco e listagem de usuários conectados/cadastrados em tempo real, mantendo o histórico de comandos na memória RAM.
* **👁️ Parsing Dinâmico e Validação (Regex):** Extração avançada de portas via Regex e bloqueio lógico contra usuários que tentam digitar IPs ou máscaras em formatos inválidos.
* **📥 Gestão Inteligente de Portas:** Submenu avançado que permite nomear interfaces (Description), configurar endereços, alterar o estado da porta (Up/Down) e detalhar a `running-config` da interface.

### 📁 Estrutura de Arquivos
```text
/
├── automacao.py            # Script principal da automação
├── requirements.txt        # Dependências do projeto Python
├── .env                    # Arquivo de variáveis de ambiente (Credenciais/IPs)
└── README.md               # Esta documentação
```

---

## 🇺🇸 English

### 🎯 About the Project
This lab demonstrates the practical and professional implementation of **Infrastructure as Code (IaC)** and **Network Automation** aimed at real Cisco IOS devices. The project validates the feasibility of provisioning network assets by eliminating human error through interactive scripts and advanced auditing mechanisms.

### 🧠 How the Architecture Works
To ensure a high degree of fidelity with corporate production environments, the architecture works as follows:

1. **Real Infrastructure:** The script interacts directly with real Cisco servers hosted in the cloud (Cisco DevNet Sandbox) over the internet, or directly on physical routers via Ethernet.
2. **Security (SSH2):** Telnet was discarded. Communication occurs exclusively through **SSH version 2** tunneling.
3. **Execution Engine (Netmiko):** The `Netmiko` library manages all I/O, handling Cisco IOS prompts and privilege escalation automatically.

### ⚙️ Main Features (Senior Architecture)
* **🔒 Zero-Trust Security:** Built-in Python login screen requiring admin credentials before initiating the SSH handshake.
* **⏪ Time Machine (Local Rollback):** Versioning system that identifies old backup files and allows reverting broken NVRAM router configurations in seconds.
* **🛡️ Native Audit Panel:** Dynamic querying of the Cisco router's `Syslog` and real-time listing of connected/registered users, maintaining session command history in RAM.
* **👁️ Dynamic Parsing & Validation (Regex):** Advanced port extraction via Regex and logical blocking against users typing invalid IP or subnet mask formats.
* **📥 Intelligent Port Management:** Advanced submenu that allows naming interfaces (Descriptions), configuring addresses, changing port states (Up/Down), and detailing the interface's `running-config`.

### 📁 File Structure
```text
/
├── automacao.py            # Main automation script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables file (Credentials/IPs)
└── README.md               # This documentation
```
