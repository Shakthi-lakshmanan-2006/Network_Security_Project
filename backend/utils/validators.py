import re
from email_validator import validate_email, EmailNotValidError
import ipaddress

def validate_ip_address(ip):
    """Validate IPv4 or IPv6 address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_ip_range(ip_range):
    """Validate IP range (CIDR notation)"""
    try:
        ipaddress.ip_network(ip_range, strict=False)
        return True
    except ValueError:
        return False

def validate_email_address(email):
    """Validate email address"""
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_password(password):
    """Validate password strength (relaxed for demo)"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Password is valid"

def validate_port(port):
    """Validate port number"""
    try:
        port = int(port)
        return 1 <= port <= 65535
    except:
        return False

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscore, and hyphen"
    return True, "Valid username"

def sanitize_input(text):
    """Remove potentially harmful characters"""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', str(text))
    # Remove SQL injection patterns
    text = re.sub(r'(;|--|\'|\")', '', text)
    return text.strip()

def validate_url(url):
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None