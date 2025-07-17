#!/bin/bash
# VPN SOCKS5 Proxy Server - Linux/Mac Startup Script

echo "========================================"
echo "VPN SOCKS5 Proxy Server"
echo "========================================"
echo ""
echo "Starting proxy server..."
echo ""
echo "Proxy will be available at:"
echo "  Host: [Auto-detected]"
echo "  Port: 1081"
echo "  Type: SOCKS5"
echo ""
echo "Configure your client with the host IP shown above."
echo ""
echo "Press Ctrl+C to stop the proxy"
echo "========================================"
echo ""

# Change to script directory
cd "$(dirname "$0")/.."

# Start the proxy
python3 socks5_proxy.py

echo ""
echo "Proxy stopped."
