"""
Main Flask application for the Fantasy Baseball API.
"""
import os
import logging
from flask import Flask
from flask_cors import CORS
from config import config
from models import db
from routes import api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
    
    # Add health check route
    @app.route('/')
    def index():
        return {
            'message': 'Fantasy Baseball API',
            'version': '1.0.0',
            'status': 'running'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    logger.info(f"Flask app created with config: {config_name}")
    return app


def init_database():
    """Initialize database with sample data."""
    from scraper import MLBScraper
    
    logger.info("Initializing database with sample data...")
    
    try:
        scraper = MLBScraper()
        scraper.run_full_scrape()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


if __name__ == '__main__':
    # Create app
    app = create_app()
    
    # Initialize database if needed
    with app.app_context():
        from models import Team
        if Team.query.count() == 0:
            init_database()
    
    # Run app
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask app on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
