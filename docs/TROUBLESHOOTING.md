# Troubleshooting Guide - VPN SOCKS5 Proxy

This guide helps you diagnose and fix common issues with the VPN SOCKS5 proxy.

## 🔍 Quick Diagnosis

### Check Proxy Status
```cmd
# Windows
management\check_status.bat

# Manual check
netstat -ano | findstr :1081
```

### Test Connection
```bash
# Auto-detect and test
python examples/test_connection.py

# Manual test
curl --socks5 192.168.1.151:1081 https://google.com
```

## 🚨 Common Issues

### Issue 1: Connection Refused

**Symptoms:**
- `curl: (7) Failed to connect to 192.168.1.151 port 1081: Connection refused`
- Browser shows "Proxy connection failed"
- FoxyProxy shows red/error status

**Diagnosis:**
```cmd
# Check if proxy is running
netstat -ano | findstr :1081

# Check for Python process
tasklist | findstr python.exe
```

**Solutions:**

#### A. Start the Proxy
```cmd
# Start proxy server
management\start_proxy.bat

# Or directly
python socks5_proxy.py
```

#### B. Fix Firewall Issues
```cmd
# Allow Python through firewall (run as admin)
netsh advfirewall firewall add rule name="SOCKS5 Proxy" dir=in action=allow protocol=TCP localport=1081

# Or disable firewall temporarily to test
netsh advfirewall set allprofiles state off
```

#### C. Check Port Usage
```cmd
# Find what's using port 1081
netstat -ano | findstr :1081

# Kill conflicting process
taskkill /PID [PID_NUMBER] /F
```

### Issue 2: DNS Resolution Failures

**Symptoms:**
- "Host not found" errors
- Can connect to IPs but not domain names
- Corporate/internal sites don't resolve

**Diagnosis:**
```cmd
# Test DNS resolution manually
nslookup your-internal-site.com 10.19.1.23

# Check VPN DNS settings
ipconfig /all
```

**Solutions:**

#### A. Verify VPN DNS
```cmd
# Check VPN adapter DNS settings
ipconfig /all | findstr /A:DNS

# Test VPN DNS servers
ping 10.19.1.23
ping 10.36.1.53
```

#### B. Fix DNS Configuration
```python
# Edit socks5_proxy.py - update VPN_DNS_SERVERS
VPN_DNS_SERVERS = [
    '10.19.1.23',    # Your VPN DNS
    '10.36.1.53',    # Backup VPN DNS
    '8.8.8.8'        # Public DNS fallback
]
```

#### C. Enable Proxy DNS
- **FoxyProxy**: Enable "Proxy DNS when using SOCKS v5"
- **System Proxy**: Ensure DNS goes through proxy

### Issue 3: VPN Not Connected

**Symptoms:**
- DNS resolution fails for internal domains
- Can't access VPN-protected resources
- Public sites work but corporate sites don't

**Diagnosis:**
```cmd
# Check VPN connection status
ipconfig | findstr "PANGP\|OpenVPN\|TAP"

# Test VPN connectivity
ping internal-server.company.com
```

**Solutions:**

#### A. Connect to VPN
1. Start your VPN client (AnyConnect, OpenVPN, etc.)
2. Ensure connection is established
3. Verify you can access internal resources directly

#### B. Verify VPN Routes
```cmd
# Check routing table
route print

# Look for VPN routes (usually 0.0.0.0 via VPN adapter)
```

#### C. Test VPN DNS
```cmd
# Test internal domain resolution
nslookup internal.company.com
```

### Issue 4: Slow Performance

**Symptoms:**
- Very slow browsing through proxy
- Timeouts on large downloads
- High CPU usage on Windows machine

**Diagnosis:**
```cmd
# Check CPU usage
tasklist | findstr python.exe

# Monitor network usage
netstat -e
```

**Solutions:**

#### A. Optimize Proxy Settings
```python
# In socks5_proxy.py, increase buffer sizes
def relay_data(self, client_socket, dest_socket):
    # Increase buffer from 4096 to 65536
    data = src.recv(65536)
```

#### B. Reduce Concurrent Connections
```python
# Limit concurrent connections
server.listen(5)  # Reduce from higher number
```

#### C. Check Network Bandwidth
```cmd
# Test network speed
speedtest-cli

# Monitor network usage
netstat -e
```

### Issue 5: Authentication Issues

**Symptoms:**
- 407 Proxy Authentication Required
- Corporate sites require authentication
- NTLM/Kerberos authentication failures

**Solutions:**

#### A. Corporate Proxy Bypass
```python
# Add corporate proxy support
# This requires extending the SOCKS5 implementation
```

#### B. Use System Credentials
- Ensure Windows machine is domain-joined
- Use integrated authentication where possible

