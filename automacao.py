from netmiko import ConnectHandler, file_transfer
import re, os, datetime, glob
from dotenv import load_dotenv

load_dotenv()

# --- HISTORICO DA SESSAO (Memoria RAM) ---
historico_comandos = []

def registrar_historico(acao):
    hora = datetime.datetime.now().strftime('%H:%M:%S')
    historico_comandos.append(f"[{hora}] {acao}")

# --- CONFIGURACOES DO ROTEADOR ---
roteador = {
    'device_type': 'cisco_ios',
    'host': os.getenv('ROUTER_HOST', '192.168.1.1'),
    'username': os.getenv('ROUTER_USER', 'admin'),      
    'password': os.getenv('ROUTER_PASS', 'cisco123'), 
    'secret': os.getenv('ROUTER_PASS', 'cisco123'),   
    'global_delay_factor': 2
}

# --- FUNCOES UTEIS ---
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n[ Pressione ENTER para continuar ]")

def validar_ipv4(ip):
    return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip) is not None

def criar_pasta_backups():
    if not os.path.exists('backups'):
        os.makedirs('backups')

# --- TELA DE LOGIN DO SISTEMA ---
def tela_de_login():
    limpar_tela()
    print("=======================================")
    print("  SISTEMA DE AUTOMACAO CISCO (IaC)     ")
    print("=======================================")
    tentativas = 3
    while tentativas > 0:
        usuario = input("Usuario (App): ")
        senha = input("Senha (App): ")
        if usuario == "admin" and senha == "admin":
            registrar_historico("Login efetuado pelo Admin.")
            return True
        else:
            tentativas -= 1
            print(f"[!] Credenciais Invalidas! Restam {tentativas} tentativas.\n")
    print("SISTEMA BLOQUEADO.")
    return False

# --- CONEXAO SEGURA E PREPARACAO SCP ---
def conectar():
    limpar_tela()
    print("[+] Conectando no Roteador (Processo SSH Seguro)...")
    try:
        sessao = ConnectHandler(**roteador)
        sessao.enable()
        
        # Ativa o servidor de arquivos no roteador para o Rollback
        sessao.send_config_set(["ip scp server enable"])
        
        print("[+] Conectado com Sucesso e Transferencia SCP habilitada!")
        registrar_historico(f"Sessao SSH iniciada com o host {roteador['host']}")
        pausar()
        return sessao
    except Exception as e:
        print(f"[-] Falha ao conectar.\nErro: {e}")
        return None

# --- BACKUP E ROLLBACK DESTRUTIVO ---
def fazer_backup(sessao):
    criar_pasta_backups()
    print("\n[+] Extraindo arquivo de configuracao (show run)...")
    show_run = sessao.send_command("show run")
    nome_arq = f"backups/backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arq, "w") as f: 
        f.write(show_run)
    print(f"[+] Backup salvo com sucesso em: {nome_arq}")
    registrar_historico(f"Backup de configuracao salvo: {nome_arq}")

def restaurar_backup(sessao):
    limpar_tela()
    print("=== SISTEMA DE ROLLBACK (REPLACE TOTAL) ===")
    arquivos = glob.glob("backups/backup_*.txt")
    if not arquivos:
        print("[-] Nenhum backup encontrado na pasta 'backups'.")
        return
        
    for i, arq in enumerate(arquivos):
        print(f"[{i}] - {arq}")
        
    try:
        escolha = int(input("\nQual versao deseja restaurar (ID)? "))
        arquivo_alvo = arquivos[escolha]
    except:
        print("[-] Opcao invalida.")
        return

    print(f"\n[+] Transferindo '{arquivo_alvo}' para o HD interno do Roteador (flash:)...")
    try:
        transferencia = file_transfer(
            sessao, source_file=arquivo_alvo, dest_file="backup_restore.txt",
            file_system="flash:", direction="put", overwrite_file=True
        )
        print("[+] Arquivo transferido! Iniciando Substituicao Destrutiva (Replace)...")
        # Substituicao oficial: Apaga configuracoes nao existentes no backup
        saida_replace = sessao.send_command_timing("configure replace flash:backup_restore.txt force")
        print(saida_replace)
        sessao.send_command("write memory")
        print("\n[+] ROLLBACK CONCLUIDO! Roteador revertido exatamente ao estado do arquivo.")
        registrar_historico(f"Rollback executado com arquivo: {arquivo_alvo}")
    except Exception as e:
        print(f"\n[-] Falha na transferencia do arquivo SCP.\nErro: {e}")

