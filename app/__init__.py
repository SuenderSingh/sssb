from flask import Flask
from .extensions import db, jwt, CORS
from .routes.auth_routes import auth_bp
from .routes.main_routes import main_bp
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(main_bp)  # Register main routes without prefix
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
