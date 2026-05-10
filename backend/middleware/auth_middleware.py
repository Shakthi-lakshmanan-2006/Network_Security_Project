import jwt
from flask import request, jsonify, g
from functools import wraps
from config import Config
from models import User
from utils.logger import auth_logger

def verify_token():
    """Verify JWT token from request"""
    token = None
    
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            parts = auth_header.split(' ')
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        except IndexError:
            return None
    
    if not token:
        return None
    
    try:
        data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return data['user_id']
    except jwt.ExpiredSignatureError:
        auth_logger.warning("Expired token used")
        return None
    except jwt.InvalidTokenError:
        auth_logger.warning("Invalid token used")
        return None
    except Exception as e:
        auth_logger.error(f"Token verification error: {e}")
        return None

def get_current_user():
    """Get current logged-in user"""
    user_id = verify_token()
    if user_id:
        try:
            user = User.objects(id=user_id).first()
            return user
        except Exception as e:
            auth_logger.error(f"Error fetching user: {e}")
            return None
    return None

def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        g.user = get_current_user()
        return f(*args, **kwargs)
    return decorated