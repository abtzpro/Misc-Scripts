import os
import requests
import json
import yara

def main():
    # AlienVault OTX setup
    api_key = 'your_otx_api_key'  # Replace with your actual OTX API key
    search_term = 'Turla'
    session = requests.Session()
    session.headers.update({'cb212bd27df90d623f9b17bd40c9c255db443397dd8ef2763f41004ba934844b': api_key})
    response = session.get(f'https://otx.alienvault.com:443/api/v1/pulses/subscribed?search={search_term}')
    pulses = json.loads(response.text)

    # Add a basic rule to look for suspicious JavaScript
    yara_rule = '''
    rule SuspiciousJavaScript {
        strings:
            $js_eval = /eval\s*\(/ nocase
            $js_unescape = /unescape\s*\(/ nocase
            $js_escape = /escape\s*\(/ nocase
            $js_exec = /\.exec\s*\(/ nocase
        condition:
            any of them
    }
    '''

    rules = yara.compile(source=yara_rule)

    for foldername, subfolders, filenames in os.walk('C:\\'):
        for filename in filenames:
            full_path = os.path.join(foldername, filename)
            if full_path.endswith('.js'):
                try:
                    matches = rules.match(full_path)
                    if matches:
                        print(f"Suspicious JavaScript file found and will be deleted: {full_path}")
                        os.remove(full_path)  # Deletes the file
                except Exception:
                    continue  # Ignore errors like PermissionError or FileNotFoundError

if __name__ == "__main__":
    main()
