#!/usr/bin/env python3
"""
VPN SOCKS5 Proxy Server
=======================

A lightweight SOCKS5 proxy server that enables VPN access sharing between 
Windows and other devices. Includes proper DNS resolution through VPN servers
and fallback to system DNS.

Features:
- VPN-aware DNS resolution with proper parsing
- Multi-threaded connection handling
- Comprehensive logging
- Automatic network interface detection
- Fallback DNS support

Author: VPN SOCKS5 Proxy Contributors
License: MIT
Repository: https://github.com/yourusername/vpn-socks5-proxy
"""

import socket
import threading
import struct
import subprocess
import sys
import time
import re
from typing import Optional, List

class VPNSocks5Proxy:
    """
    SOCKS5 proxy server optimized for VPN environments.
    
    Automatically detects VPN DNS servers and network interfaces,
    provides proper DNS resolution through VPN tunnel, and handles
    multiple concurrent connections efficiently.
    """
    
    def __init__(self, host: str = None, port: int = 1081, vpn_dns: List[str] = None):
        """
        Initialize the SOCKS5 proxy server.
        
        Args:
            host: Listen address (auto-detected if None)
            port: Listen port (default: 1081)
            vpn_dns: VPN DNS servers (auto-detected if None)
        """
        self.host = host or self._detect_listen_address()
        self.port = port
        self.vpn_dns = vpn_dns or self._detect_vpn_dns()
        self.running = True
        
        # Connection statistics
        self.stats = {
            'total_connections': 0,
            'active_connections': 0,
            'dns_queries': 0,
            'dns_failures': 0
        }
    
    def _detect_listen_address(self) -> str:
        """Auto-detect the best listening address based on network interfaces."""
        try:
            # Try to find Realtek or similar ethernet adapter for sharing
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
            lines = result.stdout.split('\n')
            
            current_adapter = None
            for line in lines:
                line = line.strip()
                if 'Ethernet adapter' in line or 'Wireless LAN adapter' in line:
                    current_adapter = line
                elif 'IPv4 Address' in line and current_adapter:
                    if 'Realtek' in current_adapter or 'USB' in current_adapter:
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip = ip_match.group(1)
                            if ip.startswith('192.168.') or ip.startswith('10.'):
                                self.log(f"Auto-detected listen address: {ip} ({current_adapter})")
                                return ip
        except Exception as e:
            self.log(f"Auto-detection failed: {e}")
        
        # Fallback to all interfaces
        return '0.0.0.0'
    
    def _detect_vpn_dns(self) -> List[str]:
        """Auto-detect VPN DNS servers from network configuration."""
        dns_servers = []
        try:
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, shell=True)
            lines = result.stdout.split('\n')
            
            in_vpn_adapter = False
            for line in lines:
                line = line.strip()
                
                # Look for VPN adapters (PANGP, OpenVPN, etc.)
                if 'Ethernet adapter' in line:
                    in_vpn_adapter = any(keyword in line for keyword in 
                                       ['PANGP', 'OpenVPN', 'TAP', 'Virtual', 'VPN'])
                elif 'DNS Servers' in line and in_vpn_adapter:
                    # Extract DNS server IPs
                    dns_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if dns_match:
                        dns_servers.append(dns_match.group(1))
                elif line.startswith((' ' * 20)) and in_vpn_adapter and dns_servers:
                    # Additional DNS servers on continuation lines
                    dns_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if dns_match:
                        dns_servers.append(dns_match.group(1))
        except Exception as e:
            self.log(f"VPN DNS detection failed: {e}")
        
        # Fallback to common VPN DNS servers
        if not dns_servers:
            dns_servers = ['10.19.1.23', '10.36.1.53', '8.8.8.8']
        
        self.log(f"Using DNS servers: {dns_servers}")
        return dns_servers
    
    def log(self, message: str) -> None:
        """Log message with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve hostname using VPN DNS servers with proper parsing.
        
        Args:
            hostname: Domain name to resolve
            
        Returns:
            Resolved IP address or None if resolution fails
        """
        self.stats['dns_queries'] += 1
        self.log(f"Resolving: {hostname}")
        
        # Try VPN DNS servers first
        for dns_server in self.vpn_dns:
            try:
                result = subprocess.run(
                    ['nslookup', hostname, dns_server],
                    capture_output=True, text=True, timeout=10, shell=True
                )
                
                if result.returncode == 0:
                    # Parse nslookup output correctly (fixed DNS parsing bug)
                    lines = result.stdout.split('\n')
                    found_name_section = False
                    
                    for line in lines:
                        line = line.strip()
                        
                        # Look for the "Name:" line to identify answer section
                        if line.startswith('Name:'):
                            found_name_section = True
                            continue
                            
                        # Get IP from answer section (not DNS server section)
                        if found_name_section and line.startswith('Address:'):
                            ip = line.split('Address:')[1].strip()
                            if ip and '.' in ip and ':' not in ip:  # IPv4 only
                                try:
                                    socket.inet_aton(ip)  # Validate IP format
                                    self.log(f"SUCCESS: {hostname} -> {ip} via {dns_server}")
                                    return ip
                                except:
                                    continue
                    
                    # Fallback parsing for different nslookup formats
                    for line in lines:
                        if 'Address:' in line and not 'Server:' in line:
                            ip = line.split('Address:')[1].strip()
                            if ip and '.' in ip and ip != dns_server and ':' not in ip:
                                try:
                                    socket.inet_aton(ip)
                                    self.log(f"SUCCESS: {hostname} -> {ip} via {dns_server} (fallback)")
                                    return ip
                                except:
                                    continue
                                    
            except Exception as e:
                self.log(f"VPN DNS {dns_server} failed: {e}")
        
        # Fallback to system DNS
        try:
            ip = socket.gethostbyname(hostname)
            self.log(f"SUCCESS: System DNS: {hostname} -> {ip}")
            return ip
        except Exception as e:
            self.log(f"ERROR: All DNS resolution failed for {hostname}: {e}")
            self.stats['dns_failures'] += 1
            return None
    
    def handle_client(self, client_socket: socket.socket, client_addr: tuple) -> None:
        """Handle individual client connection."""
        self.stats['total_connections'] += 1
        self.stats['active_connections'] += 1
        self.log(f"Client connected: {client_addr} (Total: {self.stats['total_connections']})")
        
        try:
            client_socket.settimeout(30)
            
            # SOCKS5 handshake
            data = client_socket.recv(262)
            if len(data) < 3 or data[0] != 0x05:
                self.log("ERROR: Invalid SOCKS5 handshake")
                return
            
            client_socket.send(b'\x05\x00')  # No authentication required
            self.log("Handshake complete")
            
            # Connection request
            data = client_socket.recv(262)
            if len(data) < 10 or data[0] != 0x05 or data[1] != 0x01:
                self.log("ERROR: Invalid connection request")
                return
            
            atyp = data[3]
            
            if atyp == 0x01:  # IPv4
                dest_ip = socket.inet_ntoa(data[4:8])
                dest_port = struct.unpack('>H', data[8:10])[0]
                dest_addr = dest_ip
            elif atyp == 0x03:  # Domain name
                domain_len = data[4]
                domain = data[5:5+domain_len].decode('utf-8')
                dest_port = struct.unpack('>H', data[5+domain_len:7+domain_len])[0]
                dest_addr = domain
                
                dest_ip = self.resolve_hostname(domain)
                if not dest_ip:
                    # Send DNS resolution failure response
                    response = b'\x05\x04\x00\x01' + b'\x00\x00\x00\x00' + b'\x00\x00'
                    client_socket.send(response)
                    self.log(f"ERROR: DNS resolution failed for {domain}")
                    return
            else:
                self.log(f"ERROR: Unsupported address type: {atyp}")
                return
            
            self.log(f"Connecting to: {dest_addr}:{dest_port} (IP: {dest_ip})")
            
            # Connect to destination
            try:
                dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dest_socket.settimeout(30)
                dest_socket.connect((dest_ip, dest_port))
                
                # Send success response
                response = b'\x05\x00\x00\x01' + socket.inet_aton(dest_ip) + struct.pack('>H', dest_port)
                client_socket.send(response)
                
                self.log(f"SUCCESS: Connected to {dest_addr}")
                
                # Start data relay
                self.relay_data(client_socket, dest_socket)
                
            except Exception as e:
                self.log(f"ERROR: Connection failed to {dest_ip}:{dest_port}: {e}")
                # Send connection failure response
                response = b'\x05\x01\x00\x01' + b'\x00\x00\x00\x00' + b'\x00\x00'
                client_socket.send(response)
                
        except Exception as e:
            self.log(f"ERROR: Client handler error: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
            self.stats['active_connections'] -= 1
            self.log(f"Client {client_addr} disconnected (Active: {self.stats['active_connections']})")
    
    def relay_data(self, client_socket: socket.socket, dest_socket: socket.socket) -> None:
        """Relay data bidirectionally between client and destination."""
        def forward_data(src: socket.socket, dst: socket.socket, direction: str) -> None:
            """Forward data from source to destination socket."""
            try:
                while True:
                    data = src.recv(4096)
                    if not data:
                        break
                    dst.send(data)
            except:
                pass
            finally:
                try:
                    src.close()
                    dst.close()
                except:
                    pass
        
        # Create bidirectional relay threads
        client_to_dest = threading.Thread(
            target=forward_data, 
            args=(client_socket, dest_socket, "client->dest")
        )
        dest_to_client = threading.Thread(
            target=forward_data, 
            args=(dest_socket, client_socket, "dest->client")
        )
        
        client_to_dest.daemon = True
        dest_to_client.daemon = True
        
        client_to_dest.start()
        dest_to_client.start()
        
        # Wait for both directions to complete
        client_to_dest.join()
        dest_to_client.join()
    
    def print_stats(self) -> None:
        """Print connection statistics."""
        print(f"\nConnection Statistics:")
        print(f"  Total Connections: {self.stats['total_connections']}")
        print(f"  Active Connections: {self.stats['active_connections']}")
        print(f"  DNS Queries: {self.stats['dns_queries']}")
        print(f"  DNS Failures: {self.stats['dns_failures']}")
        if self.stats['dns_queries'] > 0:
            success_rate = ((self.stats['dns_queries'] - self.stats['dns_failures']) / 
                           self.stats['dns_queries'] * 100)
            print(f"  DNS Success Rate: {success_rate:.1f}%")
    
    def start(self) -> None:
        """Start the SOCKS5 proxy server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind((self.host, self.port))
            server.listen(5)
            
            print("VPN SOCKS5 Proxy Server")
            print("=" * 40)
            print(f"Listening: {self.host}:{self.port}")
            print(f"VPN DNS: {', '.join(self.vpn_dns)}")
            print(f"Platform: {sys.platform}")
            print()
            print("Client Configuration:")
            print(f"  SOCKS Host: {self.host}")
            print(f"  SOCKS Port: {self.port}")
            print(f"  Type: SOCKS5")
            print()
            print("Press Ctrl+C to stop")
            print("=" * 40)
            
            while self.running:
                try:
                    client_socket, client_addr = server.accept()
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    self.log("Shutdown requested")
                    break
                except Exception as e:
                    if self.running:
                        self.log(f"Accept error: {e}")
        
        except Exception as e:
            print(f"ERROR: Server startup failed: {e}")
            print("Try running as administrator or check if port is already in use")
        finally:
            self.running = False
            server.close()
            self.print_stats()
            print("VPN SOCKS5 proxy stopped")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='VPN SOCKS5 Proxy Server')
    parser.add_argument('--host', help='Listen address (auto-detected if not specified)')
    parser.add_argument('--port', type=int, default=1081, help='Listen port (default: 1081)')
    parser.add_argument('--dns', nargs='+', help='VPN DNS servers (auto-detected if not specified)')
    parser.add_argument('--version', action='version', version='VPN SOCKS5 Proxy 1.0.0')
    
    args = parser.parse_args()
    
    try:
        proxy = VPNSocks5Proxy(host=args.host, port=args.port, vpn_dns=args.dns)
        proxy.start()
    except KeyboardInterrupt:
        print("\nShutdown requested")
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
