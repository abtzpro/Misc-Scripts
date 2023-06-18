$sysinternalsPath = "C:\Users\Recta\OneDrive\Desktop\SysinternalsSuite"
$outputFilePath = "C:\Users\Recta\OneDrive\Desktop\Testing\IDS1-Output.txt"
$gitRepoPath = "C:\Users\Recta\OneDrive\Desktop\Testing"

$suspiciousEventIDs = @(4625, 4720, 1102, 7045, 4672)
$suspiciousIPs = @("192.0.2.0", "203.0.113.0")
$suspiciousDomains = @("malicious.com", "suspicious.net")
$suspiciousProcessNames = @("badprocess.exe", "malware.exe")
$suspiciousFileHashes = @("9f86d081884c7d659a2feaa0c55ad015", "5f4dcc3b5aa765d61d8327deb882cf99")

function Analyze-ActiveTCPConnectionsForSuspiciousActivities {
    $connections = Get-NetTCPConnection | Where-Object { $suspiciousIPs -contains $_.RemoteAddress -or $suspiciousDomains -contains $_.RemoteAddress }
    foreach ($connection in $connections) {
        Write-Output "Suspicious TCP connection detected: $($connection.RemoteAddress)"
    }
}

function Analyze-EventLogsForSuspiciousActivities {
    $logs = Get-WinEvent -LogName "Security", "System", "Application" -MaxEvents 100
    $suspiciousEvents = $logs | Where-Object { $suspiciousEventIDs -contains $_.Id }
    foreach ($event in $suspiciousEvents) {
        Write-Output "Suspicious event detected: $($event.Id) - $($event.Message)"
    }
}

function Analyze-RunningProcessesForSuspiciousNames {
    $runningProcesses = Get-Process
    $suspiciousProcesses = $runningProcesses | Where-Object { $suspiciousProcessNames -contains $_.Name }
    foreach ($process in $suspiciousProcesses) {
        Write-Output "Suspicious process detected: $($process.Name)"
    }
}

function Analyze-FilesForSuspiciousHashes {
    $runningProcesses = Get-Process
    foreach ($process in $runningProcesses) {
        if ($null -ne $process.Path) {
            $hash = Get-FileHash -Path $process.Path -ErrorAction SilentlyContinue
            if ($null -ne $hash) {
                if ($suspiciousFileHashes -contains $hash.Hash) {
                    Write-Output "Suspicious file hash detected: $($hash.Hash)"
                }
            }
        }
    }
}

while ($true) {
    # Use Sysmon to monitor system activities
    $sysmonOutput = & "$sysinternalsPath\Sysmon.exe" -accepteula -h md5,sha256 -i
    Add-Content -Path $outputFilePath -Value $sysmonOutput

    # Analyze network connections for suspicious activities
    $connectionsOutput = Analyze-ActiveTCPConnectionsForSuspiciousActivities
    Add-Content -Path $outputFilePath -Value $connectionsOutput

    # Analyze event logs for suspicious activities
    $logsOutput = Analyze-EventLogsForSuspiciousActivities
    Add-Content -Path $outputFilePath -Value $logsOutput

    # Analyze running processes for suspicious names
    $processesOutput = Analyze-RunningProcessesForSuspiciousNames
    Add-Content -Path $outputFilePath -Value $processesOutput

    # Analyze running processes for suspicious file hashes
    $hashesOutput = Analyze-FilesForSuspiciousHashes
    Add-Content -Path $outputFilePath -Value $hashesOutput

    # Every 3 hours, commit and push the output file to GitHub
    if ((Get-Date).Hour % 3 -eq 0) {
        Set-Location -Path $gitRepoPath
        & git add .
        & git commit -m "Automatic update from IDS script"
        & gh repo clone https://github.com/abtzpro/SimpleIDS.git
        & git push
    }

    # Pause before the next iteration
    Start-Sleep -Seconds 60
}
