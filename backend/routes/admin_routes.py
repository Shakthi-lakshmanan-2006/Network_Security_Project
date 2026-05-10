from flask import Blueprint, jsonify, request
from models import User, Alert, SystemConfig
from database import db
from utils.decorators import token_required, admin_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/db-sync', methods=['POST'])
def db_sync():
    """Manually trigger database synchronization (Migration)"""
    try:
        data = request.get_json() or {}
        drop_tables = data.get('drop_tables', False)
        
        if drop_tables:
            db.drop_all()
            db.create_all()
            return jsonify({'message': 'Database RECREATED (Dropped and created all tables)'}), 200
        else:
            from sqlalchemy import text
            # Manually add E2EE columns if they don't exist
            try:
                db.session.execute(text("ALTER TABLE users ADD COLUMN encrypted_data TEXT"))
                db.session.commit()
            except: 
                db.session.rollback()
            try:
                db.session.execute(text("ALTER TABLE users ADD COLUMN public_key TEXT"))
                db.session.commit()
            except: 
                db.session.rollback()
            
            db.create_all()
            return jsonify({'message': 'Database sync triggered (Encryption columns added if missing)'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    """Get all users (admin only)"""
    try:
        users = db.session.query(User).all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(current_user, user_id):
    """Update user details"""
    data = request.get_json() or {}
    
    try:
        user = db.session.query(User).get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update allowed fields
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/system/health', methods=['GET'])
@token_required
@admin_required
def system_health(current_user):
    """Get system health metrics"""
    try:
        import psutil
        
        return jsonify({
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/system/config', methods=['GET'])
@token_required
@admin_required
def get_system_config(current_user):
    """Get system configuration"""
    try:
        configs = db.session.query(SystemConfig).all()
        return jsonify({
            'configs': [config.to_dict() for config in configs]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500