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