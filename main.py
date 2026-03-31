"""
OGSNIPER - Fast Edition
No boxes, pure text design
"""

import subprocess
import sys
import os

# Auto-install requirements
def install_requirements():
    """Auto-install required packages"""
    requirements = ['aiohttp']
    
    print("Checking requirements...")
    for package in requirements:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
    print("+ All requirements installed\n")

install_requirements()

import asyncio
import aiohttp
import string
import random
import time
from datetime import datetime
import json
from pathlib import Path
import platform

VERSION = "3.0"

class Colors:
    """Modern color palette"""
    RESET = '\033[0m'
    
    # Primary colors
    PRIMARY = '\033[38;5;51m'       # Cyan
    SECONDARY = '\033[38;5;33m'     # Blue
    ACCENT = '\033[38;5;123m'       # Light Cyan
    
    # Status colors
    SUCCESS = '\033[38;5;46m'       # Bright Green
    ERROR = '\033[38;5;196m'        # Red
    WARNING = '\033[38;5;226m'      # Yellow
    INFO = '\033[38;5;250m'         # Grey
    
    # Text colors
    BRIGHT = '\033[97m'
    DIM = '\033[38;5;240m'
    HIGHLIGHT = '\033[38;5;231m'
    
    # Special
    GRADIENT1 = '\033[38;5;51m'
    GRADIENT2 = '\033[38;5;45m'
    GRADIENT3 = '\033[38;5;39m'
    GRADIENT4 = '\033[38;5;33m'

C = Colors

stats = {
    'requests': 0,
    'available': 0,
    'taken': 0,
    'rps': 0,
    'session_start': None,
    'epic_found': 0
}

available_usernames = []
webhook_sent_usernames = set()
STOP = False

for path in ['logs', 'results', 'data']:
    os.makedirs(path, exist_ok=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    print(f"""
{C.GRADIENT1}   ____   ____ ____  _   _ ___ ____  _____ ____  
{C.GRADIENT2}  / __ \ / ___/ ___|| \ | |_ _|  _ \| ____|  _ \ 
{C.GRADIENT3} | |  | | |  _\___ \|  \| || || |_) |  _| | |_) |
{C.GRADIENT3} | |__| | |_| |___) | |\  || ||  __/| |___|  _ < 
{C.GRADIENT4}  \____/ \____|____/|_| \_|___|_|   |_____|_| \_\ {C.RESET}
""")
    animate(f"  {C.BRIGHT}OGSNIPER - Fast Edition v{VERSION}{C.RESET}")
    animate(f"  {C.DIM}dev: yoh{C.RESET}")
    print(f"""
  {C.PRIMARY}//////////////////////////////////////////////////{C.RESET}
""")

def print_header(text):
    """Print section header"""
    print()
    animate(f"  {C.PRIMARY}/// {C.HIGHLIGHT}{text}{C.PRIMARY} ///{C.RESET}")
    print()

def print_option(number, text, description=""):
    """Print menu option"""
    if description:
        print(f"  {C.SECONDARY}{number} »{C.RESET} {C.BRIGHT}{text}{C.RESET}")
        print(f"      {C.DIM}  {description}{C.RESET}")
    else:
        print(f"  {C.SECONDARY}{number} »{C.RESET} {C.BRIGHT}{text}{C.RESET}")

def print_generator_option(number, text, example):
    """Print generator menu option"""
    print(f"  {C.SECONDARY}{number} »{C.RESET} {C.BRIGHT}{text:<15}{C.RESET} {C.DIM}(e.g. {example}){C.RESET}")

def print_info(label, value, prefix="+"):
    """Print info line"""
    print(f"{C.INFO}{prefix}{C.RESET} {C.DIM}{label}:{C.RESET} {C.HIGHLIGHT}{value}{C.RESET}")

def print_success(text):
    """Print success message"""
    print(f"{C.SUCCESS}+{C.RESET} {text}")

def print_error(text):
    """Print error message"""
    print(f"{C.ERROR}!{C.RESET} {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{C.WARNING}!{C.RESET} {text}")

def send_desktop_notification(title, message):
    """Send desktop notification - silent errors"""
    try:
        system = platform.system()
        if system == 'Windows':
            try:
                import subprocess
                ps_script = f'''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$Template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$RawXml = [xml] $Template.GetXml()
($RawXml.toast.visual.binding.text|where {{$_.id -eq "1"}}).AppendChild($RawXml.CreateTextNode("{title}")) > $null
($RawXml.toast.visual.binding.text|where {{$_.id -eq "2"}}).AppendChild($RawXml.CreateTextNode("{message}")) > $null
$SerializedXml = New-Object Windows.Data.Xml.Dom.XmlDocument
$SerializedXml.LoadXml($RawXml.OuterXml)
$Toast = [Windows.UI.Notifications.ToastNotification]::new($SerializedXml)
$Toast.Tag = "PowerShell"
$Toast.Group = "PowerShell"
$Toast.ExpirationTime = [DateTimeOffset]::Now.AddMinutes(1)
$Notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("PowerShell")
$Notifier.Show($Toast);
'''
                subprocess.run(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script], 
                             capture_output=True, creationflags=0x08000000)
            except:
                pass
        elif system == 'Darwin':
            os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"' 2>/dev/null")
        elif system == 'Linux':
            os.system(f'notify-send "{title}" "{message}" 2>/dev/null')
    except:
        pass