# --- GERENCIAMENTO DO ROTEADOR ---
def mudar_hostname(sessao):
    limpar_tela()
    print("=== RENOMEAR ROTEADOR ===")
    novo_nome = input("Digite o novo Hostname: ")
    sessao.send_config_set([f"hostname {novo_nome}"])
    sessao.send_command("write memory")
    print(f"[+] O nome do roteador agora e: {novo_nome}")
    registrar_historico(f"Hostname alterado para {novo_nome}")

def gerenciar_portas(sessao):
    limpar_tela()
    print("=== STATUS DAS PORTAS ===")
    print(sessao.send_command("show interfaces description"))
    
    portas_brutas = sessao.send_command("show ip int brief")
    portas = re.findall(r'^(FastEthernet\S+|GigabitEthernet\S+|Serial\S+)', portas_brutas, re.MULTILINE)
    if not portas: 
        print("[-] Nenhuma porta encontrada.")
        return

    print("\n--- SELECIONE UMA PORTA PARA CONFIGURAR ---")
    for i, p in enumerate(portas): 
        print(f"[{i}] - {p}")
        
    try:
        porta_alvo = portas[int(input("\nDigite o ID da porta: "))]
    except:
        print("[-] Opcao invalida.")
        return

    while True:
        limpar_tela()
        print(f"=== GERENCIANDO A PORTA: {porta_alvo} ===")
        print("1. Configurar IP e Mascara")
        print("2. Nomear Porta (Description)")
        print("3. Ligar a porta (No Shutdown)")
        print("4. Desligar a porta (Shutdown)")
        print("5. Ver Configuracao Detalhada")
        if "Serial" in porta_alvo:
            print("6. Configurar Clock Rate")
        print("0. Voltar")
        
        acao = input("\nEscolha uma opcao: ")

        if acao == "1":
            ip = input("IPv4 (Ex: 192.168.10.1): ")
            mascara = input("Mascara (Ex: 255.255.255.0): ")
            if validar_ipv4(ip) and validar_ipv4(mascara):
                sessao.send_config_set([f"interface {porta_alvo}", f"ip address {ip} {mascara}"])
                print("[+] IP Configurado com sucesso!")
                registrar_historico(f"IP {ip} atribuido a porta {porta_alvo}")
            else: print("[-] Formato invalido."); pausar()
        elif acao == "2":
            desc = input("Descricao (Ex: Roteador_B): ")
            sessao.send_config_set([f"interface {porta_alvo}", f"description {desc}"])
            print("[+] Descricao aplicada!"); pausar()
        elif acao == "3":
            sessao.send_config_set([f"interface {porta_alvo}", "no shutdown"])
            print("[+] Porta ligada!"); pausar()
        elif acao == "4":
            sessao.send_config_set([f"interface {porta_alvo}", "shutdown"])
            print("[+] Porta desligada!"); pausar()
        elif acao == "5":
            print("\n--- DETALHES DA PORTA ---")
            print(sessao.send_command(f"show run interface {porta_alvo}")); pausar()
        elif acao == "6" and "Serial" in porta_alvo:
            clock = input("Valor do Clock Rate (Ex: 64000): ")
            sessao.send_config_set([f"interface {porta_alvo}", f"clock rate {clock}"])
            print(f"[+] Clock rate definido para {clock}"); pausar()
        elif acao == "0":
            sessao.send_command("write memory")
            break

