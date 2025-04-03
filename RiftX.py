import random
import string
import time
import socket
import whois
import requests
import multiprocessing

def print_banner():
    print("""
    ██████╗ ██╗███████╗████████╗██╗  ██╗
    ██╔══██╗██║██╔════╝╚══██╔══╝██║  ██║
    ██████╔╝██║███████╗   ██║   ███████║
    ██╔═══╝ ██║╚════██║   ██║   ██╔══██║
    ██║     ██║███████║   ██║   ██║  ██║
    ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝
    RiftX - Ethical Hacking & Pentesting Tool
    """)

def show_options():
    print("\nSelect an operation:")
    print("1. Brute Force Attack")
    print("2. Vulnerability Scan")
    print("3. Passive Reconnaissance")
    print("4. Exit")

def brute_force_attack(target_url, username, password_list, delay):
    with requests.Session() as session:  # Using requests session for HTTP requests
        for password in password_list:
            response = session.post(target_url, data={"username": username, "password": password})
            if "Invalid credentials" not in response.text:
                print(f"Success! Found password: {password}")
                break
            time.sleep(delay)

def multi_process_brute_force(target_url, username, password_list, num_processes=10, delay=0):
    pool = multiprocessing.Pool(processes=num_processes)
    results = [pool.apply_async(brute_force_attack, (target_url, username, [password], delay)) for password in password_list]
    for result in results:
        result.get()  # Wait for all results to finish

def generate_password_list(length=8, count=10):
    return [''.join(random.choices(string.ascii_letters + string.digits, k=length)) for _ in range(count)]

# Basic Port Scan using socket
def basic_port_scan(target_ip):
    print(f"\nPerforming basic port scan on {target_ip}...")
    open_ports = []
    for port in range(20, 1025):  # Scanning common ports (20-1024)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Port {port} is open")
            open_ports.append(port)
        sock.close()

    if not open_ports:
        print("No open ports found.")
    else:
        print(f"Open ports: {open_ports}")

# Passive Reconnaissance - WHOIS Lookup
def whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        print("\nWHOIS Information:")
        print(domain_info)
    except Exception as e:
        print(f"Error fetching WHOIS data: {e}")

# Passive Reconnaissance - DNS Lookup using socket
def dns_lookup(domain):
    try:
        print("\nDNS Records (A):")
        ip = socket.gethostbyname(domain)  # Resolve domain to IP address
        print(f"IP Address: {ip}")
    except Exception as e:
        print(f"Error fetching DNS records: {e}")

# Passive Reconnaissance - IP Geolocation using ip-api.com
def ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'fail':
            print(f"Could not fetch geolocation for IP: {ip}")
        else:
            print("\nIP Geolocation:")
            print(f"Location: {data['city']}, {data['country']}")
    except Exception as e:
        print(f"Error fetching geolocation: {e}")

def main():
    print_banner()
    delay = 1
    num_processes = 5
    while True:
        show_options()
        choice = input("Enter your choice: ")
        if choice == "1":
            target_url = input("Enter target login URL: ")
            username = input("Enter username: ")
            password_list = generate_password_list()
            print(f"Starting multi-process brute-force attack...")
            multi_process_brute_force(target_url, username, password_list, num_processes, delay)
        elif choice == "2":
            target_ip = input("Enter target IP for vulnerability scan: ")
            print(f"Performing basic port scan on {target_ip}...")
            basic_port_scan(target_ip)
        elif choice == "3":
            domain = input("Enter domain for Passive Reconnaissance: ")
            print(f"Performing Passive Reconnaissance on {domain}...")
            whois_lookup(domain)
            dns_lookup(domain)
            ip = input("Enter IP for geolocation lookup: ")
            ip_geolocation(ip)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
