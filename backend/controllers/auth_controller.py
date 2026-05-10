import jwt
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from models import User
from database import db
from config import Config
from utils.validators import validate_email_address, validate_password
from utils.logger import auth_logger

class AuthController:
    
    @staticmethod
    def get_cipher():
        """Returns the Fernet cipher suite using the E2EE key"""
        return Fernet(Config.E2EE_SECRET_KEY.encode())

    @staticmethod
    def register_user(username, email, password, role='user', sensitive_data=None):
        """Register new user in MySQL with E2EE for sensitive data"""
        try:
            if not validate_email_address(email):
                return {'error': 'Invalid email address format'}, 400
            
            is_valid, message = validate_password(password)
            if not is_valid:
                return {'error': message}, 400
            
            if User.query.filter_by(username=username).first():
                return {'error': 'Username already exists'}, 400
            
            if User.query.filter_by(email=email).first():
                return {'error': 'Email already registered'}, 400
            
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            
            # E2EE WhatsApp Style Encryption
            if sensitive_data:
                cipher = AuthController.get_cipher()
                encrypted = cipher.encrypt(sensitive_data.encode('utf-8'))
                user.encrypted_data = encrypted.decode('utf-8')
            
            db.session.add(user)
            db.session.commit()
            
            auth_logger.info(f"User registered: {username} ({role})")
            return {
                'message': 'User registered successfully',
                'user': user.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            auth_logger.error(f"Registration error: {error_msg}")
            # In development, returning the real error helps debugging missing DB columns
            return {'error': f'Registration failed: {error_msg}'}, 500
    
    @staticmethod
    def login_user(username, password):
        """Authenticate user, return JWT token and decrypted E2EE data"""
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                return {'error': 'Invalid credentials'}, 401
            
            # Check account lockout
            if user.locked_until and user.locked_until > datetime.utcnow():
                time_left = int((user.locked_until - datetime.utcnow()).total_seconds() / 60)
                return {'error': f'Account locked. Try again in {max(1, time_left)} minutes.'}, 403
            
            if not user.check_password(password):
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= Config.MAX_LOGIN_ATTEMPTS:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=Config.BLOCK_DURATION_MINUTES)
                    auth_logger.warning(f"Account locked: {username}")
                db.session.commit()
                return {'error': 'Invalid credentials'}, 401
            
            # Reset on successful login
            user.failed_login_attempts = 0
            user.locked_until = None
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Decrypt E2EE data
            decrypted_data = None
            if user.encrypted_data:
                cipher = AuthController.get_cipher()
                try:
                    decrypted_data = cipher.decrypt(user.encrypted_data.encode('utf-8')).decode('utf-8')
                except Exception as e:
                    auth_logger.error(f"Decryption failed for user {username}: {str(e)}")
            
            # Generate JWT
            token = jwt.encode(
                {
                    'user_id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
                },
                Config.JWT_SECRET_KEY,
                algorithm='HS256'
            )
            
            user_dict = user.to_dict()
            # Inject the decrypted data into the response (only returned on login)
            user_dict['decrypted_sensitive_data'] = decrypted_data
            
            auth_logger.info(f"Successful login: {username}")
            return {
                'message': 'Login successful',
                'token': token,
                'user': user_dict
            }, 200
            
        except Exception as e:
            error_msg = str(e)
            auth_logger.error(f"Login error: {error_msg}")
            return {'error': f'Login failed: {error_msg}'}, 500