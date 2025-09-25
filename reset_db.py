#!/usr/bin/env python3
"""
Script to reset the database with updated schema
"""
from app import create_app
from app.extensions import db
from app.models import User

def reset_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables with updated schema...")
        db.create_all()
        
        print("Database reset complete!")
        print("The 'users' table now has a password_hash column that can store up to 255 characters.")

if __name__ == "__main__":
    reset_database()
