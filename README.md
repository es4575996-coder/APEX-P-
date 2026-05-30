# jimmyconnect WhatsApp Bot 🎓

An intelligent WhatsApp bot for educational exam preparation (JAMB, WAEC, NECO, ICAN, CIPM, AWS) with subscription management and payment integration.

## Features ✨

- ✅ WhatsApp Cloud API integration
- ✅ Automated Q&A engine for exam preparation
- ✅ Selar payment integration for subscriptions
- ✅ Google Sheets student tracking
- ✅ User management with subscription status
- ✅ Real-time message handling
- ✅ Admin dashboard with statistics
- ✅ Docker & Heroku ready

## Quick Start 🚀

### 1. Clone Repository
```bash
git clone https://github.com/es4575996-coder/APEX-P-.git
cd APEX-P-
```

### 2. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Add Google Sheets Credentials
```bash
# Place google_credentials.json in project root
# Follow GOOGLE_SHEETS_SETUP.md for setup
```

### 6. Run Bot
```bash
python app.py
```

## Configuration 🔧

Create `.env` file with:

```env
# WhatsApp
WHATSAPP_API_VERSION=v18.0
WHATSAPP_BUSINESS_ACCOUNT_ID=your_id
WHATSAPP_PHONE_NUMBER_ID=your_id
WHATSAPP_ACCESS_TOKEN=your_token
WEBHOOK_VERIFY_TOKEN=secret

# Selar
SELAR_API_KEY=your_key
SELAR_SUBSCRIPTION_ID=your_id
SUBSCRIPTION_PRICE=2500

# Google Sheets
GOOGLE_SHEETS_ENABLED=true
```

## Supported Exams 📚

- 📌 JAMB - University entrance
- 📌 WAEC - Secondary certificate
- 📌 NECO - Secondary alternative
- 📌 ICAN - Accounting qualification
- 📌 CIPM - HR qualification
- 📌 AWS - Cloud certification

## API Endpoints 🔌

- `POST /webhook` - Receive WhatsApp messages
- `GET /webhook` - Verify webhook token
- `GET /health` - Health check
- `GET /admin/stats` - Get statistics

## Deployment 🌐

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t jimmyconnect .
docker run -p 5000:5000 jimmyconnect
```

## Documentation 📖

- [Google Sheets Setup](GOOGLE_SHEETS_SETUP.md)
- [Configuration Guide](SETUP_GUIDE.md)

## License 📄

MIT License

## Support 💬

For issues or questions, create an issue in the repository.
