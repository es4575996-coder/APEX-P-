from flask import Flask, request, jsonify
import logging
from config import WEBHOOK_VERIFY_TOKEN
from user_management import UserManager
from qa_engine import QAEngine
from whatsapp_handler import WhatsAppHandler
from selar_integration import SelarIntegration

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize managers
user_manager = UserManager()
qa_engine = QAEngine()
whatsapp = WhatsAppHandler()
selar = SelarIntegration()

# Extract phone number from message
def extract_phone(message_data):
    """Extract phone number from WhatsApp message"""
    try:
        return message_data['from']
    except:
        return None

# Parse user message
def parse_user_message(message_data):
    """Parse different message types"""
    if message_data.get('type') == 'text':
        return message_data['text']['body']
    elif message_data.get('type') == 'interactive':
        return message_data['interactive'].get('button_reply', {}).get('title') or \
               message_data['interactive'].get('list_reply', {}).get('title')
    return None

# Generate response
def generate_response(user_input, phone_number, is_subscribed):
    """Generate bot response based on user input"""
    user_input_lower = user_input.lower().strip()
    
    # Check if user is not subscribed
    if not is_subscribed and user_input_lower not in ['subscribe', 'help', 'menu', 'pay', 'hello', 'hi']:
        return {
            "type": "subscription_required",
            "message": "💳 *Premium Feature* 💳\n\nTo access study materials and answers, you need an active subscription.\n\n*Price:* ₦2,500/month\n\nReply *SUBSCRIBE* to get started!"
        }
    
    # Handle subscription request
    if user_input_lower in ['subscribe', 'pay']:
        return {
            "type": "subscription",
            "message": "📲 *Subscription Activated!*\n\nClick the link below to complete your payment:\n\n(Payment link will be sent via Selar)\n\nOnce payment is confirmed, you'll have unlimited access for 30 days!"
        }
    
    # Handle help and menu
    if user_input_lower in ['help', 'menu', 'hi', 'hello']:
        return {
            "type": "info",
            "message": f"🎓 *Welcome to jimmyconnect!* 🎓\n\n*Available Topics:*\n• JAMB\n• WAEC\n• NECO\n• ICAN\n• CIPM\n• AWS\n\n*How to use:*\n1️⃣ Ask any question about the topics above\n2️⃣ Type a topic name for quick info\n3️⃣ Type *SUBSCRIBE* for premium access\n\n*Example:*\n- 'What is JAMB?'\n- 'AWS certification'\n- 'WAEC subjects'"
        }
    
    # Try to find answer in database
    result = qa_engine.find_answer(user_input)
    
    if result['found']:
        confidence = result['confidence']
        answer = result['answer']
        category = result['category']
        
        if confidence > 0.7:
            return {
                "type": "answer",
                "message": f"📚 *{category}*\n\n{answer}\n\n✅ *Need more info?* Ask another question!"
            }
    
    # Search for related questions
    keywords = user_input_lower.split()
    for keyword in keywords:
        if len(keyword) > 3:
            search_results = qa_engine.search_by_keyword(keyword)
            if search_results:
                return {
                    "type": "search_results",
                    "message": f"🔍 *Related Topics Found:*\n\n{search_results[0]['answer']}\n\n💡 Ask more specific questions for better answers!"
                }
    
    # Default response
    return {
        "type": "not_found",
        "message": "❓ *Question Not Found*\n\nI couldn't find an answer to that question.\n\n*Try:*\n• Asking about JAMB, WAEC, NECO, ICAN, CIPM, or AWS\n• Using simpler keywords\n• Type *HELP* for more options"
    }

# Webhook for incoming messages
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")
        
        # Check if it's a message event
        if data.get('entry'):
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    if change['field'] == 'messages':
                        messages = change['value'].get('messages', [])
                        
                        for message in messages:
                            phone_number = extract_phone(message)
                            user_message = parse_user_message(message)
                            
                            if phone_number and user_message:
                                # Register/update user
                                user_manager.add_user(phone_number)
                                user = user_manager.get_user(phone_number)
                                
                                # Check subscription status
                                is_subscribed = user_manager.is_subscribed(phone_number)
                                
                                # Increment message count
                                user_manager.increment_message_count(phone_number)
                                
                                # Generate response
                                response = generate_response(user_message, phone_number, is_subscribed)
                                
                                # Send response
                                whatsapp.send_text_message(phone_number, response['message'])
                                
                                # Handle subscription requests
                                if response['type'] == 'subscription':
                                    # Create Selar payment link
                                    payment_result = selar.create_payment_link(
                                        customer_email=f"{phone_number}@jimmyconnect.local",
                                        customer_phone=phone_number
                                    )
                                    
                                    if payment_result['success']:
                                        payment_msg = f"💳 *Payment Link Ready!*\n\n{payment_result['payment_link']}\n\nClick the link to complete your ₦2,500 subscription."
                                        whatsapp.send_text_message(phone_number, payment_msg)
        
        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Webhook verification
@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """Verify webhook token"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == WEBHOOK_VERIFY_TOKEN:
        return challenge
    return "Invalid verification token", 403

# Health check
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

# Admin dashboard (simple)
@app.route('/admin/stats', methods=['GET'])
def admin_stats():
    """Get admin statistics"""
    all_users = user_manager.get_all_users()
    
    total_users = len(all_users)
    active_subscriptions = sum(1 for u in all_users.values() if user_manager.is_subscribed(u['phone_number']))
    total_messages = sum(u.get('total_messages', 0) for u in all_users.values())
    
    return jsonify({
        "total_users": total_users,
        "active_subscriptions": active_subscriptions,
        "total_messages": total_messages,
        "revenue_potential": f"₦{active_subscriptions * 2500}/month"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