#### C. Alternative: Direct VPN Client
- Install VPN client directly on client device
- Use SOCKS5 proxy only for specific resources

### Issue 6: Mobile Device Issues

**Symptoms:**
- Mobile proxy settings don't work
- Apps bypass proxy settings
- Inconsistent behavior across apps

**Solutions:**

#### A. Per-App Proxy (Android)
```
# Use apps that support per-app proxy:
- ProxyDroid (requires root)
- Orbot (Tor-based)
- VPN apps with SOCKS5 support
```

#### B. VPN Profile (iOS)
```
# Create VPN profile with proxy settings
# Use Apple Configurator or MDM
```

#### C. Router-Level Proxy
```
# Configure router to use SOCKS5 proxy
# All devices inherit proxy settings
```

## 🔧 Advanced Troubleshooting

### Enable Debug Logging

```python
# Add to socks5_proxy.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('proxy_debug.log'),
        logging.StreamHandler()
    ]
)
```

### Network Packet Analysis

```cmd
# Install Wireshark
# Monitor traffic on port 1081
# Look for connection patterns and errors
```

### Performance Monitoring

```python
# Add connection statistics
def print_stats(self):
    print(f"Active connections: {self.active_connections}")
    print(f"Total connections: {self.total_connections}")
    print(f"DNS success rate: {self.dns_success_rate}%")
```

## 🛡️ Security Troubleshooting

### Firewall Configuration

```cmd
# Check Windows Firewall rules
netsh advfirewall firewall show rule name="SOCKS5 Proxy"

# Add specific IP range restriction
netsh advfirewall firewall add rule name="SOCKS5 Proxy Limited" dir=in action=allow protocol=TCP localport=1081 remoteip=192.168.1.0/24
```

### Access Control

```python
# Add IP whitelist to socks5_proxy.py
ALLOWED_IPS = ['192.168.1.162', '192.168.1.0/24']

def handle_client(self, client_socket, client_addr):
    if not self.is_allowed_ip(client_addr[0]):
        self.log(f"Rejected connection from {client_addr}")
        client_socket.close()
        return
```

## 📊 Monitoring and Logging

### Connection Logs

```python
# Enhanced logging
def log_connection(self, client_addr, dest_addr, status):
    with open('connections.log', 'a') as f:
        f.write(f"{time.time()},{client_addr},{dest_addr},{status}\n")
```

### Health Monitoring

```python
# Health check endpoint
def health_check(self):
    return {
        'status': 'healthy',
        'active_connections': self.active_connections,
        'uptime': time.time() - self.start_time
    }
```

## 🔄 Recovery Procedures

### Automatic Restart

```cmd
# Create restart script
@echo off
:restart
python socks5_proxy.py
echo Proxy crashed, restarting in 5 seconds...
timeout /t 5
goto restart
```

### Service Installation

```cmd
# Install as Windows service using NSSM
nssm install VPNSocksProxy "python.exe" "C:\path\to\socks5_proxy.py"
nssm set VPNSocksProxy Start SERVICE_AUTO_START
nssm start VPNSocksProxy
```

## 🔍 Error Code Reference

### SOCKS5 Error Codes
- `0x00`: Success
- `0x01`: General SOCKS server failure
- `0x02`: Connection not allowed by ruleset
- `0x03`: Network unreachable
- `0x04`: Host unreachable
- `0x05`: Connection refused
- `0x06`: TTL expired
- `0x07`: Command not supported
- `0x08`: Address type not supported

### Common Windows Error Codes
- `10061`: Connection refused (proxy not running)
- `10060`: Connection timeout (firewall/network issue)
- `10054`: Connection reset by peer (proxy crashed)

## 📞 Getting Help

### Information to Gather
```cmd
# System information
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Network configuration
ipconfig /all > network_config.txt

# Proxy status
netstat -ano | findstr :1081 > proxy_status.txt

# Error logs
type proxy_debug.log
```

### Reporting Issues
When reporting issues, include:
1. Operating system versions (Windows + client)
2. VPN client type and version
3. Network configuration (ipconfig output)
4. Proxy logs and error messages
5. Steps to reproduce the issue

### Community Resources
- GitHub Issues: Report bugs and feature requests
- Wiki: Community troubleshooting tips
- Discussions: Q&A and usage examples

## 🏁 Emergency Reset

If everything fails, try this complete reset:

```cmd
# 1. Kill all proxy processes
taskkill /F /IM python.exe

# 2. Clear firewall rules
netsh advfirewall firewall delete rule name="SOCKS5 Proxy"

# 3. Reset network configuration
netsh winsock reset
netsh int ip reset

# 4. Restart network services
net stop "Windows Firewall"
net start "Windows Firewall"

# 5. Reboot system
shutdown /r /t 0
```

After reboot, start fresh with basic configuration and gradually add complexity.
