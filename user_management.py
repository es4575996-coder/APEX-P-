import json
import os
from datetime import datetime, timedelta
from config import DATABASE_FILE

class UserManager:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.load_database()
    
    def load_database(self):
        """Load user database from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_database(self):
        """Save user database to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def add_user(self, phone_number):
        """Add a new user"""
        if phone_number not in self.users:
            self.users[phone_number] = {
                "phone_number": phone_number,
                "created_at": datetime.now().isoformat(),
                "subscription_status": "inactive",
                "subscription_expiry": None,
                "total_messages": 0,
                "selar_reference": None
            }
            self.save_database()
            return True
        return False
    
    def get_user(self, phone_number):
        """Get user information"""
        if phone_number not in self.users:
            self.add_user(phone_number)
        return self.users.get(phone_number)
    
    def is_subscribed(self, phone_number):
        """Check if user has active subscription"""
        user = self.get_user(phone_number)
        if user["subscription_status"] == "active":
            expiry = datetime.fromisoformat(user["subscription_expiry"])
            if datetime.now() < expiry:
                return True
            else:
                # Subscription expired
                self.deactivate_subscription(phone_number)
                return False
        return False
    
    def activate_subscription(self, phone_number, selar_reference):
        """Activate subscription for a user"""
        user = self.get_user(phone_number)
        expiry_date = datetime.now() + timedelta(days=30)
        
        user["subscription_status"] = "active"
        user["subscription_expiry"] = expiry_date.isoformat()
        user["selar_reference"] = selar_reference
        
        self.save_database()
        return True
    
    def deactivate_subscription(self, phone_number):
        """Deactivate subscription for a user"""
        user = self.get_user(phone_number)
        user["subscription_status"] = "inactive"
        self.save_database()
        return True
    
    def increment_message_count(self, phone_number):
        """Increment message count for a user"""
        user = self.get_user(phone_number)
        user["total_messages"] = user.get("total_messages", 0) + 1
        self.save_database()
    
    def get_all_users(self):
        """Get all users"""
        return self.users
    
    def get_subscription_status(self, phone_number):
        """Get subscription status message"""
        user = self.get_user(phone_number)
        if user["subscription_status"] == "active":
            expiry = datetime.fromisoformat(user["subscription_expiry"])
            days_left = (expiry - datetime.now()).days
            return f"Active (Expires in {days_left} days)"
        return "Inactive"