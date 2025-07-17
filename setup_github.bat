@echo off
title Initialize GitHub Repository
echo ========================================
echo VPN SOCKS5 Proxy - GitHub Setup
echo ========================================
echo.

echo This script will help you set up the GitHub repository.
echo Make sure you have Git installed and GitHub account ready.
echo.

echo Step 1: Initialize Git Repository
echo ================================
git init
git add .
git commit -m "Initial commit - VPN SOCKS5 Proxy v1.0"
echo.

echo Step 2: Create GitHub Repository
echo ================================
echo 1. Go to https://github.com/new
echo 2. Repository name: vpn-socks5-proxy
echo 3. Description: Lightweight SOCKS5 proxy for VPN access sharing
echo 4. Make it Public
echo 5. Don't initialize with README (we already have one)
echo 6. Click "Create repository"
echo.

echo Step 3: Connect to GitHub
echo ================================
echo Replace 'yourusername' with your GitHub username:
echo.
set /p username="Enter your GitHub username: "
echo.

echo Adding remote origin...
git remote add origin https://github.com/%username%/vpn-socks5-proxy.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo GitHub Repository Setup Complete!
echo ========================================
echo.
echo Repository URL: https://github.com/%username%/vpn-socks5-proxy
echo.
echo Next steps:
echo 1. Update README.md with your actual GitHub username
echo 2. Add topics/tags in GitHub: socks5, proxy, vpn, networking
echo 3. Enable GitHub Pages for documentation (optional)
echo.
pause
