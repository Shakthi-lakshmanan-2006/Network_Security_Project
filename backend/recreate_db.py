from app import app
from database import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate():
    with app.app_context():
        try:
            logger.info("Dropping all tables...")
            db.drop_all()
            logger.info("Creating all tables...")
            db.create_all()
            logger.info("✅ Database recreated successfully with new schema (E2EE columns added).")
        except Exception as e:
            logger.error(f"❌ Failed to recreate database: {e}")

if __name__ == '__main__':
    recreate()
