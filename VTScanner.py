import os
import hashlib
import requests
import time

API_KEY = '850bbcad00c66ad6980503688affc7fdd0b9caf200a1d228c01518e67f7803e3'

def get_file_hashes(directory):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            hash_md5 = hashlib.md5()
            try:
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                yield hash_md5.hexdigest()
            except PermissionError:
                print(f"Permission denied for file: {filepath}")
                continue

def check_virus_total(file_hashes):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    with open('VirusTotalResults.txt', 'a') as f:
        for file_hash in file_hashes:
            params = {'apikey': API_KEY, 'resource': file_hash}
            response = requests.get(url, params=params)
            data = response.json()
            if data['response_code'] == 1:
                result = f'File Hash: {file_hash}\nAntivirus Results: {data["positives"]}/{data["total"]}\n'
                print(result)
                f.write(result)
            else:
                result = f'File Hash: {file_hash}\nNot Found in VirusTotal\n'
                print(result)
                f.write(result)
            time.sleep(15)  # To comply with the public API's request rate limit

def main():
    directory = 'C:\\'
    file_hashes = get_file_hashes(directory)
    check_virus_total(file_hashes)

if __name__ == "__main__":
    main()
