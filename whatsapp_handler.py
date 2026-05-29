import requests
import json
import logging
from config import (
    WHATSAPP_API_VERSION,
    WHATSAPP_BUSINESS_ACCOUNT_ID,
    WHATSAPP_PHONE_NUMBER_ID,
    WHATSAPP_ACCESS_TOKEN
)

logger = logging.getLogger(__name__)

class WhatsAppHandler:
    def __init__(self):
        self.api_version = WHATSAPP_API_VERSION
        self.business_account_id = WHATSAPP_BUSINESS_ACCOUNT_ID
        self.phone_number_id = WHATSAPP_PHONE_NUMBER_ID
        self.access_token = WHATSAPP_ACCESS_TOKEN
        self.api_url = f"https://graph.instagram.com/{self.api_version}/{self.phone_number_id}"
    
    def send_text_message(self, phone_number, message):
        """Send a text message via WhatsApp"""
        url = f"{self.api_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                logger.info(f"Message sent to {phone_number}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False
    
    def send_template_message(self, phone_number, template_name, template_language="en"):
        """Send a template message"""
        url = f"{self.api_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": template_language
                }
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                logger.info(f"Template message sent to {phone_number}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending template: {str(e)}")
            return False