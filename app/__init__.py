from flask import Flask
from .extensions import db, jwt, CORS
from .routes.auth_routes import auth_bp
from .routes.main_routes import main_bp
from .routes.goal_routes import goal_bp
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    if config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'staging':
        from config import StagingConfig
        app.config.from_object(StagingConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(main_bp)  # Register main routes without prefix
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(goal_bp, url_prefix="/api")  # Goals API routes

    return app
