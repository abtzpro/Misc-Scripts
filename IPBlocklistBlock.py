import subprocess

# Put the path to your blocklist file here
blocklist_file_path = r'C:\pathtoyour\ipblockist.txt'

def read_blocklist(file_path):
    with open(file_path, 'r') as file:
        return [ip.strip() for ip in file.readlines() if ip.strip()]

def block_ip(ip):
    # Block inbound and outbound traffic for the IP
    subprocess.run(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}', shell=True)
    subprocess.run(f'netsh advfirewall firewall add rule name="Block {ip}" dir=out action=block remoteip={ip}', shell=True)

def main():
    blocklist = read_blocklist(blocklist_file_path)
    for ip in blocklist:
        block_ip(ip)

if __name__ == '__main__':
    main()
