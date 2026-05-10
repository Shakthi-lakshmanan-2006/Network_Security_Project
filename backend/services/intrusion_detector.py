from collections import defaultdict
import time
from services.alert_manager import AlertManager
from utils.logger import network_logger

class IntrusionDetector:
    
    def __init__(self):
        # In-memory tracking
        self.login_attempts = defaultdict(list)
        self.port_scan_attempts = defaultdict(set)
        self.packet_flood = defaultdict(list)
    
    def track_login_attempt(self, ip_address, username, success=False):
        """Track failed login attempts for brute force detection"""
        now = time.time()
        
        if not success:
            self.login_attempts[ip_address].append(now)
            
            # Keep only attempts from last 60 seconds
            self.login_attempts[ip_address] = [
                t for t in self.login_attempts[ip_address]
                if now - t < 60
            ]
            
            # Trigger alert if 5+ failed attempts in 60 seconds
            if len(self.login_attempts[ip_address]) >= 5:
                AlertManager.trigger_alert(
                    alert_type='brute_force',
                    severity='high',
                    description=f"Brute force attack: {len(self.login_attempts[ip_address])} failed login attempts in 60 seconds (User: {username})",
                    source_ip=ip_address,
                    details={
                        'username': username,
                        'attempts': len(self.login_attempts[ip_address])
                    }
                )
                
                # Clear to prevent duplicate alerts
                self.login_attempts[ip_address] = []
                network_logger.warning(f"Brute force detected from {ip_address}")
                return True
        else:
            # Clear on successful login
            if ip_address in self.login_attempts:
                del self.login_attempts[ip_address]
        
        return False
    
    def track_port_access(self, ip_address, destination_port):
        """Detect port scanning activity"""
        self.port_scan_attempts[ip_address].add(destination_port)
        
        # Trigger if accessing 15+ unique ports
        if len(self.port_scan_attempts[ip_address]) >= 15:
            AlertManager.trigger_alert(
                alert_type='port_scan',
                severity='medium',
                description=f"Port scan detected: {len(self.port_scan_attempts[ip_address])} unique ports accessed",
                source_ip=ip_address,
                details={
                    'ports_scanned': list(self.port_scan_attempts[ip_address])
                }
            )
            
            # Reset counter
            self.port_scan_attempts[ip_address].clear()
            network_logger.warning(f"Port scan detected from {ip_address}")
            return True
        
        return False
    
    def track_packet_flood(self, ip_address):
        """Detect potential DDoS/flood attacks"""
        now = time.time()
        self.packet_flood[ip_address].append(now)
        
        # Keep only packets from last 10 seconds
        self.packet_flood[ip_address] = [
            t for t in self.packet_flood[ip_address]
            if now - t < 10
        ]
        
        # Trigger if 100+ packets in 10 seconds
        if len(self.packet_flood[ip_address]) >= 100:
            AlertManager.trigger_alert(
                alert_type='ddos',
                severity='critical',
                description=f"Potential DDoS attack: {len(self.packet_flood[ip_address])} packets in 10 seconds",
                source_ip=ip_address,
                details={
                    'packet_count': len(self.packet_flood[ip_address])
                }
            )
            
            self.packet_flood[ip_address] = []
            network_logger.critical(f"DDoS attack detected from {ip_address}")
            return True
        
        return False