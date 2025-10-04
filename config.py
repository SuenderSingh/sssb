# config.py
import os
import urllib.parse

# Database configuration
class Config:
    user = "postgres"
    password = urllib.parse.quote_plus("Singh@7082")
    host = "localhost"
    port = "5432"
    db = "postgres"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"  

class DevelopmentConfig(Config):
    DEBUG = True

# Deployment configuration
class ProductionConfig:
    # Database configuration for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key-here-change-this'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key-here-change-this'
    
    # Other production settings
    DEBUG = False
    TESTING = False
    
    # CORS settings for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

class StagingConfig(ProductionConfig):
    DEBUG = True

class DevelopmentConfig:
    # Database configuration for development
    user = "postgres"
    password = urllib.parse.quote_plus("Singh@7082")
    host = "localhost"
    port = "5432"
    db = "postgres"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"
    JWT_SECRET_KEY = "jwt-secret-string"
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
