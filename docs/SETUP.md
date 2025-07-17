# Setup Guide - VPN SOCKS5 Proxy

This guide walks you through setting up the VPN SOCKS5 proxy for sharing VPN access between devices.

## Prerequisites

### Windows Machine (VPN Server)
- ✅ **Python 3.6+** installed
- ✅ **Active VPN connection** (any VPN client)
- ✅ **Network connectivity** to client devices

### Client Devices (Mac, Linux, Mobile)
- ✅ **SOCKS5 proxy support** (browser, system settings, or apps)
- ✅ **Network access** to Windows machine

## Step 1: Windows Setup (VPN Server)

### Download and Install
```bash
# Option 1: Clone from GitHub
git clone https://github.com/yourusername/vpn-socks5-proxy.git
cd vpn-socks5-proxy

# Option 2: Download ZIP and extract
# Download from: https://github.com/yourusername/vpn-socks5-proxy/archive/main.zip
```

### Verify Python Installation
```cmd
python --version
# Should show Python 3.6 or higher
```

### Find Your Windows IP Address
```cmd
ipconfig
# Look for your main network adapter IP (usually 192.168.x.x)
```

### Start the Proxy
```cmd
# Method 1: Double-click
management\start_proxy.bat

# Method 2: Command line
python socks5_proxy.py

# Method 3: With custom settings
python socks5_proxy.py --host 192.168.1.151 --port 1081
```

### Create Desktop Shortcut (Optional)
```cmd
management\create_shortcut.bat
```

## Step 2: Configure Windows Firewall

### Allow Python Through Firewall
1. Open **Windows Defender Firewall**
2. Click **"Allow an app or feature through Windows Defender Firewall"**
3. Click **"Change Settings"** then **"Allow another app..."**
4. Browse to Python executable (usually `C:\Python3x\python.exe`)
5. Check both **Private** and **Public** networks
6. Click **OK**

### Alternative: Manual Firewall Rule
```cmd
# Run as Administrator
netsh advfirewall firewall add rule name="VPN SOCKS5 Proxy" dir=in action=allow protocol=TCP localport=1081
```

## Step 3: Client Configuration

### Chrome/Firefox with FoxyProxy

#### Install FoxyProxy
- **Chrome**: [FoxyProxy Extension](https://chrome.google.com/webstore/detail/foxyproxy/gcknhkkoolaabfmlnjonogaaifnjlfnp)
- **Firefox**: [FoxyProxy Add-on](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy/)

#### Configure Proxy
1. Open FoxyProxy settings
2. Click **"Add"** or **"New Proxy"**
3. Configure:
   - **Title**: `VPN SOCKS5 Proxy`
   - **Type**: `SOCKS5`
   - **Proxy IP**: `192.168.1.151` (your Windows IP)
   - **Port**: `1081`
   - **Username/Password**: Leave blank
4. Enable **"Proxy DNS when using SOCKS v5"** if available
5. Save settings

#### Set Proxy Mode
- **All traffic**: Select "Use proxy for all URLs"
- **Specific sites**: Create URL patterns for VPN-only resources

### macOS System Proxy

#### Manual Configuration
1. **System Preferences** → **Network**
2. Select your network connection
3. Click **"Advanced..."** → **"Proxies"**
4. Check **"SOCKS Proxy"**
5. Enter:
   - **SOCKS Proxy Server**: `192.168.1.151:1081`
6. Click **"OK"** and **"Apply"**

#### Command Line Test
```bash
# Test connection
curl --socks5 192.168.1.151:1081 https://google.com

# Set environment variables
export https_proxy=socks5://192.168.1.151:1081
export http_proxy=socks5://192.168.1.151:1081
```

### Linux Configuration

#### System Proxy (Ubuntu/Debian)
1. **Settings** → **Network** → **Network Proxy**
2. Select **"Manual"**
3. Configure **SOCKS Host**:
   - **Host**: `192.168.1.151`
   - **Port**: `1081`
4. Apply settings

#### Command Line
```bash
# Test connection
curl --socks5 192.168.1.151:1081 https://example.com

# Environment variables
export ALL_PROXY=socks5://192.168.1.151:1081
export all_proxy=socks5://192.168.1.151:1081
```

### Mobile Devices

#### iOS
1. **Settings** → **Wi-Fi**
2. Tap the **(i)** next to your network
3. Scroll down to **"HTTP Proxy"**
4. Select **"Manual"**
5. Configure:
   - **Server**: `192.168.1.151`
   - **Port**: `1081`

#### Android
1. **Settings** → **Wi-Fi**
2. Long press your network → **"Modify network"**
3. Tap **"Advanced options"**
4. Set **Proxy** to **"Manual"**
5. Configure:
   - **Proxy hostname**: `192.168.1.151`
   - **Proxy port**: `1081`

## Step 4: Verification

### Test Connection
```bash
# Use the test script
python examples/test_connection.py

# Manual curl test
curl --socks5 192.168.1.151:1081 https://google.com

# Check VPN-specific resources
curl --socks5 192.168.1.151:1081 https://your-corporate-site.com
```

### Verify VPN Traffic
1. Check proxy logs on Windows
2. Verify you can access VPN-protected resources
3. Confirm DNS resolution works for internal domains

## Step 5: Management

### Check Status
```cmd
management\check_status.bat
```

### Stop Proxy
```cmd
management\kill_proxy.bat
```

### Restart After Reboot
```cmd
management\start_proxy.bat
```

## Common Issues

### Connection Refused
- ❌ Proxy not running on Windows
- ❌ Firewall blocking connections
- ❌ Incorrect IP address
- ❌ Port already in use

### DNS Resolution Fails
- ❌ VPN not connected on Windows
- ❌ VPN DNS servers not accessible
- ❌ Client not using proxy for DNS

### Slow Performance
- ❌ Network congestion
- ❌ VPN server overloaded
- ❌ Too many concurrent connections

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Advanced Configuration

### Custom DNS Servers
```bash
python socks5_proxy.py --dns 8.8.8.8 1.1.1.1
```

### Custom Listen Address
```bash
python socks5_proxy.py --host 0.0.0.0 --port 8080
```

### Multiple Network Interfaces
```bash
# Listen on specific interface only
python socks5_proxy.py --host 192.168.1.151
```

## Security Considerations

1. **Network Access**: Only allow trusted devices on your network
2. **Firewall Rules**: Restrict proxy access to specific IP ranges
3. **VPN Security**: Ensure your VPN connection is secure and trusted
4. **Monitoring**: Monitor proxy logs for unusual activity

## Next Steps

- Set up automatic startup: [Auto-start configuration](ADVANCED.md#auto-start)
- Configure URL patterns: [Pattern matching guide](ADVANCED.md#url-patterns)
- Monitor usage: [Logging and statistics](ADVANCED.md#monitoring)
- Load balancing: [Multiple VPN setup](ADVANCED.md#load-balancing)
