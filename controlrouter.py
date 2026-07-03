#!/usr/bin/env python3
# ============================================================
#   ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗   ██╗████████╗███████╗██████╗ 
#  ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
#  ██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██████╔╝
#  ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
#  ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
#   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
#                                                                                         
#  CONTROLROUTER v1.0 - ULTIMATE EDITION
#  Create by vikk official
#  "Control your network, control your world." 🔥
# ============================================================

import os
import sys
import time
import json
import subprocess
import re
import threading
import signal
from datetime import datetime

# ============================================================
#  🎨 GLOBAL VARIABLES
# ============================================================
VERSION = '1.0'
AUTHOR = 'vikk official'
CONFIG_FILE = 'controlrouter_config.json'
BLACKLIST_FILE = 'blacklist.txt'
WHITELIST_FILE = 'whitelist.txt'
PENDING_FILE = 'pending.txt'
APPROVED_FILE = 'approved.txt'
LOG_FILE = 'controlrouter.log'
running = True

BANNER = """
\033[96m
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗   ██╗████████╗     ║
║  ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝     ║
║  ██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║   ██║   ██║        ║
║  ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║   ██║   ██║        ║
║  ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝╚██████╔╝   ██║        ║
║   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝        ║
║                                                                               ║
║   CONTROLROUTER v1.0 - ULTIMATE EDITION                                      ║
║   Create by vikk official                                                     ║
║   "Control your network, control your world." 🔥                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
\033[0m
"""

# ============================================================
#  🛠️ UTILITY FUNCTIONS
# ============================================================
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def loading(text):
    print(f"\033[92m[+] {text}\033[0m")

def error(text):
    print(f"\033[91m[-] {text}\033[0m")

def info(text):
    print(f"\033[94m[!] {text}\033[0m")

def success(text):
    print(f"\033[92m[✓] {text}\033[0m")

def warning(text):
    print(f"\033[93m[⚠] {text}\033[0m")

def log_activity(text):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] {text}\n")

