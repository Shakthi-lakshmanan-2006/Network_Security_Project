from models import Alert
from database import db
from datetime import datetime
from utils.logger import alert_logger

class AlertController:
    
    @staticmethod
    def get_all_alerts(status=None, severity=None, alert_type=None, limit=50, skip=0):
        """Fetch filtered alerts from MySQL"""
        try:
            query = Alert.query
            
            if status:
                query = query.filter_by(status=status)
            if severity:
                query = query.filter_by(severity=severity)
            if alert_type:
                query = query.filter_by(alert_type=alert_type)
            
            total = query.count()
            alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
            
            return {
                'alerts': [alert.to_dict() for alert in alerts],
                'total': total,
                'limit': limit,
                'skip': skip
            }, 200
        except Exception as e:
            alert_logger.error(f"Error fetching alerts: {str(e)}")
            return {'error': 'Failed to retrieve alerts'}, 500

    @staticmethod
    def resolve_alert(alert_id, resolved_by, notes=None):
        """Mark alert as resolved"""
        try:
            alert = Alert.query.get(alert_id)
            if not alert:
                return {'error': 'Alert not found'}, 404
            
            alert.status = 'resolved'
            alert.resolved_at = datetime.utcnow()
            alert.resolved_by = resolved_by
            if notes:
                alert.notes = notes
            
            db.session.commit()
            
            alert_logger.info(f"Alert {alert_id} resolved by {resolved_by}")
            return {
                'message': 'Alert resolved successfully',
                'alert': alert.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            alert_logger.error(f"Error resolving alert: {str(e)}")
            return {'error': 'Failed to resolve alert'}, 500