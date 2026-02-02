“””
User management for Starlightdeck V2
Handles user profiles, authentication, and data
“””

import json
from pathlib import Path
from datetime import datetime

class UserManager:
def **init**(self, user_file=“user_profile.json”):
self.user_file = user_file
self.load_users()

```
def load_users(self):
    """Load user data from JSON file"""
    try:
        with open(self.user_file, 'r') as f:
            self.users = json.load(f)
    except FileNotFoundError:
        self.users = {}

def save_users(self):
    """Save user data to JSON file"""
    with open(self.user_file, 'w') as f:
        json.dump(self.users, f, indent=2)

def create_user(self, username, password):
    """Create a new user account"""
    if username in self.users:
        return False, "Username already exists"
    
    self.users[username] = {
        'password': password,  # NOTE: In production, hash this!
        'created_at': datetime.now().isoformat(),
        'last_login': None,
        'profile': {
            'display_name': username
        }
    }
    self.save_users()
    return True, "User created successfully"

def authenticate(self, username, password):
    """Authenticate user login - BASIC LOGIC PLACEHOLDER"""
    if username not in self.users:
        return False, "User not found"
    
    if self.users[username]['password'] == password:
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.save_users()
        return True, "Login successful"
    return False, "Invalid password"

def get_user(self, username):
    """Get user profile data"""
    return self.users.get(username, None)

def update_profile(self, username, profile_data):
    """Update user profile"""
    if username in self.users:
        self.users[username]['profile'].update(profile_data)
        self.save_users()
        return True
    return False

def user_exists(self, username):
    """Check if user exists"""
    return username in self.users
```

# TODO: Replace basic authentication with Careon login system