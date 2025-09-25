# config.py
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