class Config:
    def __init__(self):
        self.config_file = 'data/config.json'
        self.config = self.load()
    
    def load(self):
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump({}, f)
            return {}
        with open(self.config_file, 'r') as f:
            try:
                return json.load(f)
            except:
                return {}
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

# ================== GENERATOR ==================

def generate_username(char_length, pattern):
    """Generate username with various patterns"""
    
    if pattern == '1':
        username = ''.join(random.choices(string.ascii_lowercase, k=char_length))
    
    elif pattern == '2':
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=char_length))
    
    elif pattern == '3':
        if char_length % 2 != 0:
            char_length += 1
        pairs = char_length // 2
        letters = random.choices(string.ascii_lowercase, k=pairs)
        username = ''.join(letter * 2 for letter in letters)
    
    elif pattern == '4':
        chars = string.ascii_lowercase + string.digits
        main_part = ''.join(random.choices(chars, k=char_length - 1))
        username = main_part + '.'
    
    elif pattern == '5':
        if char_length < 4:
            char_length = 4
        username_parts = []
        remaining = char_length
        while remaining >= 4:
            base_char = random.choice(string.ascii_lowercase)
            username_parts.append(base_char * 3)
            different_char = random.choice(string.ascii_lowercase + string.digits)
            username_parts.append(different_char)
            remaining -= 4
        if remaining > 0:
            username_parts.append(''.join(random.choices(string.ascii_lowercase, k=remaining)))
        username = ''.join(username_parts)
    
    elif pattern == '6':
        chars = string.ascii_lowercase + string.digits
        parts = []
        remaining = char_length
        while remaining > 0:
            if remaining == 1:
                parts.append(random.choice(chars))
                remaining = 0
            else:
                parts.append(random.choice(chars))
                if remaining > 2 and random.random() < 0.4:
                    parts.append('_')
                    remaining -= 2
                else:
                    remaining -= 1
        username = ''.join(parts)[:char_length]
    
    elif pattern == '7':
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        username = ''
        for i in range(char_length):
            if i % 2 == 0:
                username += random.choice(consonants)
            else:
                username += random.choice(vowels)
    
    elif pattern == '8':
        half = char_length // 2
        first_half = ''.join(random.choices(string.ascii_lowercase, k=half))
        if char_length % 2 == 0:
            username = first_half + first_half[::-1]
        else:
            middle = random.choice(string.ascii_lowercase)
            username = first_half + middle + first_half[::-1]
    
    elif pattern == '9':
        random_pattern = random.choice(['1', '2', '3', '4', '5', '6', '7', '8'])
        username = generate_username(char_length, random_pattern)
    
    else:
        username = ''.join(random.choices(string.ascii_lowercase, k=char_length))
    
    return username

