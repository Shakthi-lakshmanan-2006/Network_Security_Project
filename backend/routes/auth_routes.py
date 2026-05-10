from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController
from middleware.rate_limiter import rate_limit
from utils.decorators import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=300)
def register():
    data = request.get_json() or {}
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    res, status = AuthController.register_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user'),
        sensitive_data=data.get('sensitive_data')
    )
    return jsonify(res), status

@auth_bp.route('/login', methods=['POST'])
@rate_limit(max_requests=10, window_seconds=60)
def login():
    data = request.get_json() or {}
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Credentials omitted'}), 400
    
    res, status = AuthController.login_user(
        username=data['username'],
        password=data['password']
    )
    return jsonify(res), status