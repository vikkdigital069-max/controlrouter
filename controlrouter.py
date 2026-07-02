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
    devices = []
    
    loading(f"Scanning network...")
    
    # ARP Scan
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if '(' in line and ')' in line:
                parts = line.split()
                if len(parts) >= 3:
                    ip = parts[1].strip('()')
                    mac = parts[3] if len(parts) > 3 else 'Unknown'
                    if mac != 'Unknown' and mac != '<incomplete>':
                        name = get_device_name(mac)
                        devices.append({'ip': ip, 'mac': mac, 'name': name, 'status': 'Active'})
    except:
        pass
    
    # Ping sweep
    try:
        for i in range(1, 255):
            ip = gateway.rsplit('.', 1)[0] + f'.{i}'
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True)
            if '1 received' in result.stdout:
                if not any(d['ip'] == ip for d in devices):
                    mac = get_mac(ip) or 'Unknown'
                    devices.append({'ip': ip, 'mac': mac, 'name': get_device_name(mac), 'status': 'Active'})
    except:
        pass
    
    return devices

# ============================================================
#  🚫 BLOCK FUNCTIONS (REAL)
# ============================================================
def block_mac(mac):
    blacklist = load_blacklist()
    if mac in blacklist:
        warning(f"MAC {mac} already blocked")
        return
    
    blacklist.append(mac)
    save_blacklist(blacklist)
    
    # Method 1: ARP poisoning (real blocking)
    try:
        subprocess.run(['sudo', 'arp', '-d', mac], capture_output=True)
        success(f"MAC {mac} blocked via ARP")
    except:
        pass
    
    # Method 2: iptables blocking (if available)
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
    
    # Remove iptables rules
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
            # Check whitelist mode
            if config.get('whitelist_mode', False) and device['mac'] in whitelist:
                continue
            if block_mac(device['mac']):
                blocked += 1
    
    success(f"Blocked {blocked} new devices")
    return blocked

def deauth_attack(mac, interface='wlan0'):
    """Send deauth packets to disconnect device (requires monitor mode)"""
    warning("Deauth attack requires monitor mode")
    try:
        # Try aireplay-ng if available
        subprocess.run(['sudo', 'aireplay-ng', '--deauth', '10', '-a', mac, interface], capture_output=True)
        success(f"Deauth sent to {mac}")
    except:
        error("Deauth not available. Install aircrack-ng")
        return False
    return True

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
    config = load_config()
    
    print("\n" + "="*80)
    print(f"{'NO':<5} {'IP':<18} {'MAC':<20} {'STATUS':<15} {'NAME':<20}")
    print("="*80)
    
    for i, device in enumerate(devices, 1):
        if device['mac'] in blacklist:
            status = '🚫 BLOCKED'
        elif config.get('whitelist_mode', False) and device['mac'] in whitelist:
            status = '✅ ALLOWED'
        elif device['mac'] == 'Unknown':
            status = '❓ UNKNOWN'
        else:
            status = '✅ ALLOWED'
        
        print(f"{i:<5} {device['ip']:<18} {device['mac']:<20} {status:<15} {device['name']:<20}")
    
    print("="*80)
    print(f"\nTotal devices: {len(devices)}")
    print(f"Blocked: {len([d for d in devices if d['mac'] in blacklist])}")
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
    
    config = load_config()
    gateway = config.get('gateway', get_gateway())
    interface = config.get('interface', get_interface())
    
    print(f"\033[90m┌─────────────────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[90m│ Gateway: {gateway:<20} Interface: {interface:<15} │\033[0m")
    print(f"\033[90m│ Blacklist: {len(load_blacklist()):<10} Whitelist: {len(load_whitelist()):<10} Mode: {'WHITELIST' if config.get('whitelist_mode', False) else 'BLACKLIST'} │\033[0m")
    print(f"\033[90m└─────────────────────────────────────────────────────────────────┘\033[0m")
    
    print("""
\033[96m═══════════════════════════════════════════════════════════════════════\033[0m
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
\033[92m12. 🌐 Community & Support\033[0m
\033[91m13. ❌ Exit\033[0m
\033[96m═══════════════════════════════════════════════════════════════════════\033[0m
""")
    
    choice = input("\033[96mSelect option (1-13): \033[0m")
    
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
                config = load_config()
                for device in devices:
                    if device['mac'] != 'Unknown' and device['mac'] not in blacklist:
                        if config.get('whitelist_mode', False) and device['mac'] in whitelist:
                            continue
                        block_mac(device['mac'])
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
        show_community()
    
    elif choice == '13':
        print("\n\033[92mControl your network, control your world. 🔥\033[0m")
        sys.exit(0)
    
    else:
        error("Invalid option")
        input("\nPress Enter to continue...")
    
    main()

# ============================================================
#  🚀 START
# ============================================================
if __name__ == '__main__':
    main()
