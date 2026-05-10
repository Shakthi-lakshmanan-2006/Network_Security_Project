import threading
import time
import random
from datetime import datetime
from models import NetworkLog, BlockedIP
from database import db
from services.intrusion_detector import IntrusionDetector
from utils.logger import network_logger

# Initialize detector
detector = IntrusionDetector()

class NetworkMonitor(threading.Thread):
    
    def __init__(self):
        super(NetworkMonitor, self).__init__()
        self.daemon = True
        self.running = False
        self.use_scapy = False
    
    def run(self):
        """Start network monitoring"""
        self.running = True
        network_logger.info("🔍 Starting Network Monitor...")
        
        # Try to use Scapy for real packet capture
        try:
            from scapy.all import sniff, IP, TCP, UDP
            self.use_scapy = True
            network_logger.info("✅ Scapy initialized - Real packet capture mode")
            
            sniff(
                prn=self.process_packet,
                store=0,
                stop_filter=lambda x: not self.running
            )
            
        except Exception as e:
            network_logger.warning(f"⚠️ Scapy failed: {str(e)}")
            network_logger.info("🔄 Switching to simulation mode...")
            self.run_simulation_mode()
    
    def process_packet(self, packet):
        """Process real network packet (Scapy mode)"""
        if not self.running:
            return
        
        try:
            from scapy.all import IP, TCP, UDP
            
            if packet.haslayer(IP):
                ip_layer = packet[IP]
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
                
                # Determine protocol
                if packet.haslayer(TCP):
                    protocol = "TCP"
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                elif packet.haslayer(UDP):
                    protocol = "UDP"
                    src_port = packet[UDP].sport
                    dst_port = packet[UDP].dport
                else:
                    protocol = "OTHER"
                    src_port = None
                    dst_port = None
                
                packet_size = len(packet)
                
                # Check if IP is blocked
                blocked = db.session.query(BlockedIP).filter_by(ip_address=src_ip).first()
                status = 'blocked' if blocked else 'allowed'
                
                # Save to database
                log = NetworkLog(
                    source_ip=src_ip,
                    dest_ip=dst_ip,
                    source_port=src_port,
                    dest_port=dst_port,
                    protocol=protocol,
                    packet_size=packet_size,
                    status=status,
                    action_taken='dropped' if blocked else 'forwarded'
                )
                db.session.add(log)
                db.session.commit()
                
                # Run intrusion detection
                if not blocked and dst_port:
                    detector.track_port_access(src_ip, dst_port)
                    detector.track_packet_flood(src_ip)
                    
        except Exception as e:
            network_logger.error(f"Packet processing error: {str(e)}")
            db.session.rollback()
    
    def run_simulation_mode(self):
        """Simulate network traffic (fallback when Scapy unavailable)"""
        network_logger.info("📊 Simulation mode active - Generating mock traffic")
        
        # Sample IPs for simulation
        internal_ips = ['192.168.1.5', '192.168.1.10', '192.168.1.25', '10.0.0.12']
        external_ips = ['185.220.101.4', '45.143.201.21', '203.0.113.42', '198.51.100.88']
        local_gateway = '192.168.1.1'
        
        common_ports = [22, 80, 443, 8080, 3306, 21, 23, 25, 53, 3389]
        protocols = ["TCP", "UDP"]
        
        while self.running:
            try:
                # Randomly choose internal or external source
                if random.random() < 0.7:
                    src_ip = random.choice(internal_ips)
                else:
                    src_ip = random.choice(external_ips)
                
                dst_ip = local_gateway
                dst_port = random.choice(common_ports)
                protocol = random.choice(protocols)
                
                # Check if blocked
                blocked = db.session.query(BlockedIP).filter_by(ip_address=src_ip).first()
                status = 'blocked' if blocked else 'allowed'
                
                # Create log entry
                log = NetworkLog(
                    source_ip=src_ip,
                    dest_ip=dst_ip,
                    source_port=random.randint(49152, 65535),
                    dest_port=dst_port,
                    protocol=protocol,
                    packet_size=random.randint(40, 1500),
                    status=status,
                    action_taken='dropped' if blocked else 'forwarded',
                    threat_level=random.randint(0, 30) if not blocked else 80
                )
                
                db.session.add(log)
                db.session.commit()
                
                # Run detection on external IPs
                if not blocked and src_ip in external_ips:
                    # Occasionally trigger port scans
                    if random.random() < 0.15:
                        detector.track_port_access(src_ip, dst_port)
                
                # Sleep between packets
                time.sleep(random.uniform(0.5, 2.5))
                
            except Exception as e:
                network_logger.error(f"Simulation error: {str(e)}")
                db.session.rollback()
                time.sleep(1)
    
    def stop(self):
        """Stop network monitoring"""
        self.running = False
        network_logger.info("🛑 Network Monitor stopped")