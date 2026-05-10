from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from utils.logger import logger

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return jsonify({'error': 'Token validation failed'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        from models import User
        from database import db
        
        try:
            user = db.session.query(User).filter_by(id=current_user).first()
            if not user or user.role != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
        except Exception as e:
            logger.error(f"Admin check error: {e}")
            return jsonify({'error': 'Authorization failed'}), 500
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def analyst_or_admin_required(f):
    """Decorator to require analyst or admin role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        from models import User
        from database import db
        
        try:
            user = db.session.query(User).filter_by(id=current_user).first()
            if not user or user.role not in ['admin', 'analyst']:
                return jsonify({'error': 'Analyst or Admin access required'}), 403
        except Exception as e:
            logger.error(f"Role check error: {e}")
            return jsonify({'error': 'Authorization failed'}), 500
        
        return f(current_user, *args, **kwargs)
    
    return decorated