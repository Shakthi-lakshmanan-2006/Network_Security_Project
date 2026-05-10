import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app
from database import db
from sqlalchemy import text

try:
    with app.app_context():
        db.session.execute(text('ALTER TABLE users ADD COLUMN encrypted_data TEXT'))
        db.session.execute(text('ALTER TABLE users ADD COLUMN public_key TEXT'))
        db.session.commit()
        print("Success")
except Exception as e:
    print(f"Failed or already exists: {e}")
