@echo off
title Create Desktop Shortcut
echo ========================================
echo Creating Desktop Shortcut
echo ========================================
echo.

set SCRIPT="%TEMP%\CreateVPNProxyShortcut.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\VPN SOCKS5 Proxy.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0start_proxy.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "Start VPN SOCKS5 Proxy Server" >> %SCRIPT%
echo oLink.IconLocation = "C:\Windows\System32\shell32.dll,13" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo Desktop shortcut created: "VPN SOCKS5 Proxy"
echo You can now double-click the desktop icon to start the proxy.
echo.
pause
