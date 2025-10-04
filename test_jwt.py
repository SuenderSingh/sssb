#!/usr/bin/env python3
"""
Test script to check JWT token creation and validation
"""
from app import create_app
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token, decode_token

def test_jwt_tokens():
    app = create_app()
    
    with app.app_context():
        # Test user
        test_user = User.query.first()
        if not test_user:
            print("No users found in database. Please register a user first.")
            return
        
        print(f"Testing with user ID: {test_user.id} (type: {type(test_user.id)})")
        
        # Create token with string user ID
        token_str = create_access_token(identity=str(test_user.id))
        print(f"Token created with string ID: {token_str[:50]}...")
        
        # Create token with integer user ID
        try:
            token_int = create_access_token(identity=test_user.id)
            print(f"Token created with integer ID: {token_int[:50]}...")
        except Exception as e:
            print(f"Error creating token with integer ID: {e}")
        
        # Decode tokens to see what's inside
        try:
            decoded_str = decode_token(token_str)
            print(f"Decoded string token subject: {decoded_str['sub']} (type: {type(decoded_str['sub'])})")
        except Exception as e:
            print(f"Error decoding string token: {e}")
        
        try:
            decoded_int = decode_token(token_int)
            print(f"Decoded integer token subject: {decoded_int['sub']} (type: {type(decoded_int['sub'])})")
        except Exception as e:
            print(f"Error decoding integer token: {e}")

if __name__ == "__main__":
    test_jwt_tokens()