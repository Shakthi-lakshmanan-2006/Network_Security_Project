import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root123')
    DB_NAME = os.getenv('DB_NAME', 'network_security_db')
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set True for SQL query debugging
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in seconds
    
    # Security
    E2EE_SECRET_KEY = os.getenv('E2EE_SECRET_KEY', 'gD9tPj6pWwY3lZ2kL8fQ4mN1vR5cX7sT0bH4yJ8kM3w=') # Fernet Key
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    BLOCK_DURATION_MINUTES = int(os.getenv('BLOCK_DURATION_MINUTES', 30))
    
    # Email Configuration
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'admin@yourdomain.com')
    
    # Twilio (SMS Alerts)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    ALERT_PHONE = os.getenv('ALERT_PHONE', '')
    
    # API Keys
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')
    ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY', '')
    
    # Network Monitoring
    MONITOR_INTERFACE = os.getenv('MONITOR_INTERFACE', 'Ethernet')
    PACKET_CAPTURE_LIMIT = int(os.getenv('PACKET_CAPTURE_LIMIT', 1000))
    ENABLE_REAL_TIME_MONITORING = os.getenv('ENABLE_REAL_TIME_MONITORING', 'false').lower() == 'true'
    
    # File Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'pcap'}