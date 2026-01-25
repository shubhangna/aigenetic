import socket
import unittest
from datetime import datetime

class TestGitHubIPs(unittest.TestCase):
    """Test suite to verify GitHub Pages IP addresses remain constant"""
    
    # Expected GitHub Pages IP addresses
    EXPECTED_IPS = {
        '185.199.108.153',
        '185.199.109.153',
        '185.199.110.153',
        '185.199.111.153'
    }
    
    GITHUB_DOMAIN = 'aigenetic.in'
    
    def test_github_ips_resolve_correctly(self):
        """Verify that aigenetic.in resolves to expected GitHub IPs"""
        try:
            resolved_ips = set(socket.gethostbyname_ex(self.GITHUB_DOMAIN)[2])
            print(f"\n[{datetime.now()}] Resolved IPs for {self.GITHUB_DOMAIN}: {resolved_ips}")
            
            # Check if resolved IPs match expected IPs
            self.assertEqual(
                resolved_ips,
                self.EXPECTED_IPS,
                f"IP mismatch! Expected {self.EXPECTED_IPS}, got {resolved_ips}"
            )
        except socket.gaierror as e:
            self.fail(f"DNS resolution failed for {self.GITHUB_DOMAIN}: {e}")
    
    def test_github_ips_are_accessible(self):
        """Verify that GitHub IP addresses are reachable"""
        for ip in self.EXPECTED_IPS:
            with self.subTest(ip=ip):
                try:
                    socket.create_connection((ip, 443), timeout=5)
                    print(f"✓ IP {ip} is accessible on port 443")
                except (socket.timeout, socket.error) as e:
                    self.fail(f"IP {ip} is not accessible: {e}")
    
    def test_load_expected_ips_from_file(self):
        """Verify IPs listed in gitIps file match expected IPs"""
        try:
            with open('gitIps', 'r') as f:
                file_ips = set(line.strip() for line in f if line.strip())
            
            print(f"\nIPs from gitIps file: {file_ips}")
            self.assertEqual(
                file_ips,
                self.EXPECTED_IPS,
                f"gitIps file IPs don't match! Expected {self.EXPECTED_IPS}, got {file_ips}"
            )
        except FileNotFoundError:
            self.fail("gitIps file not found")

if __name__ == '__main__':
    unittest.main(verbosity=2)