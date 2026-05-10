import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app
from database import db
from models import User, Alert, NetworkLog
from datetime import datetime, timedelta

def seed():
    with app.app_context():
        # 1. Sync Schema
        print("Syncing database schema...")
        from sqlalchemy import text
        try:
            db.session.execute(text("ALTER TABLE users ADD COLUMN encrypted_data TEXT"))
            db.session.commit()
        except: db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE users ADD COLUMN public_key TEXT"))
            db.session.commit()
        except: db.session.rollback()
        db.create_all()

        # 2. Create Default Admin
        if not User.query.filter_by(username='admin').first():
            print("Creating default admin user...")
            admin = User(username='admin', email='admin@netsec.local', role='admin')
            admin.set_password('admin123')
            admin.encrypted_data = "E2EE-Master-Key-Active" # Mock encrypted data
            db.session.add(admin)
        
        # 3. Add some Mock Alerts for the Dashboard
        if Alert.query.count() == 0:
            print("Seeding mock alerts...")
            alerts = [
                Alert(alert_type='unauthorized_access', severity='critical', source_ip='192.168.1.105', description='Multiple failed SSH attempts'),
                Alert(alert_type='brute_force', severity='high', source_ip='45.33.22.11', description='Brute force attack on login portal'),
                Alert(alert_type='phishing', severity='medium', source_ip='unknown', description='Malicious link detected in incoming mail'),
            ]
            db.session.bulk_save_objects(alerts)

        db.session.commit()
        print("✅ Database successfully seeded!")
        print("\nLogin Credentials:")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    seed()
