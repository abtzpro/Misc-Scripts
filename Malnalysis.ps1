# You will need to have the ThreatIntelligence module installed for this to work
# You can install it using 'Install-Module -Name ThreatIntelligence'

# Define the output directory
$OutputDir = ".\Malware Analysis"
# Create the directory if it doesn't exist
if(!(Test-Path -Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Get a list of running processes
Get-Process | Out-File -FilePath "$OutputDir\1_processes.txt"

# Get detailed process information including loaded modules
Get-Process | ForEach-Object {
    $_ | Format-List * 
    $_.Modules | Format-List *
} | Out-File -FilePath "$OutputDir\2_detailed_processes.txt"

# Get a list of active network connections
Get-NetTCPConnection | Out-File -FilePath "$OutputDir\3_connections.txt"

# Get a list of auto-start entries
Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name, command, Location, User | Out-File -FilePath "$OutputDir\4_startup.txt"

# Show hidden files and protected operating system files
Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Name Hidden -Value 1
Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Name ShowSuperHidden -Value 1

# Get a list of all files in critical system directories
Get-ChildItem -Path C:\Windows\System32, C:\ProgramData -Recurse -Force -ErrorAction SilentlyContinue | Out-File -FilePath "$OutputDir\5_system_files.txt"

# List all services
Get-Service | Format-List * | Out-File -FilePath "$OutputDir\6_services.txt"

# List all drivers
Get-WmiObject Win32_SystemDriver | Format-List * | Out-File -FilePath "$OutputDir\7_drivers.txt"

# Check for any oddities in the hosts file
Get-Content -Path C:\Windows\System32\drivers\etc\hosts | Out-File -FilePath "$OutputDir\8_hosts.txt"

# Query AlienVault OTX for threat intelligence
# Here you would normally use the IP addresses or domain names you are interested in
# In this case, replace 'YOUR_OTX_API_KEY' with your actual AlienVault OTX API key
# and replace 'Indicator_To_Search' with actual IP address or domain name
# $OtxKey = 'YOUR_OTX_API_KEY'
# $IndicatorToSearch = 'Indicator_To_Search'
# Get-OtxPulse -APIKey $OtxKey -Indicator $IndicatorToSearch | Out-File -FilePath "$OutputDir\9_OTX_Pulse.txt"
