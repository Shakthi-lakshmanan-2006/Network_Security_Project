from models import Alert, BlockedIP
from database import db
from services.email_service import EmailService
from utils.logger import alert_logger
from datetime import datetime, timedelta

class AlertManager:
    
    @staticmethod
    def trigger_alert(alert_type, severity, description, source_ip=None, dest_ip=None, details=None):
        """Create alert, auto-block critical IPs, and send notifications"""
        try:
            # Check for duplicate recent alerts (prevent spam)
            recent_threshold = datetime.utcnow() - timedelta(minutes=5)
            recent_alert = Alert.query.filter(
                Alert.alert_type == alert_type,
                Alert.source_ip == source_ip,
                Alert.status == 'active',
                Alert.timestamp > recent_threshold
            ).first()
            
            if recent_alert:
                alert_logger.debug(f"Duplicate alert suppressed: {alert_type} from {source_ip}")
                return recent_alert
            
            # Create new alert
            alert = Alert(
                alert_type=alert_type,
                severity=severity,
                source_ip=source_ip,
                dest_ip=dest_ip,
                description=description,
                details=details or {}
            )
            
            db.session.add(alert)
            db.session.commit()
            
            alert_logger.warning(
                f"🚨 ALERT TRIGGERED: {alert_type.upper()} | "
                f"Severity: {severity} | IP: {source_ip}"
            )
            
            # Auto-block for critical/high severity threats
            if severity in ['critical', 'high'] and source_ip:
                try:
                    existing_block = BlockedIP.query.filter_by(ip_address=source_ip).first()
                    
                    if not existing_block:
                        block = BlockedIP(
                            ip_address=source_ip,
                            reason=f"Auto-blocked: {alert_type} (Severity: {severity})",
                            blocked_until=datetime.utcnow() + timedelta(minutes=30),
                            blocked_by="Auto-IPS",
                            threat_score=80 if severity == 'critical' else 60
                        )
                        db.session.add(block)
                        db.session.commit()
                        
                        alert_logger.warning(f"🔒 Auto-blocked IP: {source_ip}")
                except Exception as e:
                    alert_logger.error(f"Auto-block failed: {str(e)}")
            
            # Send email notification
            try:
                EmailService.send_security_alert(
                    alert_type=alert_type,
                    severity=severity,
                    description=description,
                    source_ip=source_ip or 'Unknown'
                )
            except Exception as e:
                alert_logger.error(f"Email notification failed: {str(e)}")
            
            return alert
            
        except Exception as e:
            db.session.rollback()
            alert_logger.error(f"Alert creation failed: {str(e)}")
            return None