# ============================================================
#  🌐 COMMUNITY & SUPPORT
# ============================================================
def show_community():
    clear()
    print("\033[96m")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║                                                                       ║")
    print("║   🌐  OFFICIAL COMMUNITY & SUPPORT  🌐                              ║")
    print("║                                                                       ║")
    print("║   For updates, bug reports, and feature requests, join our Discord:  ║")
    print("║                                                                       ║")
    print("║   🔗  https://discord.gg/APQBgCaV6                                  ║")
    print("║                                                                       ║")
    print("║   ⚡  Report bugs, suggest features, get latest updates.            ║")
    print("║   💬  Chat with the community and the developer.                    ║")
    print("║                                                                       ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    input("\nPress Enter to return...")

# ============================================================
#  📂 CONFIG & LISTS
# ============================================================
def load_list(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_list(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(item + '\n')

def load_blacklist():
    return load_list(BLACKLIST_FILE)

def save_blacklist(data):
    save_list(BLACKLIST_FILE, data)

def load_whitelist():
    return load_list(WHITELIST_FILE)

def save_whitelist(data):
    save_list(WHITELIST_FILE, data)

def load_pending():
    return load_list(PENDING_FILE)

def save_pending(data):
    save_list(PENDING_FILE, data)

def load_approved():
    return load_list(APPROVED_FILE)

def save_approved(data):
    save_list(APPROVED_FILE, data)

def load_config():
    default = {
        'interface': 'wlan0',
        'gateway': '192.168.1.1',
        'subnet': '192.168.1.0/24',
        'monitor_interval': 10,
        'auto_block_new': False,
        'whitelist_mode': False
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(default, f, indent=2)
    return default

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# ============================================================
#  🔍 NETWORK FUNCTIONS
# ============================================================
def get_gateway():
    try:
        result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
        match = re.search(r'default via ([\d.]+)', result.stdout)
        if match:
            return match.group(1)
    except:
        pass
    return '192.168.1.1'

def get_interface():
    try:
        result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
        match = re.search(r'dev (\w+)', result.stdout)
        if match:
            return match.group(1)
    except:
        pass
    return 'wlan0'

def get_mac(ip):
    try:
        result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True)
        match = re.search(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})', result.stdout)
        if match:
            return match.group(1)
    except:
        pass
    return None

def get_device_name(mac):
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if mac in line:
                parts = line.split()
                if len(parts) >= 4:
                    return parts[0].strip('()')
    except:
        pass
    return 'Unknown'

def scan_network():
    config = load_config()
    gateway = config.get('gateway', get_gateway())
    subnet = gateway.rsplit('.', 1)[0] + '.0/24'
    devices = []
    
    loading(f"Scanning network {subnet} with nmap...")
    
    try:
        # Method 1: nmap ping scan
        result = subprocess.run(['nmap', '-sn', subnet], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        current_ip = None
        for line in lines:
            if 'Nmap scan report for' in line:
                parts = line.split()
                for part in parts:
                    if '.' in part and len(part.split('.')) == 4:
                        current_ip = part.strip('()')
                        break
            
            if 'MAC Address:' in line and current_ip:
                mac = line.split('MAC Address:')[1].split()[0].strip()
                name = line.split('(')[-1].strip(')') if '(' in line else 'Unknown'
                devices.append({'ip': current_ip, 'mac': mac, 'name': name, 'status': 'Active'})
                current_ip = None
    
    except Exception as e:
        error(f"nmap scan failed: {e}")
    
    # Method 2: Fallback to arp -a
    if not devices:
        loading("Fallback to arp -a...")
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if '(' in line and ')' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        ip = parts[1].strip('()')
                        mac = parts[3] if len(parts) > 3 else 'Unknown'
                        if mac != 'Unknown' and mac != '<incomplete>':
                            name = get_device_name(mac)
                            devices.append({'ip': ip, 'mac': mac, 'name': name, 'status': 'Active'})
        except:
            pass
    
    if not devices:
        warning("No devices found. Try manually: nmap -sn [your_subnet]")
        warning("Check your interface: ip route | grep default")
    
    return devices

# ============================================================
#  📋 ACCESS REQUEST SYSTEM
# ============================================================
def check_new_devices():
    """Detect new devices and add to pending list"""
    devices = scan_network()
    approved = load_approved()
    blacklist = load_blacklist()
    pending = load_pending()
    
    new_devices = []
    for device in devices:
        mac = device.get('mac', 'Unknown')
        if mac != 'Unknown' and mac not in approved and mac not in blacklist and mac not in pending:
            pending.append(mac)
            new_devices.append(device)
    
    if new_devices:
        save_pending(pending)
        warning(f"{len(new_devices)} new device(s) requesting access!")
        for d in new_devices:
            info(f"  📱 {d.get('ip')} - {d.get('mac')} ({d.get('name')})")
    
    return new_devices

def show_pending_requests():
    clear()
    print("\n\033[96m╔════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                          📋 PENDING ACCESS REQUESTS                             ║\033[0m")
    print("\033[96m╚════════════════════════════════════════════════════════════════════════════════╝\033[0m")
    
    pending = load_pending()
    
    if not pending:
        info("No pending requests.")
        input("\nPress Enter to continue...")
        return
    
    print("\n" + "="*70)
    print(f"{'NO':<5} {'MAC':<20} {'IP':<18} {'NAME':<20}")
    print("="*70)
    
    devices = scan_network()
    for i, mac in enumerate(pending, 1):
        ip = 'Unknown'
        name = 'Unknown'
        for d in devices:
            if d.get('mac') == mac:
                ip = d.get('ip', 'Unknown')
                name = d.get('name', 'Unknown')
                break
        print(f"{i:<5} {mac:<20} {ip:<18} {name:<20}")
    
    print("="*70)
    print(f"Total pending: {len(pending)}")
    
    print("\nOptions:")
    print("1. Approve all")
    print("2. Approve specific (by number)")
    print("3. Reject specific (by number)")
    print("4. Back to menu")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == '1':
        approved = load_approved()
        pending = load_pending()
        for mac in pending:
            if mac not in approved:
                approved.append(mac)
        save_approved(approved)
        save_pending([])
        success("All devices approved!")
    
    elif choice == '2':
        num = input("Enter number(s) to approve (e.g., 1,2,3): ")
        nums = [int(x.strip()) for x in num.split(',') if x.strip().isdigit()]
        pending = load_pending()
        approved = load_approved()
        for n in nums:
            if 1 <= n <= len(pending):
                mac = pending[n-1]
                if mac not in approved:
                    approved.append(mac)
        save_approved(approved)
        new_pending = [mac for i, mac in enumerate(pending) if (i+1) not in nums]
        save_pending(new_pending)
        success(f"Approved {len(nums)} device(s)!")
    
    elif choice == '3':
        num = input("Enter number(s) to reject (e.g., 1,2,3): ")
        nums = [int(x.strip()) for x in num.split(',') if x.strip().isdigit()]
        pending = load_pending()
        blacklist = load_blacklist()
        for n in nums:
            if 1 <= n <= len(pending):
                mac = pending[n-1]
                if mac not in blacklist:
                    blacklist.append(mac)
        save_blacklist(blacklist)
        new_pending = [mac for i, mac in enumerate(pending) if (i+1) not in nums]
        save_pending(new_pending)
        success(f"Rejected {len(nums)} device(s)!")
    
    elif choice == '4':
        return
    
    input("\nPress Enter to continue...")

# ============================================================
#  🚫 BLOCK FUNCTIONS
# ============================================================
def block_mac(mac):
    blacklist = load_blacklist()
    if mac in blacklist:
        warning(f"MAC {mac} already blocked")
        return
    
    blacklist.append(mac)
    save_blacklist(blacklist)
    
    try:
        subprocess.run(['sudo', 'arp', '-d', mac], capture_output=True)
        success(f"MAC {mac} blocked via ARP")
    except:
        pass
    
    try:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-m', 'mac', '--mac-source', mac, '-j', 'DROP'], capture_output=True)
        subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-m', 'mac', '--mac-source', mac, '-j', 'DROP'], capture_output=True)
        success(f"MAC {mac} blocked via iptables")
    except:
        pass
    
    log_activity(f"BLOCKED: {mac}")
    return True

def unblock_mac(mac):
    blacklist = load_blacklist()
    if mac not in blacklist:
        warning(f"MAC {mac} not in blacklist")
        return
    
    blacklist.remove(mac)
    save_blacklist(blacklist)
    
    try:
        subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-m', 'mac', '--mac-source', mac, '-j', 'DROP'], capture_output=True)
        subprocess.run(['sudo', 'iptables', '-D', 'FORWARD', '-m', 'mac', '--mac-source', mac, '-j', 'DROP'], capture_output=True)
    except:
        pass
    
    success(f"MAC {mac} unblocked")
    log_activity(f"UNBLOCKED: {mac}")
    return True

def block_all_new():
    devices = scan_network()
    blacklist = load_blacklist()
    whitelist = load_whitelist()
    config = load_config()
    
    blocked = 0
    for device in devices:
        if device['mac'] != 'Unknown' and device['mac'] not in blacklist:
            if config.get('whitelist_mode', False) and device['mac'] in whitelist:
                continue
            if block_mac(device['mac']):
                blocked += 1
    
    success(f"Blocked {blocked} new devices")
    return blocked

# ============================================================
#  📊 INTERFACE FUNCTIONS
# ============================================================
def show_devices():
    clear()
    print("\n\033[96m╔════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                          📡 ACTIVE DEVICES                                      ║\033[0m")
    print("\033[96m╚════════════════════════════════════════════════════════════════════════════════╝\033[0m")
    
    devices = scan_network()
    blacklist = load_blacklist()
    whitelist = load_whitelist()
    approved = load_approved()
    config = load_config()
    
    print("\n" + "="*85)
    print(f"{'NO':<5} {'IP':<18} {'MAC':<20} {'STATUS':<18} {'NAME':<20}")
    print("="*85)
    
    for i, device in enumerate(devices, 1):
        mac = device.get('mac', 'Unknown')
        if mac in blacklist:
            status = '🚫 BLOCKED'
        elif mac in approved:
            status = '✅ APPROVED'
        elif config.get('whitelist_mode', False) and mac in whitelist:
            status = '✅ ALLOWED'
        elif mac == 'Unknown':
            status = '❓ UNKNOWN'
        else:
            status = '⚠️ PENDING'
        
        print(f"{i:<5} {device['ip']:<18} {mac:<20} {status:<18} {device['name']:<20}")
    
    print("="*85)
    print(f"\nTotal devices: {len(devices)}")
    print(f"Blocked: {len(blacklist)}")
    print(f"Approved: {len(approved)}")
    print(f"Pending: {len(load_pending())}")
    print(f"Whitelist mode: {'ON' if config.get('whitelist_mode', False) else 'OFF'}")
    
    input("\nPress Enter to continue...")

def show_blacklist():
    clear()
    print("\n\033[96m╔════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                          🚫 BLACKLIST                                          ║\033[0m")
    print("\033[96m╚════════════════════════════════════════════════════════════════════════════════╝\033[0m")
    
    blacklist = load_blacklist()
    
    if not blacklist:
        info("Blacklist is empty")
    else:
        print("\n" + "="*60)
        for i, mac in enumerate(blacklist, 1):
            name = get_device_name(mac)
            print(f"{i}. {mac} - {name}")
        print("="*60)
        print(f"Total: {len(blacklist)} devices")
    
    input("\nPress Enter to continue...")

def show_whitelist():
    clear()
    print("\n\033[96m╔════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                          ✅ WHITELIST                                          ║\033[0m")
    print("\033[96m╚════════════════════════════════════════════════════════════════════════════════╝\033[0m")
    
    whitelist = load_whitelist()
    
    if not whitelist:
        info("Whitelist is empty")
    else:
        print("\n" + "="*60)
        for i, mac in enumerate(whitelist, 1):
            name = get_device_name(mac)
            print(f"{i}. {mac} - {name}")
        print("="*60)
        print(f"Total: {len(whitelist)} devices")
    
    input("\nPress Enter to continue...")

def show_logs():
    clear()
    print("\n\033[96m╔════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                          📋 ACTIVITY LOGS                                      ║\033[0m")
    print("\033[96m╚════════════════════════════════════════════════════════════════════════════════╝\033[0m")
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines[-20:]:
                print(line.strip())
    else:
        info("No logs yet")
    
    input("\nPress Enter to continue...")

# ============================================================
#  🎯 MAIN MENU
# ============================================================
def signal_handler(sig, frame):
    global running
    running = False
    print("\n\n\033[93m[!] Stopping...\033[0m")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    clear()
    print(BANNER)
    
    # ============================================================
    #  🚀 AUTO-LOAD ON START
    # ============================================================
    print("\033[96m╔═══════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                    🔄 INITIALIZING NETWORK SCAN                      ║\033[0m")
    print("\033[96m╚═══════════════════════════════════════════════════════════════════════╝\033[0m")
    
    # Detect gateway & interface
    gateway = get_gateway()
    interface = get_interface()
    loading(f"Gateway detected: {gateway}")
    loading(f"Interface detected: {interface}")
    
    # Save to config
    config = load_config()
    config['gateway'] = gateway
    config['interface'] = interface
    save_config(config)
    
    # Auto-scan network
    loading("Scanning network for devices...")
    devices = scan_network()
    
    if devices:
        success(f"Found {len(devices)} device(s) on network")
    else:
        warning("No devices found. Make sure you're connected to WiFi.")
    
    # Check pending requests
    loading("Checking for pending access requests...")
    new_devices = check_new_devices()
    if new_devices:
        warning(f"{len(new_devices)} new device(s) requesting access!")
        for d in new_devices:
            info(f"  📱 {d.get('ip')} - {d.get('mac')} ({d.get('name')})")
    
    # Display quick summary
    print("\n\033[96m╔═══════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[96m║                         📊 NETWORK SUMMARY                            ║\033[0m")
    print("\033[96m╚═══════════════════════════════════════════════════════════════════════╝\033[0m")
    print(f"\n  Gateway  : {gateway}")
    print(f"  Interface: {interface}")
    print(f"  Devices  : {len(devices)}")
    
    blacklist = load_blacklist()
    approved = load_approved()
    pending = load_pending()
    
    print(f"  Blocked  : {len(blacklist)}")
    print(f"  Approved : {len(approved)}")
    print(f"  Pending  : {len(pending)}")
    
    if pending:
        print("\n\033[93m⚠️ There are pending access requests!\033[0m")
        print("   Use option 12 to review them.")
    
    input("\n\033[96mPress Enter to continue to main menu...\033[0m")
    
    # ============================================================
    #  🎯 MAIN MENU LOOP
    # ============================================================
    while True:
        clear()
        print(BANNER)
        
        # Show real-time status bar
        config = load_config()
        gateway = config.get('gateway', get_gateway())
        interface = config.get('interface', get_interface())
        
        print(f"\033[90m┌─────────────────────────────────────────────────────────────────────────────────┐\033[0m")
        print(f"\033[90m│ Gateway: {gateway:<20} Interface: {interface:<15} │\033[0m")
        print(f"\033[90m│ Blacklist: {len(load_blacklist()):<10} Whitelist: {len(load_whitelist()):<10} Approved: {len(load_approved()):<10} Pending: {len(load_pending()):<10} │\033[0m")
        print(f"\033[90m└─────────────────────────────────────────────────────────────────────────────────┘\033[0m")
        
        print("""
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
\033[92m1.  📡 Scan Network (Show all devices)\033[0m
\033[92m2.  🚫 Block MAC Address\033[0m
\033[92m3.  ✅ Unblock MAC Address\033[0m
\033[92m4.  📋 Show Blacklist\033[0m
\033[92m5.  📋 Show Whitelist\033[0m
\033[92m6.  🛡️ Block All New Devices\033[0m
\033[92m7.  ⚪ Whitelist Mode (Allow only specific MACs)\033[0m
\033[92m8.  🔄 Auto-Block (Continuous monitoring)\033[0m
\033[92m9.  📰 Show Logs\033[0m
\033[92m10. ⚙️ Settings\033[0m
\033[92m11. 📱 Device Info\033[0m
\033[92m12. 📋 Pending Access Requests\033[0m
\033[92m13. 🌐 Community & Support\033[0m
\033[91m14. ❌ Exit\033[0m
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
""")
        
        choice = input("\033[96mSelect option (1-14): \033[0m")
        
        if choice == '1':
            show_devices()
        elif choice == '2':
            mac = input("Enter MAC address to block (xx:xx:xx:xx:xx:xx): ").strip()
            if re.match(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', mac, re.IGNORECASE):
                block_mac(mac)
            else:
                error("Invalid MAC format")
            input("\nPress Enter to continue...")
        elif choice == '3':
            mac = input("Enter MAC address to unblock: ").strip()
            unblock_mac(mac)
            input("\nPress Enter to continue...")
        elif choice == '4':
            show_blacklist()
        elif choice == '5':
            show_whitelist()
        elif choice == '6':
            warning("This will block ALL new devices not in blacklist")
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() == 'y':
                block_all_new()
            input("\nPress Enter to continue...")
        elif choice == '7':
            info("Whitelist Mode: Only allow devices in whitelist")
            mac = input("Enter MAC to add to whitelist (or 'done' to finish): ").strip()
            whitelist = load_whitelist()
            while mac.lower() != 'done':
                if re.match(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', mac, re.IGNORECASE):
                    if mac not in whitelist:
                        whitelist.append(mac)
                        success(f"Added {mac} to whitelist")
                    else:
                        warning(f"{mac} already in whitelist")
                else:
                    error("Invalid MAC format")
                mac = input("Enter MAC to add (or 'done' to finish): ").strip()
            save_whitelist(whitelist)
            config = load_config()
            config['whitelist_mode'] = True
            save_config(config)
            success(f"Whitelist mode enabled. {len(whitelist)} devices allowed.")
            input("\nPress Enter to continue...")
        elif choice == '8':
            warning("Auto-Block Mode: Monitoring network...")
            info("Press Ctrl+C to stop")
            try:
                while running:
                    devices = scan_network()
                    blacklist = load_blacklist()
                    whitelist = load_whitelist()
                    approved = load_approved()
                    config = load_config()
                    for device in devices:
                        mac = device.get('mac', 'Unknown')
                        if mac != 'Unknown' and mac not in blacklist and mac not in approved:
                            if config.get('whitelist_mode', False) and mac in whitelist:
                                continue
                            block_mac(mac)
                    time.sleep(config.get('monitor_interval', 10))
            except KeyboardInterrupt:
                info("Auto-Block stopped")
            input("\nPress Enter to continue...")
        elif choice == '9':
            show_logs()
        elif choice == '10':
            clear()
            print("\n\033[96m⚙️ SETTINGS\033[0m")
            config = load_config()
            print(f"1. Gateway: {config.get('gateway', 'N/A')}")
            print(f"2. Interface: {config.get('interface', 'N/A')}")
            print(f"3. Monitor Interval: {config.get('monitor_interval', 10)}s")
            print(f"4. Whitelist Mode: {config.get('whitelist_mode', False)}")
            print("5. Reset to default")
            opt = input("Select setting to change (1-5): ")
            if opt == '1':
                config['gateway'] = input("New gateway: ")
            elif opt == '2':
                config['interface'] = input("New interface: ")
            elif opt == '3':
                config['monitor_interval'] = int(input("New interval (seconds): "))
            elif opt == '4':
                config['whitelist_mode'] = not config.get('whitelist_mode', False)
                success(f"Whitelist mode: {config['whitelist_mode']}")
            elif opt == '5':
                config = {'interface': 'wlan0', 'gateway': '192.168.1.1', 'subnet': '192.168.1.0/24', 'monitor_interval': 10, 'auto_block_new': False, 'whitelist_mode': False}
            save_config(config)
            success("Settings updated")
            input("\nPress Enter to continue...")
        elif choice == '11':
            show_devices()
        elif choice == '12':
            show_pending_requests()
        elif choice == '13':
            show_community()
        elif choice == '14':
            print("\n\033[92mControl your network, control your world. 🔥\033[0m")
            sys.exit(0)
        else:
            error("Invalid option")
            input("\nPress Enter to continue...")

# ============================================================
#  🚀 START
# ============================================================
if __name__ == '__main__':
    main()
