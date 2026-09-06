from netmiko import ConnectHandler
import re
import datetime
import os

# --- CONFIGURAÇÕES DO ROTEADOR ---
roteador = {
    'device_type': 'cisco_ios',
    'host': 'IP_DO_ROTEADOR',
    'username': 'SEU_USUARIO',      
    'password': 'SUA_SENHA', 
    'secret': 'SUA_SENHA',   
    'global_delay_factor': 2
}
# --- FUNÇÕES DE INTERFACE ---
def limpar_tela():
    """Limpa o terminal (funciona no Windows e no Linux/Mac)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa a tela até o usuário apertar Enter"""
    input("\n➡️  Pressione ENTER para continuar...")

# --- FUNÇÕES DO SISTEMA ---
def conectar():
    limpar_tela()
    print("====================================================")
    print("⏳ Conectando no Data Center da Cisco (DevNet Sandbox)...")
    print("====================================================\n")
    try:
        sessao = ConnectHandler(**roteador)
        sessao.enable()
        print("✅ Acesso Liberado! Você está dentro do Roteador.")
        pausar()
        return sessao
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def fazer_backup(sessao):
    print("\n⏳ Gerando Backup das configurações da Cisco...")
    show_run = sessao.send_command("show run")
    nome_arquivo = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arquivo, "w") as f:
        f.write(show_run)
    print(f"✅ Backup salvo com sucesso no arquivo: {nome_arquivo}")

def ver_portas(sessao):
    print("\n--- PORTAS DO ROTEADOR ---")
    saida = sessao.send_command("show ip interface brief")
    
    portas = re.findall(r'^(FastEthernet\S+|GigabitEthernet\S+|Serial\S+)', saida, re.MULTILINE)
    
    for numero, porta in enumerate(portas):
        detalhes = sessao.send_command(f"show interfaces {porta} | include Description")
        texto_descricao = ""
        if "Description:" in detalhes:
            texto_descricao = "-> " + detalhes.strip()
            
        print(f"[{numero}] - {porta} {texto_descricao}")
        
    print("--------------------------")
    return portas

def configurar_porta(sessao):
    portas_disponiveis = ver_portas(sessao)
    
    try:
        escolha = int(input("\nQual NÚMERO da interface deseja configurar? "))
        interface_alvo = portas_disponiveis[escolha]
    except (ValueError, IndexError):
        print("❌ Número inválido!")
        return

    ip = input(f"Digite o IP para a porta {interface_alvo}: ")
    mascara = input("Digite a Máscara: ")
    descricao = input("Deseja colocar um Nome/Descrição na porta? (Se não, dê Enter): ")

    comandos = [
        f"interface {interface_alvo}",
        f"ip address {ip} {mascara}",
        "no shutdown"
    ]
    
    if descricao != "":
        comandos.append(f"description {descricao}")
        
    if "Serial" in interface_alvo:
        comandos.append("clock rate 64000")
        
    print("\n🚀 Enviando configurações pela internet...")
    sessao.send_config_set(comandos)
    sessao.send_command("write memory")
    print("✅ Configuração Aplicada no roteador!")

def aplicar_template(sessao):
    print("\n--- APLICAR ARQUIVO DE CONFIGURAÇÃO (GOLDEN CONFIG) ---")
    arquivo = input("Digite o nome do arquivo txt (ex: config.txt): ")
    
    try:
        print(f"⏳ Injetando no roteador...")
        resultado = sessao.send_config_from_file(arquivo)
        print("✅ Aplicado com sucesso!\n")
        print("--- Log do Servidor ---")
        print(resultado)
        sessao.send_command("write memory")
        
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo '{arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

# --- MOTOR DO PROGRAMA (MENU INTERATIVO) ---
def menu_principal():
    sessao = conectar()
    if sessao is None:
        return
        
    while True:
        limpar_tela()
        print("==========================================")
        print("   🤖 SISTEMA DE AUTOMAÇÃO CLOUD CISCO")
        print("==========================================")
        print("1. 🛡️  Fazer Backup do Roteador")
        print("2. 👁️  Ver Portas e Status")
        print("3. ⚙️  Configurar uma Porta")
        print("4. 📥 Aplicar Configuração Padrão (.txt)")
        print("5. ❌ Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            fazer_backup(sessao)
            pausar()
        elif opcao == "2":
            ver_portas(sessao)
            pausar()
        elif opcao == "3":
            configurar_porta(sessao)
            pausar()
        elif opcao == "4":
            aplicar_template(sessao)
            pausar()
        elif opcao == "5":
            print("\nDesconectando do Servidor da Cisco... Tchau!")
            sessao.disconnect()
            break
        else:
            print("❌ Opção Inválida! Tente de novo.")
            pausar()

if __name__ == "__main__":
    menu_principal()