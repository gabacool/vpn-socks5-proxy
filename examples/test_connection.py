#!/usr/bin/env python3
"""
VPN SOCKS5 Proxy Connection Test
================================

Test script to verify SOCKS5 proxy connectivity and DNS resolution.
Use this to troubleshoot connection issues and verify proper setup.
"""

import socket
import struct
import time
import sys

def test_socks5_connection(proxy_host, proxy_port, target_host, target_port=443):
    """
    Test SOCKS5 proxy connection to a target host.
    
    Args:
        proxy_host: SOCKS5 proxy server IP
        proxy_port: SOCKS5 proxy server port
        target_host: Target hostname to connect to
        target_port: Target port (default: 443 for HTTPS)
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    print(f"Testing SOCKS5 connection:")
    print(f"  Proxy: {proxy_host}:{proxy_port}")
    print(f"  Target: {target_host}:{target_port}")
    print("-" * 50)
    
    try:
        # Step 1: Connect to SOCKS proxy
        print("1. Connecting to SOCKS proxy...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((proxy_host, proxy_port))
        print("   SUCCESS: Connected to proxy")
        
        # Step 2: SOCKS5 handshake
        print("2. Performing SOCKS5 handshake...")
        sock.send(b'\x05\x01\x00')  # SOCKS5, 1 method, no auth
        response = sock.recv(2)
        if response == b'\x05\x00':
            print("   SUCCESS: Handshake complete")
        else:
            print(f"   ERROR: Handshake failed: {response.hex()}")
            return False
        
        # Step 3: Connection request
        print(f"3. Requesting connection to {target_host}...")
        request = b'\x05\x01\x00\x03'  # SOCKS5, CONNECT, reserved, domain
        request += bytes([len(target_host)])  # domain length
        request += target_host.encode('utf-8')  # domain
        request += struct.pack('>H', target_port)  # port
        
        sock.send(request)
        
        # Step 4: Read response
        print("4. Reading connection response...")
        response = sock.recv(10)
        if len(response) >= 2:
            status = response[1]
            if status == 0x00:
                print("   SUCCESS: Connection established!")
                print("   🎉 SOCKS proxy is working correctly!")
                
                # Step 5: Send test HTTP request
                print("5. Sending test HTTP request...")
                http_request = f"HEAD / HTTP/1.1\r\nHost: {target_host}\r\nConnection: close\r\n\r\n"
                sock.send(http_request.encode())
                
                response = sock.recv(1024)
                if response:
                    response_str = response.decode('utf-8', errors='ignore')
                    first_line = response_str.split('\r\n')[0]
                    print(f"   HTTP Response: {first_line}")
                    return True
                else:
                    print("   No HTTP response received")
                    return False
                    
            else:
                error_messages = {
                    0x01: "General SOCKS server failure",
                    0x02: "Connection not allowed by ruleset",
                    0x03: "Network unreachable", 
                    0x04: "Host unreachable",
                    0x05: "Connection refused",
                    0x06: "TTL expired",
                    0x07: "Command not supported",
                    0x08: "Address type not supported"
                }
                error_msg = error_messages.get(status, f"Unknown error code: 0x{status:02x}")
                print(f"   ERROR: {error_msg}")
                return False
        else:
            print("   ERROR: Invalid response from proxy")
            return False
            
    except socket.timeout:
        print("   ERROR: Connection timeout")
        return False
    except ConnectionRefusedError:
        print("   ERROR: Connection refused - is the proxy running?")
        return False
    except Exception as e:
        print(f"   ERROR: {e}")
        return False
    finally:
        try:
            sock.close()
        except:
            pass

def detect_proxy_host():
    """Auto-detect likely proxy host on local network."""
    try:
        # Get local IP to determine network range
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Suggest likely proxy hosts based on local IP
        if local_ip.startswith('192.168.1.'):
            return ['192.168.1.151', '192.168.1.1']
        elif local_ip.startswith('192.168.'):
            network = '.'.join(local_ip.split('.')[:-1])
            return [f'{network}.1', f'{network}.151']
        elif local_ip.startswith('10.'):
            return ['10.0.0.1', '10.1.1.1']
        else:
            return ['192.168.1.151']
    except:
        return ['192.168.1.151']

def main():
    """Main test function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test VPN SOCKS5 Proxy Connection')
    parser.add_argument('--proxy-host', help='SOCKS5 proxy host IP')
    parser.add_argument('--proxy-port', type=int, default=1081, help='SOCKS5 proxy port (default: 1081)')
    parser.add_argument('--target', default='google.com', help='Target host to test (default: google.com)')
    parser.add_argument('--port', type=int, default=443, help='Target port (default: 443)')
    
    args = parser.parse_args()
    
    # Auto-detect proxy host if not specified
    if not args.proxy_host:
        candidates = detect_proxy_host()
        print("Auto-detecting proxy host...")
        print(f"Trying candidates: {candidates}")
        print()
        
        for candidate in candidates:
            print(f"Trying {candidate}...")
            if test_socks5_connection(candidate, args.proxy_port, args.target, args.port):
                print(f"\n✅ Found working proxy at {candidate}:{args.proxy_port}")
                return 0
            print()
        
        print("❌ No working proxy found. Make sure:")
        print("  1. VPN SOCKS5 proxy is running")
        print("  2. Devices are on the same network") 
        print("  3. Firewall allows connections on port", args.proxy_port)
        return 1
    else:
        # Test specific proxy host
        success = test_socks5_connection(args.proxy_host, args.proxy_port, args.target, args.port)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
