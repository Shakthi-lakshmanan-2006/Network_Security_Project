from flask import Blueprint, jsonify, request
from models import Alert, NetworkLog, BlockedIP, PhishingLog, User
from database import db
from utils.decorators import token_required
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics - public endpoint for dev, add @token_required for production"""
    try:
        # Active alerts
        active_alerts = db.session.query(Alert).filter_by(status='active').count()
        
        # Blocked IPs
        blocked_ips = db.session.query(BlockedIP).count()
        
        # Total network logs (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(hours=24)
        network_logs_24h = db.session.query(NetworkLog).filter(
            NetworkLog.timestamp > yesterday
        ).count()
        
        # Phishing emails caught
        phishing_caught = db.session.query(PhishingLog).filter_by(flagged=True).count()
        
        # Recent alerts (last 5)
        recent_alerts = db.session.query(Alert).order_by(
            Alert.timestamp.desc()
        ).limit(5).all()
        
        # Protocol distribution
        protocol_stats = db.session.query(
            NetworkLog.protocol,
            func.count(NetworkLog.id).label('count')
        ).group_by(NetworkLog.protocol).all()
        
        # Severity distribution
        severity_stats = db.session.query(
            Alert.severity,
            func.count(Alert.id).label('count')
        ).group_by(Alert.severity).all()
        
        # Alert type distribution
        alert_type_stats = db.session.query(
            Alert.alert_type,
            func.count(Alert.id).label('count')
        ).group_by(Alert.alert_type).all()

        # Total counts
        total_alerts = db.session.query(Alert).count()
        total_network_logs = db.session.query(NetworkLog).count()
        
        return jsonify({
            'active_alerts': active_alerts,
            'blocked_ips': blocked_ips,
            'network_logs_24h': network_logs_24h,
            'phishing_caught': phishing_caught,
            'total_alerts': total_alerts,
            'total_network_logs': total_network_logs,
            'recent_alerts': [alert.to_dict() for alert in recent_alerts],
            'charts': {
                'protocols': [
                    {'protocol': p[0] or 'Unknown', 'count': p[1]}
                    for p in protocol_stats
                ],
                'severities': [
                    {'severity': s[0], 'count': s[1]}
                    for s in severity_stats
                ],
                'alert_types': [
                    {'type': a[0], 'count': a[1]}
                    for a in alert_type_stats
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/timeline', methods=['GET'])
def get_timeline():
    """Get alert timeline data for charts"""
    try:
        hours = int(request.args.get('hours', 24))
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        # Alerts over time
        alerts = db.session.query(
            func.date_format(Alert.timestamp, '%Y-%m-%d %H:00:00').label('hour'),
            func.count(Alert.id).label('count')
        ).filter(
            Alert.timestamp > time_threshold
        ).group_by('hour').all()
        
        return jsonify({
            'timeline': [
                {'time': a[0], 'count': a[1]}
                for a in alerts
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500