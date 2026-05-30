import json
import os
from datetime import datetime, timedelta
from config import USERS_DATABASE_FILE
import logging

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self):
        self.db_file = USERS_DATABASE_FILE
        self.load_database()
    
    def load_database(self):
        """Load users from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_database(self):
        """Save users to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def add_user(self, phone_number, name=None):
        """Add or update user"""
        if phone_number not in self.users:
            self.users[phone_number] = {
                'phone_number': phone_number,
                'name': name or 'Student',
                'subscription_active': False,
                'subscription_start': None,
                'subscription_end': None,
                'total_messages': 0,
                'registered_at': datetime.now().isoformat()
            }
            logger.info(f"New user added: {phone_number}")
        self.save_database()
    
    def get_user(self, phone_number):
        """Get user by phone number"""
        return self.users.get(phone_number)
    
    def is_subscribed(self, phone_number):
        """Check if user has active subscription"""
        user = self.get_user(phone_number)
        if not user:
            return False
        
        if not user['subscription_active']:
            return False
        
        if user['subscription_end']:
            end_date = datetime.fromisoformat(user['subscription_end'])
            if datetime.now() > end_date:
                return False
        
        return True
    
    def activate_subscription(self, phone_number, days=30):
        """Activate subscription for user"""
        if phone_number in self.users:
            self.users[phone_number]['subscription_active'] = True
            self.users[phone_number]['subscription_start'] = datetime.now().isoformat()
            self.users[phone_number]['subscription_end'] = (datetime.now() + timedelta(days=days)).isoformat()
            self.save_database()
            logger.info(f"Subscription activated for {phone_number}")
            return True
        return False
    
    def increment_message_count(self, phone_number):
        """Increment message count for user"""
        if phone_number in self.users:
            self.users[phone_number]['total_messages'] = self.users[phone_number].get('total_messages', 0) + 1
            self.save_database()
    
    def get_all_users(self):
        """Get all users"""
        return self.users
