# 🚀 Guia de Configuração e Uso (Setup Guide)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Netmiko](https://img.shields.io/badge/Netmiko-4.0+-brightgreen.svg)](https://github.com/ktbyers/netmiko)
[![Cisco DevNet](https://img.shields.io/badge/Cisco_DevNet-Sandbox-cyan.svg)](https://developer.cisco.com/)

> 🇺🇸 **English Version available:** Scroll down to the bottom of this page.

---

## 🇧🇷 Português

Bem-vindo ao manual oficial da Automação Cisco. Siga as instruções abaixo para preparar o seu roteador físico, configurar o ambiente Python e, caso deseje, integrar o sistema à nuvem do GitHub.

### 🎯 1. Provisionamento "Day 0" (Acesso Físico)
Para que a Inteligência do Python consiga assumir o controle do roteador via rede, você deve realizar o **Day 0 Provisioning**. Conecte-se fisicamente ao roteador usando um cabo Console e o software **PuTTY**. 

Acesse a `CLI` e insira as configurações abaixo para habilitar o tunelamento SSH:

```text
Router> enable
Router# configure terminal
Router(config)# hostname Roteador_Automacao
Roteador_Automacao(config)# ip domain-name fatec.local
Roteador_Automacao(config)# username admin privilege 15 secret cisco123
Roteador_Automacao(config)# crypto key generate rsa modulus 2048
Roteador_Automacao(config)# ip ssh version 2
Roteador_Automacao(config)# line vty 0 4
Roteador_Automacao(config-line)# login local
Roteador_Automacao(config-line)# transport input ssh
Roteador_Automacao(config-line)# end
Roteador_Automacao# write memory
```

### 🧠 2. Configuração do Ambiente Python
Na máquina host (onde o script será executado), instale os pacotes e dependências necessárias através do seu terminal:

```bash
pip install netmiko python-dotenv
```

Crie um arquivo chamado **`.env`** na raiz do projeto para proteger suas credenciais. Preencha com os dados reais do seu roteador:

```env
ROUTER_HOST=192.168.1.1
ROUTER_USER=admin
ROUTER_PASS=cisco123
```

Com o ambiente pronto, inicie o software principal:
```bash
python automacao.py
```

### ⚙️ 3. Evolução para a Nuvem (GitOps)
A versão padrão deste projeto realiza o backup localmente. Se você deseja aplicar a cultura **GitOps** (onde o script faz *Push* e *Pull* dos backups automaticamente para um repositório no GitHub), realize as três alterações abaixo no código-fonte `automacao.py`:

**A. Injeção de Dependência:** Adicione a biblioteca nativa `subprocess` na primeira linha do arquivo:
```python
from netmiko import ConnectHandler, file_transfer
import re, os, datetime, glob, subprocess
```

**B. Motor de Envio (Push):** Substitua a sua função `fazer_backup()` por este bloco:
```python
def fazer_backup(sessao):
    criar_pasta_backups()
    show_run = sessao.send_command("show run")
    nome_arq = f"backups/backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arq, "w") as f: f.write(show_run)
    
    print("[+] Sincronizando com o GitHub (GitOps)...")
    try:
        subprocess.run(["git", "add", "."], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        msg_commit = f"Automacao: Backup salvo as {datetime.datetime.now().strftime('%H:%M')}"
        subprocess.run(["git", "commit", "-m", msg_commit], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push", "origin", "main"], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] SUCESSO! Backup enviado para a Nuvem.")
    except Exception:
        print("[-] Operacao Git falhou. Backup salvo apenas localmente.")
```

**C. Motor de Captura (Pull & Replace):** Substitua a sua função `restaurar_backup()` por este bloco:
```python
def restaurar_backup(sessao):
    limpar_tela()
    print("=== SISTEMA DE ROLLBACK (GITOPS) ===")
    print("\n[+] Consultando GitHub por novos backups (git pull)...")
    try:
        subprocess.run(["git", "pull", "origin", "main"], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Repositorio sincronizado com a nuvem!")
    except:
        print("[-] Falha ao alcancar a nuvem. Lendo backups locais...")

    arquivos = glob.glob("backups/backup_*.txt")
    if not arquivos: return print("[-] Nenhum backup encontrado.")
    for i, arq in enumerate(arquivos): print(f"[{i}] - {arq}")
    
    try: arquivo_alvo = arquivos[int(input("\nQual versao restaurar (ID)? "))]
    except: return print("[-] Opcao invalida.")

    print(f"\n[+] Transferindo (SCP) e Iniciando Replace Destrutivo...")
    try:
        file_transfer(sessao, source_file=arquivo_alvo, dest_file="backup_restore.txt", file_system="flash:", direction="put", overwrite_file=True)
        print(sessao.send_command_timing("configure replace flash:backup_restore.txt force"))
        sessao.send_command("write memory")
        print("\n[+] ROLLBACK CONCLUIDO!")
    except Exception as e: print("[-] Falha na transferencia SCP.")
```

<br>

---

## 🇺🇸 English

Welcome to the official manual of the Cisco Automation project. Follow the instructions below to prepare your physical router, set up the Python environment, and optionally integrate the system with the GitHub cloud (GitOps).

### 🎯 1. Day 0 Provisioning (Physical Access)
For the Python application to take network control of the router, you must perform **Day 0 Provisioning**. Physically connect to the router using a Console cable and **PuTTY**.

Access the `CLI` and insert the configurations below to enable SSH tunneling:

```text
Router> enable
Router# configure terminal
Router(config)# hostname Automation_Router
Automation_Router(config)# ip domain-name local.domain
Automation_Router(config)# username admin privilege 15 secret cisco123
Automation_Router(config)# crypto key generate rsa modulus 2048
Automation_Router(config)# ip ssh version 2
Automation_Router(config)# line vty 0 4
Automation_Router(config-line)# login local
Automation_Router(config-line)# transport input ssh
Automation_Router(config-line)# end
Automation_Router# write memory
```

### 🧠 2. Python Environment Setup
On the host machine (where the script will run), install the required packages and dependencies via terminal:

```bash
pip install netmiko python-dotenv
```

Create a file named **`.env`** in the project's root folder to protect your credentials. Fill it with your router's actual data:

```env
ROUTER_HOST=192.168.1.1
ROUTER_USER=admin
ROUTER_PASS=cisco123
```

With the environment ready, start the main software:
```bash
python automacao.py
```

### ⚙️ 3. Evolving to the Cloud (GitOps)
The standard version of this project performs local backups. If you wish to apply the **GitOps** culture (where the script automatically Pushes and Pulls backups from an isolated GitHub repository), make the following three changes to the `automacao.py` source code:

**A. Dependency Injection:** Add the native `subprocess` library to the first line of the file:
```python
from netmiko import ConnectHandler, file_transfer
import re, os, datetime, glob, subprocess
```

**B. Push Engine:** Replace your `fazer_backup()` function with this block:
```python
def fazer_backup(sessao):
    criar_pasta_backups()
    show_run = sessao.send_command("show run")
    nome_arq = f"backups/backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arq, "w") as f: f.write(show_run)
    
    print("[+] Syncing with GitHub (GitOps)...")
    try:
        subprocess.run(["git", "add", "."], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        msg_commit = f"Automation: Backup saved at {datetime.datetime.now().strftime('%H:%M')}"
        subprocess.run(["git", "commit", "-m", msg_commit], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push", "origin", "main"], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] SUCCESS! Backup pushed to the Cloud.")
    except Exception:
        print("[-] Git Operation failed. Backup saved locally only.")
```

**C. Pull & Replace Engine:** Replace your `restaurar_backup()` function with this block:
```python
def restaurar_backup(sessao):
    limpar_tela()
    print("=== ROLLBACK SYSTEM (GITOPS) ===")
    print("\n[+] Querying GitHub for new backups (git pull)...")
    try:
        subprocess.run(["git", "pull", "origin", "main"], cwd="backups", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Repository synced with the cloud!")
    except:
        print("[-] Cloud unreachable. Reading local backups...")

    arquivos = glob.glob("backups/backup_*.txt")
    if not arquivos: return print("[-] No backups found.")
    for i, arq in enumerate(arquivos): print(f"[{i}] - {arq}")
    
    try: arquivo_alvo = arquivos[int(input("\nWhich version to restore (ID)? "))]
    except: return print("[-] Invalid option.")

    print(f"\n[+] Transferring (SCP) and Initiating Destructive Replace...")
    try:
        file_transfer(sessao, source_file=arquivo_alvo, dest_file="backup_restore.txt", file_system="flash:", direction="put", overwrite_file=True)
        print(sessao.send_command_timing("configure replace flash:backup_restore.txt force"))
        sessao.send_command("write memory")
        print("\n[+] ROLLBACK COMPLETED!")
    except Exception as e: print("[-] SCP transfer failed.")
```
