@echo off
title Kill VPN SOCKS5 Proxy
echo ========================================
echo Stopping VPN SOCKS5 Proxy
echo ========================================
echo.

echo Finding SOCKS5 proxy process...
set FOUND=0

for /f "tokens=2" %%i in ('wmic process where "CommandLine like '%%socks5_proxy.py%%'" get ProcessId /value 2^>nul ^| findstr ProcessId') do (
    for /f "tokens=2 delims==" %%j in ("%%i") do (
        if "%%j" neq "" (
            echo Found SOCKS5 proxy running on PID: %%j
            echo Killing process...
            taskkill /PID %%j /F
            if %errorlevel% equ 0 (
                echo SUCCESS: SOCKS5 proxy stopped!
                set FOUND=1
            ) else (
                echo ERROR: Failed to stop SOCKS5 proxy
            )
            goto :found
        )
    )
)

if %FOUND%==0 (
    echo No SOCKS5 proxy found running
)

:found
echo.
echo Verifying port 1081 is free:
netstat -ano | findstr :1081
if %errorlevel% neq 0 (
    echo Port 1081 is now free
) else (
    echo Some connections may still be in TIME_WAIT state
)

echo.
pause
