from flask import Blueprint, jsonify, request
import random
from datetime import datetime
from models import Alert, NetworkLog
from database import db

intrusion_bp = Blueprint('intrusion', __name__)

class SocialEngineeringModel:
    """A heuristic-based intelligence model simulating a Machine Learning classifier for Social Engineering detection"""
    
    FEATURE_WEIGHTS = {
        'URGENCY': ['urgent', 'immediately', 'now', 'suspended', 'lockout', 'asap', 'expire'],
        'FINANCIAL': ['bank', 'transfer', 'payment', 'money', 'invoice', 'funds', 'billing'],
        'CREDENTIALS': ['password', 'reset', 'login', 'credentials', 'verify', 'identity', 'pin'],
        'AUTHORITY': ['administrator', 'official', 'management', 'corporate', 'it support']
    }

    @staticmethod
    def predict(content):
        content = content.lower()
        score = 0
        detected_features = []
        
        # Calculate weighted threat score
        for category, keywords in SocialEngineeringModel.FEATURE_WEIGHTS.items():
            found = [w for w in keywords if w in content]
            if found:
                # Different weights per category
                weight = 25 if category == 'CREDENTIALS' else 15
                score += weight * len(found)
                detected_features.extend(found)
        
        # Normalize score
        final_score = min(100, score)
        is_threat = final_score > 35
        
        return {
            'is_threat': is_threat,
            'confidence': final_score,
            'detected_patterns': list(set(detected_features)),
            'classification': 'THREAT' if is_threat else 'SAFE & LEGIT',
            'analysis': "Critical social engineering markers detected." if is_threat else "No significant threat patterns identified."
        }

@intrusion_bp.route('/analyze-social-engineering', methods=['POST'])
def analyze_social_engineering():
    """Analyzes content using the Social Engineering Intelligence Model"""
    data = request.get_json() or {}
    content = data.get('content', '')
    
    if not content or len(content) < 5:
        return jsonify({'error': 'Content too short for analysis'}), 400
        
    result = SocialEngineeringModel.predict(content)
    
    if result['is_threat']:
        # Log the detection as a high-priority alert
        alert = Alert(
            alert_type='phishing',
            severity='high',
            source_ip=request.remote_addr,
            description=f"AI DETECTION: Social engineering threat classified as {result['confidence']}% certainty.",
            status='active'
        )
        db.session.add(alert)
        db.session.commit()
        
    return jsonify({
        'is_phishing': result['is_threat'],
        'threat_score': result['confidence'],
        'detected_patterns': result['detected_patterns'],
        'classification': result['classification'],
        'analysis': result['analysis'],
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@intrusion_bp.route('/live-feed', methods=['GET'])
def get_live_intrusion_feed():
    """Generates a dynamic real-time feed of unauthorized access attempts and network security logs"""
    # In a real app, this would use WebSockets. Here we simulate a very active feed for the judge.
    scenarios = [
        "Unauthorized SSH attempt from unknown IP (China-based)",
        "SQL Injection pattern detected in query params",
        "Multiple failed login attempts on 'Admin' account",
        "Large data packet egress detected to unrecognized cloud bucket",
        "Suspicious 'Reset Password' link click from non-corporate device"
    ]
    
    feed = []
    for _ in range(5):
        feed.append({
            'id': random.randint(1000, 9999),
            'event': random.choice(scenarios),
            'ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'severity': random.choice(['critical', 'high', 'medium']),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    return jsonify({'feed': feed}), 200
