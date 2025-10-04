#!/usr/bin/env python3
"""
Script to update the database with the goals table
"""
from app import create_app
from app.extensions import db
from app.models import User, Goal

def update_database():
    app = create_app()
    
    with app.app_context():
        print("Creating goals table...")
        
        # Create only the goals table (users table should already exist)
        db.create_all()
        
        print("✅ Database updated successfully!")
        print("Tables in database:")
        print("- users (existing)")
        print("- goals (new)")
        print("\nGoal table structure:")
        print("- id (Primary Key)")
        print("- goal_title (String 200)")
        print("- description (Text)")
        print("- goal_type (String 50)")
        print("- priority (String 20) - low/medium/high")
        print("- category (String 50)")
        print("- start_date (Date)")
        print("- end_date (Date)")
        print("- user_id (Foreign Key to users.id)")
        print("- created_at (DateTime)")
        print("- updated_at (DateTime)")
        print("- is_completed (Boolean)")
        print("- completion_date (Date)")

if __name__ == "__main__":
    update_database()