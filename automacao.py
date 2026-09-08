from netmiko import ConnectHandler
import re, os, datetime, glob
from dotenv import load_dotenv

load_dotenv()

# --- HISTÓRICO DA SESSÃO (Memória RAM) ---
historico_comandos = []

def registrar_historico(acao):
    """Guarda a ação na memória apenas enquanto o programa estiver aberto"""
    hora = datetime.datetime.now().strftime('%H:%M:%S')
    historico_comandos.append(f"[{hora}] {acao}")

# --- CONFIGURAÇÕES DO ROTEADOR ---
roteador = {
    'device_type': 'cisco_ios', # Mantém isso, avisa o Python que é equipamento Cisco
    'host': os.getenv('ROUTER_HOST', '192.168.1.1'), # IP do Roteador Físico
    'username': os.getenv('ROUTER_USER', 'admin'), # Usuário criado no roteador físico
    'password': os.getenv('ROUTER_PASS', 'cisco123'), # Senha do SSH
    'secret': os.getenv('ROUTER_PASS', 'cisco123'), # Senha do comando 'enable'
    'global_delay_factor': 2 # Tempo de tolerância para redes lentas
}

# --- FUNÇÕES ÚTEIS ---
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n➡️ Pressione ENTER para continuar...")

def validar_ipv4(ip):
    """Garante que o usuário digitou os pontos do IP (Ex: 10.10.10.1)"""
    return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip) is not None

# --- TELA DE LOGIN DO SISTEMA ---
def tela_de_login():
    limpar_tela()
    print("=======================================")
    print("🔒 SISTEMA DE AUTOMAÇÃO CISCO (IaC) 🔒")
    print("=======================================")
    tentativas = 3
    while tentativas > 0:
        usuario = input("Usuário (App): ")
        senha = input("Senha (App): ")
        if usuario == "admin" and senha == "admin":
            registrar_historico("Login efetuado pelo Admin.")
            return True
        else:
            tentativas -= 1
            print(f"❌ Credenciais Inválidas! Restam {tentativas} tentativas.\n")
    print("SISTEMA BLOQUEADO.")
    return False

# --- CONEXÃO SEGURA ---
def conectar():
    limpar_tela()
    print("⏳ Conectando no Roteador (Processo SSH Seguro)...")
    try:
        sessao = ConnectHandler(**roteador)
        sessao.enable()
        print("✅ Conectado com Sucesso! (Modo Privilegiado)")
        registrar_historico(f"Sessão SSH iniciada com o host {roteador['host']}")
        pausar()
        return sessao
    except Exception as e:
        print(f"❌ Falha ao conectar.\nErro: {e}")
        return None

# --- ROTINAS DE AUTOMAÇÃO ---
def fazer_backup(sessao):
    print("\n⏳ Extraindo arquivo de configuração (show run)...")
    show_run = sessao.send_command("show run")
    nome_arq = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arq, "w") as f: f.write(show_run)
    print(f"✅ Backup salvo com o nome: {nome_arq}")
    registrar_historico("Backup de configuração extraído e salvo.")

def restaurar_backup(sessao):
    limpar_tela()
    print("=== 🔄 SISTEMA DE ROLLBACK (RESTAURAR VERSÃO) ===")
    arquivos = glob.glob("backup_*.txt")
    if not arquivos:
        print("❌ Nenhum backup encontrado no computador.")
        return
        
    for i, arq in enumerate(arquivos):
        print(f"[{i}] - {arq}")
        
    try:
        escolha = int(input("\nQual versão você deseja restaurar (Rollback)? "))
        arquivo_alvo = arquivos[escolha]
    except:
        print("❌ Opção inválida.")
        return

    print(f"\n⏳ Injetando arquivo {arquivo_alvo} no roteador...")
    sessao.send_config_from_file(arquivo_alvo)
    sessao.send_command("write memory")
    print("✅ ROLLBACK CONCLUÍDO! Configurações restauradas.")
    registrar_historico(f"Rollback executado com o arquivo: {arquivo_alvo}")

def configurar_acesso_remoto(sessao):
    limpar_tela()
    print("=== 🔐 CONFIGURAR ACESSO REMOTO (SSH/TELNET) ===")
    dominio = input("1. Nome do Domínio (Ex: fatec.com): ")
    usuario = input("2. Novo Usuário Cisco: ")
    senha = input("3. Nova Senha Cisco: ")
    
    comandos = [
        f"ip domain-name {dominio}",
        f"username {usuario} privilege 15 secret {senha}",
        "crypto key generate rsa modulus 2048",
        "line vty 0 4",
        "login local",
        "transport input ssh telnet"
    ]
    sessao.send_config_set(comandos)
    sessao.send_command("write memory")
    print("\n✅ SSH e Telnet configurados com sucesso!")
    registrar_historico("Acesso Remoto configurado no roteador.")

