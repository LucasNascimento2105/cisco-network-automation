# 🚀 Cisco Network Automation & IaC (Python + Netmiko)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Netmiko](https://img.shields.io/badge/Netmiko-4.0+-brightgreen.svg)](https://github.com/ktbyers/netmiko)
[![Cisco DevNet](https://img.shields.io/badge/Cisco_DevNet-Sandbox-cyan.svg)](https://developer.cisco.com/)

> 🇺🇸 **English Version available:** Scroll down to the bottom of this page.

---

## 🇧🇷 Português

### 🎯 Sobre o Projeto
Este laboratório demonstra a implementação prática e profissional de **Infraestrutura como Código (IaC)** e **Automação de Redes** voltada para dispositivos Cisco IOS reais. O projeto valida a viabilidade de provisionar ativos de rede eliminando a incidência de falhas operacionais através de scripts interativos.

### 🧠 Como a Arquitetura Funciona
Para garantir um alto grau de fidelidade com o ambiente corporativo real, a arquitetura foi desenhada da seguinte forma:

1. **Infraestrutura Real (Cloud / Hardware):** O script interage diretamente com servidores reais da Cisco hospedados na nuvem (Cisco DevNet Sandbox) através da internet, ou diretamente em roteadores físicos via Ethernet.
2. **Segurança (SSH2):** O protocolo Telnet em texto plano foi descartado para o canal principal. A comunicação ocorre exclusivamente através de tunelamento **SSH versão 2**.
3. **O Motor de Execução (Netmiko):** A biblioteca `Netmiko` gerencia todo o I/O, lidando automaticamente com os *prompts* do Cisco IOS, transições para modo privilegiado (`enable`) e paginação.

### ⚙️ Funcionalidades Principais
* **🛡️ Backup Automatizado (Rollback):** Extrai a configuração atual (`show running-config`) e salva localmente em um arquivo `.txt` com carimbo de data e hora, permitindo rollbacks emergenciais.
* **👁️ Parsing Dinâmico (Regex):** Aplica Expressões Regulares (`re.findall`) na tabela de interfaces do roteador para mapear portas ativas de forma dinâmica.
* **📥 Deploy de Configurações (IaC):** O sistema permite carregar arquivos de backup ou templates e injetá-los no equipamento de forma sequencial.
* **🔐 Gestão de Controle de Acesso:** Automatiza a criação de usuários locais com privilégio máximo e configuração de linhas VTY.

### 📁 Estrutura de Arquivos
```text
/
├── automacao.py            # Script principal da automação
├── requirements.txt        # Dependências do projeto Python
├── .env                    # Arquivo de variáveis de ambiente (Credenciais/IPs)
└── README.md               # Esta documentação
```

## 🇺🇸 English

### 🎯 About the Project
This lab demonstrates the practical and professional implementation of **Infrastructure as Code (IaC)** and **Network Automation** aimed at real Cisco IOS devices. The project validates the feasibility of provisioning network assets by eliminating human error through interactive scripts.

### 🧠 How the Architecture Works
To ensure a high degree of fidelity with corporate production environments, the architecture works as follows:

1. **Real Infrastructure:** The script interacts directly with real Cisco servers hosted in the cloud (Cisco DevNet Sandbox) over the internet, or directly on physical routers via Ethernet.
2. **Security (SSH2):** Telnet was discarded. Communication occurs exclusively through **SSH version 2** tunneling.
3. **Execution Engine (Netmiko):** The `Netmiko` library manages all I/O, handling Cisco IOS prompts and privilege escalation automatically.

### ⚙️ Main Features
* **🛡️ Automated Backup:** Extracts running-config and saves locally with timestamps for emergency rollbacks.
* **👁️ Dynamic Interface Parsing (Regex):** Applies Regular Expressions to map active ports dynamically.
* **📥 Rollback & Deploy System:** Restores previous network configurations seamlessly from local backups.
* **🔐 Remote Access Configuration:** Automates SSH/Telnet security baselines on the device.

### 📁 File Structure
```text
/
├── automacao.py            # Main automation script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables file (Credentials/IPs)
└── README.md               # This documentation
