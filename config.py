import os
from dotenv import load_dotenv

load_dotenv()

# WhatsApp Cloud API Configuration
WHATSAPP_API_VERSION = "v18.0"
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "jimmyconnect_webhook_token")

# Selar API Configuration
SELAR_API_KEY = os.getenv("SELAR_API_KEY")
SELAR_SUBSCRIPTION_ID = os.getenv("SELAR_SUBSCRIPTION_ID")
SELAR_API_URL = "https://api.selar.co/v1"

# Database Configuration (Using simple JSON file for now)
DATABASE_FILE = "users_db.json"
QA_DATABASE_FILE = "qa_database.json"

# Bot Configuration
BOT_NAME = "jimmyconnect"
SUBSCRIPTION_PRICE = 2500  # NGN per month (or your currency)
SUBSCRIPTION_DURATION = 30  # days