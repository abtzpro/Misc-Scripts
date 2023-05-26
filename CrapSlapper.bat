@echo off
setlocal enabledelayedexpansion

:: Close the browser
taskkill /f /im msedge.exe > nul 2>&1

:: Terminate Edge processes
taskkill /f /im MicrosoftEdge.exe > nul 2>&1
taskkill /f /im MicrosoftEdgeCP.exe > nul 2>&1

:: Terminate Runtime Broker processes causing high network/CPU/GPU usage
for /f "tokens=2 delims=," %%A in ('wmic process where "name='RuntimeBroker.exe'" get processid^,description /format:csv ^| findstr /r "[0-9]"') do (
    set "PID=%%~A"
    tasklist /fi "PID eq !PID!" | find /i "RuntimeBroker.exe" > nul 2>&1
    if not errorlevel 1 (
        wmic process where "processid='!PID!'" CALL terminate > nul 2>&1
    )
)

:: Reset network stack and interfaces
ipconfig /release
ipconfig /renew
ipconfig /flushdns
nbtstat -R
nbtstat -RR
netsh int ip reset
netsh winsock reset
netsh advfirewall reset
netsh branchcache reset
netsh int ipv4 reset reset.log
netsh int ipv6 reset reset.log
netsh int httpstunnel reset
netsh int isatap reset
netsh int portproxy reset
netsh int tcp reset reset.log
netsh int teredo reset
netsh int httpstunnel reset all
netsh int portproxy reset all
netsh int ipv6 reset
netsh winhttp reset proxy
netsh winhttp reset tracing
netsh winsock reset catalog

:: Detect and delete third-party user-mode services
for /f "tokens=1,2*" %%i in ('sc query type^= own type^= interact') do (
    if "%%i"=="SERVICE_NAME:" (
        for /f "tokens=2 delims=:" %%x in ('sc qc %%j ^| findstr "BINARY_PATH_NAME"') do (
            set "path=%%x"
            if "!path:system32=!"=="!path!" (
                if "!path:SysWOW64=!"=="!path!" (
                    echo Found 3rd Party User-Mode Service: %%j
                    sc stop %%j
                    sc delete %%j
                ) else (
                    echo Ignoring Windows User-Mode Service: %%j
                )
            ) else (
                echo Ignoring Windows User-Mode Service: %%j
            )
        )
    )
)

echo Network interference script complete!
endlocal
