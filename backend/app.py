from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import db, init_db, test_connection
from utils.logger import logger
from datetime import datetime, timezone

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize database
init_db(app)

# Import and register blueprints
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.alert_routes import alert_bp
from routes.network_routes import network_bp
from routes.phishing_routes import phishing_bp
from routes.training_routes import training_bp
from routes.admin_routes import admin_bp
from routes.intrusion_routes import intrusion_bp
from routes.chatbot_routes import chatbot_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(alert_bp)
app.register_blueprint(network_bp)
app.register_blueprint(phishing_bp)
app.register_blueprint(training_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(intrusion_bp, url_prefix='/api/intrusion')
app.register_blueprint(chatbot_bp)

# Root route
@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'project': 'Network Security and Social Engineering Alert System',
        'database': 'MySQL',
        'api_version': 'v1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'dashboard': '/api/dashboard',
            'alerts': '/api/alerts',
            'network': '/api/network',
            'phishing': '/api/phishing',
            'training': '/api/training',
            'admin': '/api/admin'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        connection_ok = test_connection()
        return jsonify({
            'status': 'healthy' if connection_ok else 'unhealthy',
            'database': 'connected' if connection_ok else 'disconnected',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200 if connection_ok else 503
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# Background network monitor initialization
from services.network_monitor import NetworkMonitor
monitor_thread = None

def start_background_monitoring():
    """Start the background network monitoring engine safely"""
    global monitor_thread
    if Config.ENABLE_REAL_TIME_MONITORING:
        try:
            monitor_thread = NetworkMonitor()
            monitor_thread.start()
            logger.info("[INFO] Network monitoring service started in background")
        except Exception as e:
            logger.error(f"Failed to start network monitor thread: {e}")
    else:
        logger.info("[WARN] Real-time monitoring disabled in config (.env)")

# Cleanup on shutdown
@app.teardown_appcontext
def shutdown_services(exception=None):
    """Cleanup on application shutdown"""
    global monitor_thread
    if monitor_thread and monitor_thread.is_alive():
        monitor_thread.stop()
        logger.info("[INFO] Network monitoring service stopped")

if __name__ == '__main__':
    logger.info("="*60)
    logger.info("[INFO] Starting Network Security System")
    logger.info(f"[INFO] Database: MySQL ({Config.DB_NAME})")
    logger.info(f"[INFO] Debug Mode: {Config.DEBUG}")
    logger.info(f"[INFO] Server: http://0.0.0.0:5000")
    logger.info("="*60)
    
    # Check database connection before spinning up the app
    with app.app_context():
        if test_connection():
            logger.info("[INFO] MySQL connection verified.")
        else:
            logger.critical("[CRITICAL] Could not connect to MySQL database! Ensure your MySQL server is running.")

    # Start the network thread cleanly here (Flask 3.0 safe)
    start_background_monitoring()
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=Config.DEBUG,
            use_reloader=False, # Disable reloader to prevent the network monitor thread from launching twice
            threaded=True
        )
    finally:
        if monitor_thread:
            monitor_thread.stop()
        logger.info("[INFO] Server shutdown complete")