# --- MENU DE SEGURANCA ---
def menu_seguranca(sessao):
    while True:
        limpar_tela()
        print("=== CONTROLE DE SEGURANCA E USUARIOS ===")
        print("1. Adicionar novo Usuario Cisco")
        print("2. Excluir um Usuario Cisco")
        print("3. Configurar Permissoes de Acesso (SSH ou Telnet)")
        print("0. Voltar")
        
        acao = input("\nEscolha uma opcao: ")
        
        if acao == "1":
            usuario = input("Novo Usuario: ")
            senha = input("Nova Senha: ")
            sessao.send_config_set([f"username {usuario} privilege 15 secret {senha}"])
            sessao.send_command("write memory")
            print(f"[+] Usuario {usuario} criado com sucesso.")
            registrar_historico(f"Usuario {usuario} adicionado ao roteador.")
            pausar()
            
        elif acao == "2":
            print("\n--- USUARIOS ATUAIS NO ROTEADOR ---")
            print(sessao.send_command("show run | include username"))
            usuario = input("\nDigite o nome exato do usuario para DELETAR: ")
            sessao.send_config_set([f"no username {usuario}"])
            sessao.send_command("write memory")
            print(f"[+] Usuario {usuario} apagado do banco de dados.")
            registrar_historico(f"Usuario {usuario} deletado.")
            pausar()
            
        elif acao == "3":
            print("\nQual protocolo deseja PERMITIR para acesso remoto no Roteador?")
            print("1 - Permitir Apenas SSH (Altamente Recomendado)")
            print("2 - Permitir Apenas Telnet (Ambientes de Teste)")
            escolha = input("Opcao: ")
            
            if escolha == "1":
                dominio = input("Dominio RSA (Ex: fatec.com): ")
                sessao.send_config_set([
                    f"ip domain-name {dominio}", 
                    "crypto key generate rsa modulus 2048", 
                    "line vty 0 4", "login local", "transport input ssh"
                ])
                print("[+] Acesso restrito para SSH!")
                registrar_historico("Linhas VTY restritas para protocolo SSH.")
            elif escolha == "2":
                sessao.send_config_set(["line vty 0 4", "login local", "transport input telnet"])
                print("[+] Acesso restrito para Telnet!")
                registrar_historico("Linhas VTY configuradas para Telnet.")
            else:
                print("[-] Opcao invalida.")
            sessao.send_command("write memory")
            pausar()
        elif acao == "0":
            break

# --- PAINEL ADMIN ---
def painel_admin(sessao):
    while True:
        limpar_tela()
        print("=== PAINEL DE AUDITORIA ===")
        print("1. Ver Historico do App (Sessao Atual)")
        print("2. Ver Usuarios do Roteador (show users)")
        print("3. Ver Logs Nativos do Roteador (show logging)")
        print("0. Voltar")
        
        acao = input("\nEscolha a auditoria: ")
        
        if acao == "1":
            print("\n--- HISTORICO (MEMORIA RAM) ---")
            for item in historico_comandos: print(item)
            pausar()
        elif acao == "2":
            print("\n--- USUARIOS CONECTADOS AGORA ---")
            print(sessao.send_command("show users"))
            print("\n--- CONTAS CADASTRADAS NO SISTEMA ---")
            print(sessao.send_command("show run | include username"))
            pausar()
        elif acao == "3":
            print("\n--- ULTIMOS LOGS DO ROUTER ---")
            print('\n'.join(sessao.send_command("show logging").split('\n')[-20:]))
            pausar()
        elif acao == "0": 
            break

# --- MENU PRINCIPAL ---
def menu_principal():
    if not tela_de_login(): return
    sessao = conectar()
    if not sessao: return
        
    while True:
        limpar_tela()
        print("==========================================")
        print("       AUTOMACAO DE REDES CISCO           ")
        print("==========================================")
        print("1. Gerenciar Portas (IP, Ligar, Clock Rate)")
        print("2. Fazer Backup (Salvar config na pasta)")
        print("3. Rollback (Substituicao Definitiva)")
        print("4. Seguranca (Usuarios, Telnet/SSH)")
        print("5. Renomear Roteador (Hostname)")
        print("6. Auditoria (Logs e Historico)")
        print("0. Sair e Desconectar")
        
        opcao = input("\nSelecione a opcao: ")
        
        if opcao == "1": gerenciar_portas(sessao)
        elif opcao == "2": fazer_backup(sessao); pausar()
        elif opcao == "3": restaurar_backup(sessao); pausar()
        elif opcao == "4": menu_seguranca(sessao)
        elif opcao == "5": mudar_hostname(sessao); pausar()
        elif opcao == "6": painel_admin(sessao)
        elif opcao == "0":
            print("\n[+] Encerrando sessao com o roteador. Ate a proxima!")
            sessao.disconnect()
            break

if __name__ == "__main__":
    menu_principal()