def gerenciar_portas(sessao):
    saida_desc = sessao.send_command("show interfaces description")
    print("\n--- STATUS DAS PORTAS ---")
    print(saida_desc)
    
    portas = re.findall(r'^(FastEthernet\S+|GigabitEthernet\S+|Serial\S+)', sessao.send_command("show ip int brief"), re.MULTILINE)
    if not portas: return

    try:
        print("\nSelecione uma porta abaixo:")
        for i, p in enumerate(portas): print(f"[{i}] - {p}")
        porta_alvo = portas[int(input("Número da porta: "))]
    except:
        print("❌ Opção inválida.")
        return

    while True:
        limpar_tela()
        print(f"=== GERENCIANDO A PORTA: {porta_alvo} ===")
        print("1. 🛠️  Configurar IP e Máscara")
        print("2. 📝 Nomear Porta (Adicionar Descrição)")
        print("3. 🟢 Ligar a porta (No Shutdown)")
        print("4. 🔴 Desligar a porta (Shutdown)")
        print("5. 🔍 Ver Configuração Detalhada (show run interface)")
        print("0. 🔙 Voltar")
        
        acao = input("\nO que deseja fazer? ")

        if acao == "1":
            ip = input("IPv4 (Ex: 192.168.10.1): ")
            mascara = input("Máscara (Ex: 255.255.255.0): ")
            if validar_ipv4(ip) and validar_ipv4(mascara):
                sessao.send_config_set([f"interface {porta_alvo}", f"ip address {ip} {mascara}"])
                print(f"✅ IP Configurado!")
                registrar_historico(f"IP {ip} atribuído a porta {porta_alvo}")
            else: print("❌ Formato de IP/Máscara inválido.")
            pausar()

        elif acao == "2":
            desc = input("Descrição (Ex: Roteador_B): ")
            sessao.send_config_set([f"interface {porta_alvo}", f"description {desc}"])
            print("✅ Descrição aplicada!")
            pausar()
        elif acao == "3":
            sessao.send_config_set([f"interface {porta_alvo}", "no shutdown"])
            print("✅ Porta ligada!"); pausar()
        elif acao == "4":
            sessao.send_config_set([f"interface {porta_alvo}", "shutdown"])
            print("✅ Porta desligada!"); pausar()
        elif acao == "5":
            print(sessao.send_command(f"show run interface {porta_alvo}"))
            pausar()
        elif acao == "0":
            sessao.send_command("write memory"); break

def painel_admin(sessao):
    while True:
        limpar_tela()
        print("=== 👑 PAINEL DE ADMINISTRAÇÃO ===")
        print("1. 🕒 Ver Histórico do App (O que foi feito agora)")
        print("2. 👥 Ver Usuários do Roteador Cisco")
        print("3. 📜 Ver Logs Nativos do Roteador (Syslog)")
        print("0. 🔙 Voltar")
        
        acao = input("\nEscolha uma auditoria: ")
        
        if acao == "1":
            print("\n--- HISTÓRICO ---")
            for item in historico_comandos: print(item)
            pausar()
        elif acao == "2":
            print("\n--- CONTAS CADASTRADAS NO ROTEADOR ---")
            print(sessao.send_command("show run | include username"))
            pausar()
        elif acao == "3":
            print("\n--- ÚLTIMOS LOGS DO ROTEADOR ---")
            print('\n'.join(sessao.send_command("show logging").split('\n')[-20:]))
            pausar()
        elif acao == "0": break

# --- MENU PRINCIPAL ---
def menu_principal():
    if not tela_de_login(): return
    sessao = conectar()
    if not sessao: return
        
    while True:
        limpar_tela()
        print("==========================================")
        print("   🤖 IA DE AUTOMAÇÃO DE REDES CISCO")
        print("==========================================")
        print("1. 🛡️  Fazer Backup do Roteador")
        print("2. 🔄 Restaurar Backup (Rollback)")
        print("3. ⚙️  Gerenciar uma Porta (IP, Ligar, Desligar)")
        print("4. 🔐 Configurar Acesso Remoto (SSH / Telnet)")
        print("5. 👑 Painel de Administração (Auditoria)")
        print("0. ❌ Sair e Desconectar")
        
        opcao = input("\nSelecione: ")
        
        if opcao == "1": fazer_backup(sessao); pausar()
        elif opcao == "2": restaurar_backup(sessao); pausar()
        elif opcao == "3": gerenciar_portas(sessao)
        elif opcao == "4": configurar_acesso_remoto(sessao); pausar()
        elif opcao == "5": painel_admin(sessao)
        elif opcao == "0":
            sessao.disconnect()
            break

if __name__ == "__main__":
    menu_principal()
