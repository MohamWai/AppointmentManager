#!/usr/bin/env python3
"""
User Management Script for Clinic Management System
Add users programmatically to the system
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def add_user(username, password, role, doctor_id=None):
    """Add a new user to the system"""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False
        
        # Create password hash
        password_hash = generate_password_hash(password)
        
        # Create new user
        new_user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            doctor_id=doctor_id,
            is_active=True
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ User '{username}' created successfully with role '{role}'!")
        return True

def list_users():
    """List all users in the system"""
    with app.app_context():
        users = User.query.all()
        print("\n📋 Current Users:")
        print("-" * 50)
        for user in users:
            status = "🟢 Active" if user.is_active else "🔴 Inactive"
            print(f"ID: {user.id} | Username: {user.username} | Role: {user.role} | {status}")
        print("-" * 50)

if __name__ == "__main__":
    print("🏥 Clinic Management System - User Management")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Add new user")
        print("2. List all users")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n📝 Add New User")
            print("-" * 30)
            
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            print("\nAvailable roles:")
            print("1. admin - Full system access")
            print("2. receptionist - Patient and appointment management")
            print("3. doctor - Clinical documentation")
            
            role_choice = input("Select role (1-3): ").strip()
            
            role_map = {
                "1": "admin",
                "2": "receptionist", 
                "3": "doctor"
            }
            
            role = role_map.get(role_choice)
            if not role:
                print("❌ Invalid role choice!")
                continue
            
            # For doctor role, ask for doctor_id
            doctor_id = None
            if role == "doctor":
                doctor_id_input = input("Doctor ID (optional, press Enter to skip): ").strip()
                if doctor_id_input:
                    try:
                        doctor_id = int(doctor_id_input)
                    except ValueError:
                        print("❌ Invalid doctor ID!")
                        continue
            
            add_user(username, password, role, doctor_id)
            
        elif choice == "2":
            list_users()
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.") 