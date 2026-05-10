from flask import Blueprint, request, jsonify
from models import Alert
from database import db

alert_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@alert_bp.route('', methods=['GET'])
def get_alerts():
    """Get all alerts with optional filters - public for dev"""
    try:
        status = request.args.get('status')
        severity = request.args.get('severity')
        alert_type = request.args.get('alert_type')
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))

        query = db.session.query(Alert)
        if status:
            query = query.filter_by(status=status)
        if severity:
            query = query.filter_by(severity=severity)
        if alert_type:
            query = query.filter_by(alert_type=alert_type)

        total = query.count()
        alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()

        return jsonify({
            'alerts': [a.to_dict() for a in alerts],
            'total': total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@alert_bp.route('/<int:alert_id>', methods=['GET'])
def get_alert_detail(alert_id):
    """Get single alert details"""
    alert = db.session.query(Alert).get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    return jsonify({'alert': alert.to_dict()}), 200

@alert_bp.route('/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    data = request.get_json() or {}
    alert = db.session.query(Alert).get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    try:
        from datetime import datetime
        alert.status = 'resolved'
        alert.resolved_by = data.get('resolved_by', 'Admin')
        alert.resolved_at = datetime.utcnow()
        alert.notes = data.get('notes', '')
        db.session.commit()
        return jsonify({'message': 'Alert resolved', 'alert': alert.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@alert_bp.route('/simulate', methods=['POST'])
def simulate_attack():
    """Simulates a sophisticated cyber attack burst for demonstration purposes"""
    try:
        from models import NetworkLog
        import random
        from datetime import datetime, timedelta
        
        data = request.get_json() or {}
        scenario = data.get('scenario', 'mixed')
        
        # 1. Generate Security Alerts
        attacks = [
            {'type': 'brute_force', 'severity': 'high', 'desc': 'Multiple failed SSH login attempts detected.'},
            {'type': 'port_scan', 'severity': 'medium', 'desc': 'Sequential port probing detected on internal subnet.'},
            {'type': 'unauthorized_access', 'severity': 'critical', 'desc': 'Suspicious database access attempt from unknown IP.'},
            {'type': 'phishing', 'severity': 'high', 'desc': 'High-risk phishing email blocked by gateway.'}
        ]
        
        created_alerts = []
        source_ip = data.get('source_ip', f"45.33.{random.randint(1,254)}.{random.randint(1,254)}")
        
        # Add 2-3 random alerts from the list
        for attack in random.sample(attacks, random.randint(2, 3)):
            alert = Alert(
                alert_type=attack['type'],
                severity=attack['severity'],
                source_ip=source_ip,
                dest_ip='10.0.0.5',
                description=f"[SIMULATED] {attack['desc']}",
                status='active'
            )
            db.session.add(alert)
            created_alerts.append(alert)

        # 2. Generate Network Logs (to make graphs look alive)
        for i in range(10):
            log = NetworkLog(
                timestamp=datetime.utcnow() - timedelta(seconds=i*5),
                source_ip=source_ip,
                dest_ip='10.0.0.5',
                source_port=random.randint(1024, 65535),
                dest_port=random.randint(1, 1024),
                protocol=random.choice(['TCP', 'UDP', 'ICMP']),
                packet_size=random.randint(64, 1500),
                status='blocked' if random.random() > 0.7 else 'allowed'
            )
            db.session.add(log)
            
        db.session.commit()
        
        return jsonify({
            'message': 'Cyber attack simulation successful. Alerts and logs injected.',
            'alerts_created': len(created_alerts)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500