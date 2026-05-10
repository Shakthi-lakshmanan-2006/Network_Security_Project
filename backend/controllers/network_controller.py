from models import NetworkLog, BlockedIP
from database import db
from datetime import datetime, timedelta
from utils.logger import network_logger

class NetworkController:

    @staticmethod
    def get_network_logs(limit=100, status=None, protocol=None):
        """Fetch network logs from MySQL"""
        try:
            query = NetworkLog.query
            
            if status:
                query = query.filter_by(status=status)
            if protocol:
                query = query.filter_by(protocol=protocol)
            
            logs = query.order_by(NetworkLog.timestamp.desc()).limit(limit).all()
            return {'logs': [log.to_dict() for log in logs]}, 200
        except Exception as e:
            network_logger.error(f"Error fetching logs: {str(e)}")
            return {'error': 'Failed to retrieve logs'}, 500

    @staticmethod
    def block_malicious_ip(ip_address, reason, duration_minutes=30, blocked_by='system'):
        """Block IP address"""
        try:
            until_time = datetime.utcnow() + timedelta(minutes=duration_minutes)
            blocked_ip = BlockedIP.query.filter_by(ip_address=ip_address).first()
            
            if not blocked_ip:
                blocked_ip = BlockedIP(
                    ip_address=ip_address,
                    reason=reason,
                    blocked_until=until_time,
                    blocked_by=blocked_by
                )
                db.session.add(blocked_ip)
            else:
                blocked_ip.blocked_until = until_time
                blocked_ip.reason = reason
                blocked_ip.blocked_by = blocked_by
                
            db.session.commit()
            
            network_logger.warning(f"IP {ip_address} blocked until {until_time}")
            return {
                'message': f'IP {ip_address} blocked successfully',
                'block_details': blocked_ip.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            network_logger.error(f"Error blocking IP: {str(e)}")
            return {'error': 'Failed to block IP'}, 500

    @staticmethod
    def get_blocked_ips():
        """Retrieve blocked IPs"""
        try:
            now = datetime.utcnow()
            # Clean expired blocks
            BlockedIP.query.filter(BlockedIP.blocked_until < now).delete()
            db.session.commit()
            
            blocks = BlockedIP.query.all()
            return {'blocked_ips': [block.to_dict() for block in blocks]}, 200
        except Exception as e:
            network_logger.error(f"Error fetching blocked IPs: {str(e)}")
            return {'error': 'Failed to retrieve blocklist'}, 500