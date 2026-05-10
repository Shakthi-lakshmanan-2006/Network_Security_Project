import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name='network_security', log_file=None, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    # Create logs directory if not exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file is None:
        log_file = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    return logger

# Create main logger
logger = setup_logger('network_security')

# Create specialized loggers
auth_logger = setup_logger('auth', 'logs/auth.log')
network_logger = setup_logger('network', 'logs/network.log')
alert_logger = setup_logger('alerts', 'logs/alerts.log')