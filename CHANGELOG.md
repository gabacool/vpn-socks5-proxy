# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-17

### Added
- Initial release of VPN SOCKS5 Proxy
- Core SOCKS5 proxy server implementation
- **Fixed DNS resolution bug** - properly parses nslookup output to get actual IP instead of DNS server IP
- VPN-aware DNS resolution with automatic VPN DNS server detection
- Multi-threaded connection handling for concurrent clients
- Automatic network interface detection
- Comprehensive logging and connection statistics
- Windows management scripts (start, stop, status, create shortcut)
- Cross-platform startup scripts (Windows .bat and Linux/Mac .sh)
- FoxyProxy configuration examples
- Connection testing utilities
- Detailed documentation (Setup, Troubleshooting, Advanced)
- MIT License

### Features
- ✅ **DNS Resolution Fix**: Correctly parses DNS responses from VPN servers
- ✅ **VPN-First DNS**: Prioritizes VPN DNS servers for proper internal domain resolution
- ✅ **Fallback Support**: Automatically falls back to system DNS if VPN DNS fails
- ✅ **Multi-threaded**: Handles multiple concurrent connections efficiently
- ✅ **Auto-detection**: Automatically detects network interfaces and VPN DNS servers
- ✅ **Cross-platform**: Works on Windows, Mac, Linux, and mobile devices
- ✅ **Easy Management**: Simple scripts for start/stop/status checking

### Technical Details
- **Language**: Python 3.6+
- **Protocol**: SOCKS5 (RFC 1928)
- **Default Port**: 1081
- **DNS Support**: VPN DNS servers with system DNS fallback
- **Connection Handling**: Multi-threaded with proper cleanup
- **Logging**: Timestamped logs with connection statistics

### Tested Environments
- **Windows 11**: Cisco AnyConnect, OpenVPN, WireGuard, PAN GlobalProtect
- **macOS**: Chrome + FoxyProxy, Safari + System Proxy
- **Linux**: curl/wget, system proxy configuration
- **Mobile**: iOS System Proxy, Android Chrome + Proxy

### Known Issues
- Unicode output may cause issues on some Windows systems (use ASCII version)
- Performance may vary based on VPN server location and network conditions
- Some corporate firewalls may block SOCKS5 traffic

### Installation
```bash
git clone https://github.com/yourusername/vpn-socks5-proxy.git
cd vpn-socks5-proxy
python socks5_proxy.py
```

### Quick Start
1. Ensure VPN is connected on Windows machine
2. Run `management\start_proxy.bat`
3. Configure client with Windows IP and port 1081
4. Set proxy type to SOCKS5

---

## [Unreleased]

### Planned Features
- [ ] Web-based management interface
- [ ] Configuration file support
- [ ] Performance metrics dashboard
- [ ] Load balancing across multiple VPN connections
- [ ] Authentication support (username/password)
- [ ] Automatic failover between VPN servers
- [ ] Docker containerization
- [ ] Windows service installation
- [ ] SSL/TLS encryption for proxy connections

### Improvements
- [ ] Enhanced error handling and recovery
- [ ] Better logging with log rotation
- [ ] Memory usage optimization
- [ ] Connection pooling for better performance
- [ ] IPv6 support
- [ ] Proxy chaining support

---

## Version History

### Version Numbering
- **Major (X.0.0)**: Breaking changes, major feature additions
- **Minor (0.X.0)**: New features, backwards compatible
- **Patch (0.0.X)**: Bug fixes, small improvements

### Release Notes
Each release includes:
- Feature additions and improvements
- Bug fixes and security patches
- Performance optimizations
- Documentation updates
- Compatibility updates

---

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
