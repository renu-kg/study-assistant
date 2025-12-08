# utils/auth.py
import json
import os
import hashlib

class UserAuth:
    def __init__(self):
        self.users_file = "data/user_data/users.json"
        self.ensure_users_file()
    
    def ensure_users_file(self):
        """Create users file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """Register new user"""
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            "password": self.hash_password(password),
            "email": email,
            "created_at": __import__('datetime').datetime.now().isoformat()
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        return True, "Registration successful"
    
    def login_user(self, username, password):
        """Authenticate user"""
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if username not in users:
            return False, "Username not found"
        
        if users[username]["password"] != self.hash_password(password):
            return False, "Incorrect password"
        
        return True, "Login successful"
    
    def user_exists(self, username):
        """Check if user exists"""
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        return username in users
