import urllib.request
import subprocess

# List of URLs for the blocklists
blocklist_urls = [
    'https://www.spamhaus.org/drop/drop.txt',
    'http://lists.blocklist.de/lists/all.txt',
    # Add more URLs as needed
]

def download_blocklist(url):
    with urllib.request.urlopen(url) as response:
        return [ip.strip() for ip in response.read().decode().splitlines() if ip.strip()]

def block_ip(ip):
    # Block inbound and outbound traffic for the IP
    subprocess.run(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block protocol=any remoteip={ip}', shell=True)
    subprocess.run(f'netsh advfirewall firewall add rule name="Block {ip}" dir=out action=block protocol=any remoteip={ip}', shell=True)

def main():
    blocklist = []
    for url in blocklist_urls:
        blocklist.extend(download_blocklist(url))

    # Remove duplicates
    blocklist = list(set(blocklist))

    for ip in blocklist:
        block_ip(ip)

if __name__ == '__main__':
    main()
