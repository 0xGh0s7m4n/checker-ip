import sys
from pwn import log
import socket
from termcolor import colored
import signal
import subprocess
import os

# banner
banner = """
              +-+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+-+
              |H|a|c|k|i|n|g| |T|o|o|l|s| |b|y| |0|x|G|h|0|s|7|m|4|n|
              +-+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+-+

"""

def print_with_lolcat(text):
    process = subprocess.Popen(['lolcat'], stdin=subprocess.PIPE, text=True)
    process.communicate(text)

print_with_lolcat(banner)

def def_handler(sig, frame):
    print_with_lolcat("\n\n[!] Exit...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def check_ip(ip):
    try:
        socket.setdefaulttimeout(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 80))
        return True
    except Exception:
        return False

def main():
    if len(sys.argv) < 2:
        print_with_lolcat("Usage1: python3 script.py IP")
        print_with_lolcat("Usage2: python3 script.py /path/to/ips.txt")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    p1 = log.progress(colored("Check IP", 'green'))
    p1.status("Starting process ")
    ips = []

    if os.path.isfile(arg):
       
        try:
            with open(arg, 'r') as file:
                ips = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print_with_lolcat(f"file {arg} not found")
            sys.exit(1)
        except IOError as e:
            print_with_lolcat(f"Error read to file {arg}: {e}")
            sys.exit(1)
    else:
     
        if not is_valid_ip(arg):
            print_with_lolcat(f"{arg} is not a valid file")
            sys.exit(1)
        ips = [arg]

    up_count = 0
    down_count = 0
    
    for ip in ips:
        p1.status(colored(f"{ip}", 'yellow'))
        if check_ip(ip):
            print(colored(f"[+] {ip} is alive 🟢",'green'))
            up_count += 1
        else:
            print(colored(f"[-] {ip} is dead 🔴",'red'))
            down_count += 1
    
    print(colored("\n[*] Process finished:",'yellow'))
    print(colored(f"[+] IP addresses in alive: {up_count}", 'green'))
    print(colored(f"[-] IP addresses in dead: {down_count}",'red'))
    print(colored("[☯︎] Done!",'cyan'))

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

if __name__ == "__main__":
    main()
