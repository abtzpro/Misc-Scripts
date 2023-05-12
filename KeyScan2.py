import os
import psutil
import re
import subprocess
import winreg

def find_suspicious_processes():
    suspicious_processes = []

    for process in psutil.process_iter(['name', 'pid', 'exe', 'cmdline', 'connections']):
        process_name = process.info['name'].lower()

        # Check for suspicious process names
        if re.search(r'key(log|scan|hook|record|capture)', process_name):
            suspicious_processes.append(process)
            continue

        # Check for suspicious command line arguments
        cmdline = process.info['cmdline']
        if cmdline:
            cmdline = ' '.join(cmdline).lower()
            if re.search(r'key(log|scan|hook|record|capture)', cmdline):
                suspicious_processes.append(process)
                continue

        # Check for processes with an unusually high number of connections
        connections = process.info['connections']
        if connections:
            if len(connections) > 20:
                suspicious_processes.append(process)
                continue

    return suspicious_processes

def check_registry():
    reg_paths = [
        (winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run"),
        (winreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run"),
        (winreg.HKEY_LOCAL_MACHINE, "Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run")
    ]

    suspicious_keys = []

    for hkey, path in reg_paths:
        try:
            registry_key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    key_name, key_value, key_type = winreg.EnumValue(registry_key, i)
                    if re.search(r'key(log|scan|hook|record|capture)', key_value, re.IGNORECASE):
                        suspicious_keys.append((hkey, path, key_name))
                    i += 1
                except WindowsError:
                    break
            winreg.CloseKey(registry_key)
        except WindowsError:
            pass

    return suspicious_keys

def remove_registry_keys(keys):
    for hkey, path, key_name in keys:
        try:
            registry_key = winreg.OpenKey(hkey, path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(registry_key, key_name)
            winreg.CloseKey(registry_key)
            print(f"Removed registry key: {key_name}")
        except WindowsError:
            print(f"Unable to remove registry key: {key_name}")

def terminate_processes(processes):
    for process in processes:
        try:
            process.terminate()
            print(f"Terminated process: {process.info['name']} (PID: {process.info['pid']})")
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            print(f"Unable to terminate process: {process.info['name']} (PID: {process.info['pid']})")

def main():
    print("Scanning for potential keyloggers...")
    suspicious_processes = find_suspicious_processes()
    suspicious_registry_keys = check_registry()

    if suspicious_processes or suspicious_registry_keys:
        if suspicious_processes:
            print(f"Found {len(suspicious_processes)} potential keylogger processes:")
            for process in suspicious_processes:
                print(f"  {process.info['name']} (PID: {process.info['pid']})")

            print("Terminating suspicious processes...")
            terminate_processes(suspicious_processes)
            print("Termination complete.")
        
        if suspicious_registry_keys:
            print(f"Found {len(suspicious_registry_keys)} potential keylogger registry keys:")
            for hkey, path, key_name in suspicious_registry_keys:
                print(f"  {key_name}")

            print("Removing suspicious registry keys...")
            remove_registry_keys(suspicious_registry_keys)
            print("Removal complete.")
    else:
        print("No potential keyloggers found.")

    # Check for suspicious network connections
    suspicious_connections = check_network_connections()

    if suspicious_connections:
        print(f"Found {len(suspicious_connections)} potential keylogger connections:")
        for conn in suspicious_connections:
            print(f"  {conn}")

        print("Blocking suspicious connections...")
        block_network_connections(suspicious_connections)
        print("Blocking complete.")
    else:
        print("No potential keylogger connections found.")

    # Check for suspicious files
    suspicious_files = check_files()

    if suspicious_files:
        print(f"Found {len(suspicious_files)} potential keylogger files:")
        for file_path in suspicious_files:
            print(f"  {file_path}")

        print("Deleting suspicious files...")
        delete_files(suspicious_files)
        print("Deletion complete.")
    else:
        print("No potential keylogger files found.")

if __name__ == "__main__":
    main()
