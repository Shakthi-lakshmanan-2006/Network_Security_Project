from database import db
from datetime import datetime
import bcrypt
import json

# ==================== USER MODEL ====================
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', 'analyst'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    # E2EE / Encryption Fields (WhatsApp-style)
    encrypted_data = db.Column(db.Text)  # Symmetrically encrypted sensitive info
    public_key = db.Column(db.Text)      # Optional: for public-key cryptography
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                self.password_hash.encode('utf-8')
            )
        except:
            return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'encrypted_data': self.encrypted_data,
            'public_key': self.public_key
        }


# ==================== NETWORK LOG MODEL ====================
class NetworkLog(db.Model):
    __tablename__ = 'network_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    source_ip = db.Column(db.String(45), nullable=False, index=True)
    dest_ip = db.Column(db.String(45), index=True)
    source_port = db.Column(db.Integer)
    dest_port = db.Column(db.Integer)
    protocol = db.Column(db.String(10))
    packet_size = db.Column(db.Integer)
    status = db.Column(db.String(20), default='allowed', index=True)
    action_taken = db.Column(db.String(50))
    threat_level = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'source_ip': self.source_ip,
            'dest_ip': self.dest_ip,
            'source_port': self.source_port,
            'dest_port': self.dest_port,
            'protocol': self.protocol,
            'packet_size': self.packet_size,
            'status': self.status,
            'action_taken': self.action_taken,
            'threat_level': self.threat_level
        }


# ==================== ALERT MODEL ====================
class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    alert_type = db.Column(
        db.Enum('brute_force', 'port_scan', 'phishing', 'malware', 'ddos', 
                'unauthorized_access', 'data_exfiltration', 'suspicious_activity'),
        nullable=False,
        index=True
    )
    severity = db.Column(
        db.Enum('critical', 'high', 'medium', 'low'),
        nullable=False,
        index=True
    )
    source_ip = db.Column(db.String(45), index=True)
    dest_ip = db.Column(db.String(45))
    description = db.Column(db.Text)
    details = db.Column(db.JSON)
    status = db.Column(
        db.Enum('active', 'investigating', 'resolved', 'false_positive'),
        default='active',
        index=True
    )
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'alert_type': self.alert_type,
            'severity': self.severity,
            'source_ip': self.source_ip,
            'dest_ip': self.dest_ip,
            'description': self.description,
            'details': self.details,
            'status': self.status,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by,
            'notes': self.notes
        }


# ==================== BLOCKED IP MODEL ====================
class BlockedIP(db.Model):
    __tablename__ = 'blocked_ips'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False, index=True)
    reason = db.Column(db.Text, nullable=False)
    blocked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    blocked_until = db.Column(db.DateTime, index=True)
    auto_unblock = db.Column(db.Boolean, default=True)
    blocked_by = db.Column(db.String(50), default='system')
    threat_score = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'reason': self.reason,
            'blocked_at': self.blocked_at.isoformat(),
            'blocked_until': self.blocked_until.isoformat() if self.blocked_until else None,
            'auto_unblock': self.auto_unblock,
            'blocked_by': self.blocked_by,
            'threat_score': self.threat_score
        }


# ==================== PHISHING LOG MODEL ====================
class PhishingLog(db.Model):
    __tablename__ = 'phishing_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    email_from = db.Column(db.String(100), nullable=False, index=True)
    email_to = db.Column(db.String(100))
    subject = db.Column(db.Text)
    body = db.Column(db.Text)
    threat_score = db.Column(db.Integer, default=0, index=True)
    flagged = db.Column(db.Boolean, default=False, index=True)
    details = db.Column(db.JSON)
    urls_found = db.Column(db.JSON)  # Store as JSON array
    malicious_urls = db.Column(db.JSON)
    indicators = db.Column(db.JSON)
    action_taken = db.Column(db.String(50), default='quarantined')
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'email_from': self.email_from,
            'email_to': self.email_to,
            'subject': self.subject,
            'threat_score': self.threat_score,
            'flagged': self.flagged,
            'details': self.details,
            'urls_found': self.urls_found or [],
            'malicious_urls': self.malicious_urls or [],
            'indicators': self.indicators or [],
            'action_taken': self.action_taken
        }


# ==================== TRAINING PROGRESS MODEL ====================
class TrainingProgress(db.Model):
    __tablename__ = 'training_progress'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.String(50), nullable=False, index=True)
    course_name = db.Column(db.String(100))
    completed_modules = db.Column(db.JSON)  # Array of module IDs
    quiz_scores = db.Column(db.JSON)  # Array of score objects
    completion_percentage = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    time_spent = db.Column(db.Integer, default=0)  # in minutes
    
    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='unique_user_course'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course_name': self.course_name,
            'completed_modules': self.completed_modules or [],
            'quiz_scores': self.quiz_scores or [],
            'completion_percentage': self.completion_percentage,
            'last_accessed': self.last_accessed.isoformat(),
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_spent': self.time_spent
        }


# ==================== SYSTEM CONFIG MODEL ====================
class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    setting_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    setting_value = db.Column(db.JSON)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'setting_name': self.setting_name,
            'setting_value': self.setting_value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat(),
            'updated_by': self.updated_by
        }


# ==================== THREAT INTELLIGENCE MODEL ====================
class ThreatIntelligence(db.Model):
    __tablename__ = 'threat_intelligence'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False, index=True)
    reputation_score = db.Column(db.Integer, default=0, index=True)
    is_malicious = db.Column(db.Boolean, default=False, index=True)
    country = db.Column(db.String(100))
    isp = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    threat_types = db.Column(db.JSON)  # Array of threat types
    reports_count = db.Column(db.Integer, default=0)
    source = db.Column(db.String(50))
    raw_data = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'reputation_score': self.reputation_score,
            'is_malicious': self.is_malicious,
            'country': self.country,
            'isp': self.isp,
            'last_seen': self.last_seen.isoformat(),
            'threat_types': self.threat_types or [],
            'reports_count': self.reports_count,
            'source': self.source
        }