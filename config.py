import os
from dotenv import load_dotenv

load_dotenv()

# WhatsApp Config
WHATSAPP_API_VERSION = os.getenv('WHATSAPP_API_VERSION', 'v18.0')
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN', 'jimmyconnect_secret_token')

# Selar Config
SELAR_API_KEY = os.getenv('SELAR_API_KEY')
SELAR_API_URL = os.getenv('SELAR_API_URL', 'https://api.selar.co/v1')
SELAR_SUBSCRIPTION_ID = os.getenv('SELAR_SUBSCRIPTION_ID')
SUBSCRIPTION_PRICE = int(os.getenv('SUBSCRIPTION_PRICE', '2500'))

# Database
USERS_DATABASE_FILE = os.getenv('USERS_DATABASE_FILE', 'users_db.json')
QA_DATABASE_FILE = os.getenv('QA_DATABASE_FILE', 'qa_database.json')

# Google Sheets
GOOGLE_SHEETS_ENABLED = os.getenv('GOOGLE_SHEETS_ENABLED', 'true').lower() == 'true'
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'google_credentials.json')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'jimmyconnect_students')
