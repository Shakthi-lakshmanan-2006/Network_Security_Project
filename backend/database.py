from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config
import logging

logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating database tables: {e}")

def test_connection():
    """Test MySQL database connection"""
    try:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        connection.close()
        logger.info("✅ MySQL connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ MySQL connection failed: {e}")
        return False