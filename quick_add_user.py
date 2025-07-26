#!/usr/bin/env python3
"""
Quick User Addition Script
Usage: python quick_add_user.py <username> <password> <role>
Example: python quick_add_user.py doctor1 password123 doctor
"""

import sys
from app import app, db, User
from werkzeug.security import generate_password_hash

def quick_add_user(username, password, role):
    """Quickly add a user with command line arguments"""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False
        
        # Validate role
        valid_roles = ['admin', 'receptionist', 'doctor']
        if role not in valid_roles:
            print(f"❌ Invalid role '{role}'. Valid roles: {', '.join(valid_roles)}")
            return False
        
        # Create password hash
        password_hash = generate_password_hash(password)
        
        # Create new user
        new_user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            doctor_id=None,
            is_active=True
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ User '{username}' created successfully with role '{role}'!")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python quick_add_user.py <username> <password> <role>")
        print("Example: python quick_add_user.py doctor1 password123 doctor")
        print("Valid roles: admin, receptionist, doctor")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    role = sys.argv[3].lower()
    
    quick_add_user(username, password, role) 