def generate_usernames(count, char_length, pattern):
    """Generate usernames - FAST version"""
    usernames = set()
    print()
    animate(f"{C.INFO}*{C.RESET} {C.DIM}Generating targets...{C.RESET}")
    print()
    
    while len(usernames) < count:
        needed = count - len(usernames)
        batch_size = min(50000, max(100, int(needed * 1.1)))
        
        batch = [generate_username(char_length, pattern) for _ in range(batch_size)]
        usernames.update(batch)
        
        current = min(len(usernames), count)
        progress = (current / count * 100)
        bar_length = 30
        filled = int(bar_length * current / count)
        bar = f"{C.SUCCESS}{'=' * filled}{C.DIM}{'-' * (bar_length - filled)}{C.RESET}"
        print(f"  {bar} {C.HIGHLIGHT}{int(progress)}%{C.RESET}", end='\r')
    
    print()
    return list(usernames)[:count]

def save_generated_usernames(usernames):
    """Save generated usernames to data folder"""
    filename = 'data/names_to_check.txt'
    
    if os.path.exists(filename):
        os.remove(filename)
        print_warning(f"Cleared old names_to_check.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        for username in usernames:
            f.write(username + '\n')
    
    print_success(f"Saved {C.HIGHLIGHT}{len(usernames):,}{C.RESET} entries to {C.DIM}{filename}{C.RESET}")
    return filename

# ================== CHECKER ==================

class APIClient:
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=15)
        self.endpoints = [
            "https://discord.com/api/v10/unique-username/username-attempt-unauthed",
            "https://discord.com/api/v9/unique-username/username-attempt-unauthed",
            "https://canary.discord.com/api/v10/unique-username/username-attempt-unauthed",
            "https://ptb.discord.com/api/v10/unique-username/username-attempt-unauthed",
        ]
        self.current_endpoint = 0
    
    def get_headers(self):
        ua = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ])
        return {
            'Content-Type': 'application/json',
            'User-Agent': ua,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/',
            'DNT': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    
    async def check(self, username, session, proxy=None):
        endpoint = self.endpoints[self.current_endpoint % len(self.endpoints)]
        self.current_endpoint += 1
        
        try:
            headers = self.get_headers()
            
            async with session.post(
                endpoint,
                json={'username': username},
                headers=headers,
                timeout=self.timeout,
                proxy=proxy
            ) as response:
                stats['requests'] += 1
                
                if response.status in [200, 201, 204]:
                    try:
                        data = await response.json()
                        taken = data.get('taken', True)
                        
                        if not taken:
                            stats['available'] += 1
                            return True
                        else:
                            stats['taken'] += 1
                            return False
                    except:
                        stats['taken'] += 1
                        return False
                
                elif response.status == 429:
                    try:
                        data = await response.json()
                        retry_after = data.get('retry_after', 2)
                    except:
                        retry_after = 2
                    await asyncio.sleep(min(retry_after, 5))
                    return None
                
                else:
                    return None
        
        except:
            return None

async def save_username(username):
    """Save username"""
    with open('results/hits.txt', 'a', encoding='utf-8') as f:
        f.write(f"{username}\n")
    
    session_file = 'data/webhook_sent.txt'
    if username.lower() not in webhook_sent_usernames:
        with open(session_file, 'a', encoding='utf-8') as f:
            f.write(f"{username.lower()}\n")

async def send_webhook(username, webhook_url):
    """Send webhook"""
    try:
        if not webhook_url or username.lower() in webhook_sent_usernames:
            return
        
        webhook_sent_usernames.add(username.lower())
        
        payload = {
            'embeds': [{
                'description': f'**{username}**',
                'color': 0x33CCFF,
                'footer': {'text': 'OGSNIPER'}
            }]
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(webhook_url, json=payload, timeout=aiohttp.ClientTimeout(total=5))
    except:
        pass

async def worker(queue, api_client, session, longest, proxies, proxy_index, config):
    while not queue.empty() and not STOP:
        try:
            username = await queue.get()
            
            max_retries = 3
            result = None
            
            for attempt in range(max_retries):
                proxy = None
                if proxies:
                    proxy = proxies[proxy_index[0] % len(proxies)]
                    proxy_index[0] += 1
                    if not proxy.startswith('http'):
                        proxy = f'http://{proxy}'
                
                result = await api_client.check(username, session, proxy)
                
                if result is not None:
                    break
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
            
            if result is True:
                print(f"\n  {C.SUCCESS}Valid{C.RESET} {C.DIM}»{C.RESET} {C.SUCCESS}{username:<{longest}}{C.RESET} {C.DIM}({stats['rps']} r/s){C.RESET}")
                available_usernames.append(username)
                await save_username(username)
                
                webhook_url = config.get('webhook')
                if webhook_url:
                    await send_webhook(username, webhook_url)
                
                if len(username) == 4 and username.isalpha() and config.get('desktop_notifications', False):
                    stats['epic_found'] += 1
                    send_desktop_notification("OGSNIPER HIT!", f"{username}")
            elif result is False:
                print(f"  {C.ERROR}Taken{C.RESET} {C.DIM}»{C.RESET} {C.DIM}{username:<{longest}}{C.RESET} {C.DIM}({stats['rps']} r/s){C.RESET}", end='\r')
            else:
                print(f"  {C.WARNING}Error{C.RESET} {C.DIM}»{C.RESET} {C.DIM}{username:<{longest}}{C.RESET} {C.DIM}({stats['rps']} r/s){C.RESET}", end='\r')
            
            queue.task_done()
        except:
            queue.task_done()

async def rps_calculator():
    last = 0
    while not STOP:
        await asyncio.sleep(1)
        current = stats['requests']
        stats['rps'] = current - last
        last = current

async def title_updater():
    while not STOP:
        try:
            if os.name == 'nt':
                title = f'Hits: {stats["available"]} | Epic 4-char: {stats["epic_found"]}'
                import ctypes
                ctypes.windll.kernel32.SetConsoleTitleW(title)
            else:
                sys.stdout.write(f'\33]0;Hits: {stats["available"]} | Epic 4-char: {stats["epic_found"]}\a')
                sys.stdout.flush()
        except:
            pass
        await asyncio.sleep(0.5)

async def run_checker(config):
    """Run the checker"""
    global STOP, webhook_sent_usernames
    
    api_client = APIClient()
    
    webhook_cache_file = 'data/webhook_sent.txt'
    if os.path.exists(webhook_cache_file):
        with open(webhook_cache_file, 'r', encoding='utf-8') as f:
            webhook_sent_usernames = set(line.strip().lower() for line in f if line.strip())
        if webhook_sent_usernames:
            print_info("Webhook cache loaded", f"{len(webhook_sent_usernames)} entries", "*")
    
    username_file = 'data/names_to_check.txt'
    if not os.path.exists(username_file):
        print_error("No names_to_check.txt found! Generate usernames first.")
        return
    
    with open(username_file, 'r', encoding='utf-8') as f:
        usernames = [line.strip() for line in f if line.strip()]
    
    if not usernames:
        print_error("names_to_check.txt is empty!")
        return
    
    proxy_file = 'data/proxies.txt'
    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print_info("Targets loaded", f"{len(usernames):,}", "+")
    if proxies:
        print_info("Proxies loaded", f"{len(proxies):,}", "+")
    else:
        print_warning("No proxies found! Your IP will be exposed!")
        confirm = input(f"\n{C.BRIGHT}Continue? {C.DIM}(y/N):{C.RESET} ").strip().lower()
        if confirm != 'y':
            return
    
    if proxies:
        recommended = min(len(proxies) // 2, 100)
    else:
        recommended = 10
    
    print(f"\n{C.BRIGHT}Threads {C.DIM}(recommended: {recommended}):{C.RESET} ", end='')
    threads_input = input().strip()
    workers_count = int(threads_input) if threads_input else recommended
    
    if not config.get('configured'):
        print(f"\n{C.BRIGHT}Webhook URL {C.DIM}(optional):{C.RESET} ", end='')
        webhook = input().strip()
        if webhook:
            config.set('webhook', webhook)
        config.set('configured', True)
    
    if not config.get('desktop_notifications_configured'):
        print(f"{C.BRIGHT}Enable notifications for 4-letter alpha? {C.DIM}(y/N):{C.RESET} ", end='')
        notif_choice = input().strip().lower()
        config.set('desktop_notifications', notif_choice == 'y')
        config.set('desktop_notifications_configured', True)
    
    print()
    animate(f"{C.SUCCESS}+{C.RESET} {C.BRIGHT}Starting checker...{C.RESET}")
    print()
    
    queue = asyncio.Queue()
    for u in usernames:
        await queue.put(u)
    
    longest = max(len(u) for u in usernames) if usernames else 10
    
    asyncio.create_task(rps_calculator())
    asyncio.create_task(title_updater())
    
    stats['session_start'] = time.time()
    
    connector = aiohttp.TCPConnector(limit=workers_count * 2, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        proxy_index = [0]
        
        for _ in range(workers_count):
            task = asyncio.create_task(worker(queue, api_client, session, longest, proxies, proxy_index, config))
            tasks.append(task)
        
        try:
            await queue.join()
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
        except KeyboardInterrupt:
            STOP = True
    
    elapsed = time.time() - stats['session_start']
    
    print(f"\n")
    print_header("RESULTS")
    
    print_info("Total Requests", f"{stats['requests']:,}")
    print_info("Hits", f"{stats['available']:,}")
    if stats['epic_found'] > 0:
        print_info("4-Letter Alpha", f"{stats['epic_found']:,}", "*")
    print_info("Taken", f"{stats['taken']:,}")
    print_info("Duration", f"{int(elapsed)}s")
    
    if stats['available'] > 0:
        print(f"\n{C.SUCCESS}HITS:{C.RESET}\n")
        for u in available_usernames[:10]:
            print(f"  {C.SUCCESS}• {u}{C.RESET}")
        if len(available_usernames) > 10:
            remaining = len(available_usernames) - 10
            print(f"  {C.DIM}... and {remaining} more{C.RESET}")
        print(f"\n{C.INFO}+{C.RESET} Saved to {C.HIGHLIGHT}results/hits.txt{C.RESET}")

# ================== MAIN ==================

def main():
    clear()
    banner()
    
    config = Config()
    
    print_header("MAIN MENU")
    
    print_option("1", "Generator", "Generate target list")
    print_option("2", "Checker", "Start checking session")
    print_option("3", "Auto-Run", "Gen & Check workflow")
    
    print()
    
    choice = input(f"{C.BRIGHT}Select option{C.RESET} {C.PRIMARY}›{C.RESET} ").strip()
    
    if choice == '1':
        print_header("GENERATOR MODE")
        
        print_generator_option("1", "Alpha", "abc, xyz")
        print_generator_option("2", "Alphanumeric", "a1b2, xyz9")
        print_generator_option("3", "Doubles", "vvss, ddff")
        print_generator_option("4", "Dot", "akk., wia.")
        print_generator_option("5", "Triples", "aaae, bbbx")
        print_generator_option("6", "Underscore", "a_b_c, x_y")
        print_generator_option("7", "Vowels", "baki, zito")
        print_generator_option("8", "Palindrome", "abccba, xyzzyx")
        print(f"  {C.ACCENT}9 »{C.RESET} {C.BRIGHT}{'Random':<15}{C.RESET} {C.WARNING}* Recommended{C.RESET}")
        
        print()
        
        pattern = input(f"{C.BRIGHT}Pattern{C.RESET} {C.PRIMARY}›{C.RESET} ").strip() or '1'
        
        try:
            char_length = int(input(f"{C.BRIGHT}Length (2-32){C.RESET} {C.PRIMARY}›{C.RESET} ").strip())
            count = int(input(f"{C.BRIGHT}Count (1-10,000,000){C.RESET} {C.PRIMARY}›{C.RESET} ").strip())
        except:
            print_error("Invalid input")
            return
        
        usernames = generate_usernames(count, char_length, pattern)
        save_generated_usernames(usernames)
        
        print(f"\n{C.HIGHLIGHT}PREVIEW (First 10):{C.RESET}\n")
        for i, u in enumerate(usernames[:10], 1):
            print(f"  {C.DIM}{i:2}.{C.RESET} {C.ACCENT}{u}{C.RESET}")
        
        input(f"\n{C.DIM}Press Enter to exit...{C.RESET}")
    
    elif choice == '2':
        asyncio.run(run_checker(config))
        
        print(f"\n{C.PRIMARY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}")
        print(f"{C.DIM}OGSNIPER v{VERSION}{C.RESET}")
        print(f"{C.PRIMARY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}\n")
        
        input(f"{C.DIM}Press Enter to exit...{C.RESET}")
    
    elif choice == '3':
        print_header("GENERATOR MODE")
        
        print_generator_option("1", "Alpha", "abc, xyz")
        print_generator_option("2", "Alphanumeric", "a1b2, xyz9")
        print_generator_option("3", "Doubles", "vvss, ddff")
        print_generator_option("4", "Dot", "akk., wia.")
        print_generator_option("5", "Triples", "aaae, bbbx")
        print_generator_option("6", "Underscore", "a_b_c, x_y")
        print_generator_option("7", "Vowels", "baki, zito")
        print_generator_option("8", "Palindrome", "abccba, xyzzyx")
        print(f"  {C.ACCENT}9 »{C.RESET} {C.BRIGHT}{'Random':<15}{C.RESET} {C.WARNING}* Recommended{C.RESET}")
        
        print()
        
        pattern = input(f"{C.BRIGHT}Pattern{C.RESET} {C.PRIMARY}›{C.RESET} ").strip() or '1'
        
        try:
            char_length = int(input(f"{C.BRIGHT}Length (2-32){C.RESET} {C.PRIMARY}›{C.RESET} ").strip())
            count = int(input(f"{C.BRIGHT}Count (1-10,000,000){C.RESET} {C.PRIMARY}›{C.RESET} ").strip())
        except:
            print_error("Invalid input")
            return
        
        usernames = generate_usernames(count, char_length, pattern)
        save_generated_usernames(usernames)
        
        print(f"\n{C.SUCCESS}+{C.RESET} {C.BRIGHT}Generation complete!{C.RESET}")
        print(f"{C.WARNING}!{C.RESET} {C.DIM}Checker starting in 3 seconds...{C.RESET}\n")
        
        import time
        time.sleep(3)
        
        asyncio.run(run_checker(config))
        
        print(f"\n{C.PRIMARY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}")
        print(f"{C.DIM}OGSNIPER v{VERSION}{C.RESET}")
        print(f"{C.PRIMARY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}\n")
        
        input(f"{C.DIM}Press Enter to exit...{C.RESET}")
    
    else:
        print_error("Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.ERROR}!{C.RESET} {C.DIM}Stopped by user{C.RESET}")
    except Exception as e:
        print(f"\n{C.ERROR}Error: {e}{C.RESET}")