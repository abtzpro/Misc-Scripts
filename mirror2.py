import os
import shutil
import time
import subprocess

# function to monitor machine for cyberattack
def monitor():
    while True:
        # check for signs of an ongoing attack
        if detect_attack():
            # create a directory to store logs and mirror attacker's actions if it doesn't exist
            if not os.path.exists("attack_logs"):
                os.mkdir("attack_logs")
            # mirror attacker's actions
            while True:
                try:
                    action = input("> ")
                    os.system(action)
                    with open("attack_logs/attackers_log.txt", "a") as f:
                        f.write(action + "\n")
                except KeyboardInterrupt:
                    break
        # wait for next iteration
        time.sleep(10)

# function to detect an ongoing attack
def detect_attack():
    # check for unusual network traffic
    network_traffic = subprocess.check_output("netstat -a -n -o | findstr :80", shell=True).decode("utf-8")
    if network_traffic:
        with open("attack_logs/network_traffic.log", "w") as f:
            f.write(network_traffic)
        return True

    # monitor system logs for suspicious activity
    system_logs = subprocess.check_output("wevtutil qe System /f:text /c:1 /rd:true /q:\"*[System[(EventID=4624)]]\"", shell=True).decode("utf-8")
    if system_logs:
        with open("attack_logs/system_logs.log", "w") as f:
            f.write(system_logs)
        return True

    # replace with additional checks as necessary
    return False

# function to enable PowerShell logging
def enable_powershell_logging():
    os.system("powershell -Command Set-ExecutionPolicy RemoteSigned")
    os.system("powershell -Command $LogFile = 'C:\\Logs\\PowerShell\\' + (Get-Date -Format 'yyyy-MM-dd_HH-mm-ss') + '.log'; Start-Transcript -Path $LogFile -Force")

# function to disable PowerShell logging
def disable_powershell_logging():
    os.system("powershell -Command Stop-Transcript")

# function to enable Windows Event Logging
def enable_event_logging():
    os.system("powershell -Command 'Get-EventLog -List | Where-Object {$_.Log -eq \"Windows PowerShell\"} | ForEach-Object {$_ | Set-EventLog -Enabled $True}'")
    os.system("powershell -Command 'Get-EventLog -List | Where-Object {$_.Log -eq \"Security\"} | ForEach-Object {$_ | Set-EventLog -Enabled $True}'")

# function to disable Windows Event Logging
def disable_event_logging():
    os.system("powershell -Command 'Get-EventLog -List | Where-Object {$_.Log -eq \"Windows PowerShell\"} | ForEach-Object {$_ | Set-EventLog -Enabled $False}'")
    os.system("powershell -Command 'Get-EventLog -List | Where-Object {$_.Log -eq \"Security\"} | ForEach-Object {$_ | Set-EventLog -Enabled $False}'")

# function to enable Windows Firewall logging
def enable_firewall_logging():
    os.system("powershell -Command Set-NetFirewallProfile -LogAllowed True -LogBlocked True -LogFileName C:\\Logs\\Firewall\\firewall.log")

# function to disable Windows Firewall logging
def disable_firewall_logging():
    os.system("powershell -Command Set-NetFirewallProfile -LogAllowed False -LogBlocked False")

# function to enable Windows Defender logging
def enable_defender_logging():
    os.system("powershell -Command Set-MpPreference -EnableControlledFolderAccess AuditMode")
    os.system("powershell -Command Set-MpPreference -MAPSReporting AuditMode")

# function to disable Windows Defender logging
def disable_defender_logging():
    os.system("powershell -Command Set-MpPreference -EnableControlledFolderAccess Disabled")
    os.system("powershell -Command Set-MpPreference -MAPSReporting Disabled")

# start monitoring
monitor()
