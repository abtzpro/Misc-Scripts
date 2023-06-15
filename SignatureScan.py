import os
import hashlib
import requests
import json
import datetime

def calculate_hash(file_path):
    try:
        with open(file_path, 'rb') as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest()
            return readable_hash
    except Exception:
        return None

def main():
    # AlienVault OTX setup
    api_key = 'cb212bd27df90d623f9b17bd40c9c255db443397dd8ef2763f41004ba934844b'  # Replace with your actual OTX API key
    search_term = 'Turla'
    session = requests.Session()
    session.headers.update({'X-OTX-API-KEY': api_key})
    response = session.get(f'https://otx.alienvault.com:443/api/v1/pulses/subscribed?search={search_term}')
    pulses = json.loads(response.text)

    turla_signatures = []
    for pulse in pulses['results']:
        for indicator in pulse['indicators']:
            if indicator['type'] == 'FileHash-SHA256':
                turla_signatures.append(indicator['indicator'])

    log_file = open('scan_log.txt', 'a')

    for foldername, subfolders, filenames in os.walk('C:\\'):
        for filename in filenames:
            full_path = os.path.join(foldername, filename)
            file_hash = calculate_hash(full_path)
            if file_hash in turla_signatures:
                log_entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}: File with Turla hash found: {full_path}, hash: {file_hash}\n"
                log_file.write(log_entry)

    log_file.close()

if __name__ == "__main__":
    main()