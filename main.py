import string
import time
import sys
import numpy as np
import psutil
import itertools
from password import PASSWORD  # Import the password from password.py

locate_erorr = "ERROR CODE: F927NG"
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[8m"
STRIKETHROUGH = "\033[9m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

def slow_print(text, delay=0.008):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

slow_print(f"{BOLD}{GREEN}Project 12{RESET}\n")
time.sleep(0.1)
slow_print(
    f"{GREEN}Project 12 is a top-secret operation that hacks passwords. It completely utilizes your PC to quote-on-quote, guess a password. It is very powerful and is kept secret because of this.{RESET}\n"
)
time.sleep(0.1)
print()
slow_print(f"{BOLD}{GREEN}Specs:{RESET}\n")
slow_print(f"{GREEN}Programming Language: Python 3.13{RESET}\n")
slow_print(f"{GREEN}Author: Bogdan Zogovic{RESET}\n")
slow_print(
    f"{GREEN}Libraries: itertools, string, concurrent.futures, numpy, psutil{RESET}\n"
)
slow_print(
    f"{GREEN}Parallelism: Uses ProcessPoolExecutor for efficient parallel processing across CPU cores.{RESET}\n"
)
time.sleep(0.1)
print()
slow_print(f"{RED}{BOLD}DISCLAIMERS:{RESET}\n")
slow_print(
    f"{RED}This tool is intended for educational and personal use only. It is powerful and should not be used for malicious purposes. Use it responsibly and never attempt to gain unauthorized access to accounts or systems. By using this tool, you assume all responsibility for its usage. The creator is not liable for any consequences or damages resulting from its use.{RESET}\n"
)
print()

# Removed the old password checking logic and added the new one below
def ask_for_password():
    entered_password = input(f"{BOLD}{GREEN}Enter the password to continue: {RESET}")
    if entered_password == PASSWORD:
        print()
        print(f"{GREEN}Password correct.{RESET}")
    else:
        print(f"{RED}Incorrect password. Exiting...{RESET}")
        sys.exit(1)  # Exit the program if the password is incorrect

def get_charset():
    while True:
        print()
        print()
        print()
        print()
        print("\nSelect character set:")
        print("1. Numbers only")
        print("2. Lowercase letters only")
        print("3. Uppercase letters only")
        print("4. Uppercase + Lowercase + Numbers")
        print("5. Uppercase + Lowercase + Numbers + Symbols")
        print("6. Lowercase + Numbers")
        print("7. Uppercase + Numbers")
        choice = input("Enter choice (1-7): ").strip()
        if choice == '1':
            return list(string.digits)
        elif choice == '2':
            return list(string.ascii_lowercase)
        elif choice == '3':
            return list(string.ascii_uppercase)
        elif choice == '4':
            return list(string.ascii_letters + string.digits)
        elif choice == '5':
            return list(string.ascii_letters + string.digits + string.punctuation)
        elif choice == '6':
            return list(string.ascii_lowercase + string.digits)
        elif choice == '7':
            return list(string.ascii_uppercase + string.digits)
        else:
            print("Invalid choice. Please try again.\n")

def show_progress_bar(iteration, total, length=40):
    progress = int((iteration / total) * length)
    sys.stdout.write("\r[" + "=" * progress + " " * (length - progress) +
                     "] " + f"{iteration}/{total}")
    sys.stdout.flush()

def show_status(cpu, ram, sent, recv, guess):
    sys.stdout.write(
        f"\rCPU: {cpu:.1f}% | RAM: {ram:.1f}% | ↑ {sent:.2f} MB ↓ {recv:.2f} MB | Guessing: {guess:<20}"
    )
    sys.stdout.flush()

def brute_force():
    charset = get_charset()
    target_password = input("Enter the password to brute-force: ").strip()
    length = len(target_password)
    start_time = time.time()
    guess_counter = 0
    last_display = time.time()
    net_old = psutil.net_io_counters()
    for combo in itertools.product(charset, repeat=length):
        guess = ''.join(combo)
        guess_counter += 1
        if time.time() - last_display >= 1:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            net_new = psutil.net_io_counters()
            sent_speed = (net_new.bytes_sent - net_old.bytes_sent) / 1e6
            recv_speed = (net_new.bytes_recv - net_old.bytes_recv) / 1e6
            net_old = net_new
            last_display = time.time()
            show_status(cpu, ram, sent_speed, recv_speed, guess)
        if guess == target_password:
            print(
                f"\nFound it! '{guess}' in {guess_counter} tries and {time.time() - start_time:.2f} seconds."
            )
            return
    print(f"""\nERROR CODE: F927NG
    Could not locate your set of numbers in the given command. Please enter your combination in accordance to what you chose.""")

# Ask for the password once at the beginning
ask_for_password()  
while True:
    print("Booting:")
    total_steps = 100
    for i in range(total_steps):
        show_progress_bar(i + 1, total_steps)
        time.sleep(0.005)
    print("\n")
    brute_force()
    again = input(f"{BOLD}{GREEN}Do you want to try again or exit? ( type: Y/N): {RESET}").strip().lower()
    if again != 'y':
        print(f"{GREEN}Exiting...{RESET}")
        break
