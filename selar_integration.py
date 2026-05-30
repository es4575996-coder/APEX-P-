import requests
import json
from config import SELAR_API_KEY, SELAR_API_URL, SELAR_SUBSCRIPTION_ID, SUBSCRIPTION_PRICE
import logging

logger = logging.getLogger(__name__)

class SelarIntegration:
    def __init__(self):
        self.api_key = SELAR_API_KEY
        self.api_url = SELAR_API_URL
        self.subscription_id = SELAR_SUBSCRIPTION_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_payment_link(self, customer_email, customer_phone, amount=None):
        """Create a payment link for subscription"""
        if amount is None:
            amount = SUBSCRIPTION_PRICE
        
        payload = {
            "product_id": self.subscription_id,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "amount": amount,
            "currency": "NGN"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/products/create-checkout-link",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "payment_link": data.get("checkout_link"),
                    "reference": data.get("reference")
                }
            else:
                logger.error(f"Selar API error: {response.text}")
                return {
                    "success": False,
                    "payment_link": None,
                    "reference": None,
                    "error": response.text
                }
        except Exception as e:
            logger.error(f"Error creating payment link: {str(e)}")
            return {
                "success": False,
                "payment_link": None,
                "reference": None,
                "error": str(e)
            }
    
    def verify_payment(self, reference):
        """Verify if payment was successful"""
        try:
            response = requests.get(
                f"{self.api_url}/transactions/verify/{reference}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("status"),
                    "amount": data.get("amount"),
                    "customer_email": data.get("customer_email")
                }
            else:
                logger.error(f"Verification error: {response.text}")
                return {
                    "success": False,
                    "status": "failed"
                }
        except Exception as e:
            logger.error(f"Error verifying payment: {str(e)}")
            return {
                "success": False,
                "status": "error",
                "error": str(e)
            }
