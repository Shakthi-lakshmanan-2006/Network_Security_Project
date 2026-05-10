from datetime import datetime, timedelta
import hashlib
import secrets
import json

def generate_token(length=32):
    """Generate random secure token"""
    return secrets.token_urlsafe(length)

def hash_string(text):
    """Hash string using SHA256"""
    return hashlib.sha256(text.encode()).hexdigest()

def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """Format datetime for display"""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt
    if dt:
        return dt.strftime(format_str)
    return None

def calculate_threat_score(factors):
    """Calculate threat score based on multiple factors"""
    weights = {
        'failed_attempts': 20,
        'suspicious_ports': 15,
        'blacklisted_ip': 30,
        'unusual_traffic': 15,
        'time_of_day': 5,
        'geographic_anomaly': 10,
        'known_malware': 25,
        'data_exfiltration': 20
    }
    
    score = 0
    for factor, value in factors.items():
        if factor in weights:
            if isinstance(value, bool):
                value = 1 if value else 0
            score += weights[factor] * value
    
    return min(int(score), 100)

def get_severity_level(score):
    """Determine severity based on threat score"""
    if score >= 80:
        return 'critical'
    elif score >= 60:
        return 'high'
    elif score >= 40:
        return 'medium'
    else:
        return 'low'

def paginate_results(items, page=1, per_page=20):
    """Paginate list of items"""
    page = max(1, page)
    start = (page - 1) * per_page
    end = start + per_page
    
    total_pages = (len(items) + per_page - 1) // per_page
    
    return {
        'items': items[start:end],
        'total': len(items),
        'page': page,
        'per_page': per_page,
        'total_pages': max(1, total_pages),
        'has_next': page < total_pages,
        'has_prev': page > 1
    }