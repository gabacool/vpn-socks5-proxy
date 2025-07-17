@echo off
title VPN SOCKS5 Proxy Server
echo ========================================
echo VPN SOCKS5 Proxy Server
echo ========================================
echo.
echo Starting proxy server...
echo.
echo Proxy will be available at:
echo   Host: [Auto-detected]
echo   Port: 1081
echo   Type: SOCKS5
echo.
echo Configure your client (Chrome/FoxyProxy/etc.)
echo with the host IP shown above.
echo.
echo Press Ctrl+C to stop the proxy
echo ========================================
echo.

cd /d "%~dp0\.."
python socks5_proxy.py

echo.
echo Proxy stopped. Press any key to exit...
pause >nul
