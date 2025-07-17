@echo off
title Check VPN SOCKS5 Proxy Status
echo ========================================
echo VPN SOCKS5 Proxy Status Check
echo ========================================
echo.

echo 1. Checking port 1081 usage:
echo --------------------------------
netstat -ano | findstr :1081
if %errorlevel% neq 0 (
    echo No process listening on port 1081
) else (
    echo.
    echo Port 1081 is in use (proxy may be running)
)
echo.

echo 2. Finding Python SOCKS5 process:
echo --------------------------------
for /f "tokens=1,2" %%a in ('wmic process where "CommandLine like '%%socks5_proxy.py%%'" get ProcessId^,CommandLine /format:csv 2^>nul ^| findstr /v "Node\|^$"') do (
    if "%%b" neq "" (
        echo Found SOCKS5 proxy running:
        echo   PID: %%b
        echo   Command: %%a
        echo.
        echo To stop the proxy:
        echo   management\kill_proxy.bat
        goto :found
    )
)

echo No SOCKS5 proxy process found
echo.
echo To start the proxy:
echo   management\start_proxy.bat

:found
echo.
echo 3. Network interface information:
echo --------------------------------
ipconfig | findstr /C:"IPv4 Address"

echo.
pause
