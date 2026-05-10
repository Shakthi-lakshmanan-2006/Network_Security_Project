from flask import Blueprint, request, jsonify
from models import PhishingLog
from database import db

phishing_bp = Blueprint('phishing', __name__, url_prefix='/api/phishing')

@phishing_bp.route('/logs', methods=['GET'])
def get_phishing_logs():
    """Get phishing scan logs - public for dev"""
    try:
        limit = int(request.args.get('limit', 50))
        flagged_only = request.args.get('flagged', 'false').lower() == 'true'

        query = db.session.query(PhishingLog)
        if flagged_only:
            query = query.filter_by(flagged=True)

        total = query.count()
        logs = query.order_by(PhishingLog.timestamp.desc()).limit(limit).all()

        return jsonify({
            'logs': [log.to_dict() for log in logs],
            'total': total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@phishing_bp.route('/scan', methods=['POST'])
def scan_email():
    """Scan email content for phishing indicators"""
    data = request.get_json() or {}
    required_fields = ['sender', 'subject', 'body']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Sender, subject, and body required'}), 400

    # Simple in-app phishing heuristics (no external service needed)
    body = data.get('body', '')
    subject = data.get('subject', '')
    sender = data.get('sender', '')

    indicators = []
    threat_score = 0

    phishing_keywords = ['verify your account', 'click here', 'urgent', 'suspended', 
                         'confirm password', 'limited time', 'act now', 'prize', 'won']
    for kw in phishing_keywords:
        if kw.lower() in body.lower() or kw.lower() in subject.lower():
            indicators.append(f"Keyword detected: '{kw}'")
            threat_score += 15

    import re
    urls = re.findall(r'https?://[^\s]+', body)
    flagged = threat_score >= 30

    try:
        log = PhishingLog(
            email_from=sender,
            email_to=data.get('recipient', 'unknown'),
            subject=subject,
            body=body[:500],
            threat_score=min(threat_score, 100),
            flagged=flagged,
            details={'indicators': indicators},
            urls_found=urls,
            malicious_urls=[],
            indicators=indicators
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({
            'result': {
                'threat_score': min(threat_score, 100),
                'flagged': flagged,
                'indicators': indicators,
                'urls_found': urls
            },
            'log_id': log.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500