from flask import Blueprint, request, jsonify
from models import NetworkLog, BlockedIP
from database import db
from datetime import datetime, timedelta

network_bp = Blueprint('network', __name__, url_prefix='/api/network')

@network_bp.route('/logs', methods=['GET'])
def get_network_logs():
    """Get network traffic logs - public for dev"""
    try:
        limit = int(request.args.get('limit', 100))
        status = request.args.get('status')
        protocol = request.args.get('protocol')

        query = db.session.query(NetworkLog)
        if status:
            query = query.filter_by(status=status)
        if protocol:
            query = query.filter_by(protocol=protocol)

        total = query.count()
        logs = query.order_by(NetworkLog.timestamp.desc()).limit(limit).all()

        return jsonify({
            'logs': [log.to_dict() for log in logs],
            'total': total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/blocked', methods=['GET'])
def get_blocked_ips():
    """Get list of blocked IPs"""
    try:
        blocked = db.session.query(BlockedIP).order_by(BlockedIP.blocked_at.desc()).all()
        return jsonify({'blocked_ips': [b.to_dict() for b in blocked]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/block', methods=['POST'])
def block_ip():
    """Block an IP address"""
    data = request.get_json() or {}
    if 'ip_address' not in data or 'reason' not in data:
        return jsonify({'error': 'IP address and reason required'}), 400
    try:
        duration_minutes = int(data.get('duration', 30))
        blocked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        existing = db.session.query(BlockedIP).filter_by(ip_address=data['ip_address']).first()
        if existing:
            return jsonify({'error': 'IP already blocked'}), 409
        block = BlockedIP(
            ip_address=data['ip_address'],
            reason=data['reason'],
            blocked_until=blocked_until,
            blocked_by=data.get('blocked_by', 'Admin')
        )
        db.session.add(block)
        db.session.commit()
        return jsonify({'message': f"IP {data['ip_address']} blocked", 'block': block.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@network_bp.route('/unblock/<int:block_id>', methods=['DELETE'])
def unblock_ip(block_id):
    """Unblock an IP address"""
    try:
        block = db.session.query(BlockedIP).get(block_id)
        if not block:
            return jsonify({'error': 'Block record not found'}), 404
        ip_address = block.ip_address
        db.session.delete(block)
        db.session.commit()
        return jsonify({'message': f'IP {ip_address} unblocked successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500