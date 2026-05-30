# 📊 Google Sheets Integration Guide

## Overview

Your jimmyconnect bot now integrates with **Google Sheets** to automatically track and store student information!

## What Gets Tracked

Every student is automatically recorded with:

| Column | Description | Example |
|--------|-------------|---------|
| **Student ID** | Unique identifier | STU_20260529123456_5678 |
| **Full Name** | Student name | Ahmed Mohammed |
| **WhatsApp Phone** | Student's phone number | +2348012345678 |
| **Exam Type** | Type of exam | JAMB, WAEC, NECO, AWS, etc. |
| **Subscription Status** | Active/Inactive | Active |
| **Subscription Date** | When subscription started | 2026-05-29T12:34:56 |
| **Expiry Date** | When subscription expires | 2026-06-28T12:34:56 |
| **Total Messages** | Messages sent to bot | 45 |
| **Last Activity** | Last interaction timestamp | 2026-05-29T15:30:00 |
| **Registration Date** | When student joined | 2026-05-29T10:00:00 |
| **Notes** | Admin notes | Referred by school |

---

## Setup Instructions

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a Project" → "New Project"
3. Enter project name: `jimmyconnect`
4. Click "Create"
5. Wait for project to be created

### Step 2: Enable Google Sheets & Drive APIs

1. Go to **APIs & Services** → **Library**
2. Search for "Google Sheets API"
3. Click it → Click "Enable"
4. Go back to Library
5. Search for "Google Drive API"
6. Click it → Click "Enable"

### Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - Service account name: `jimmyconnect-bot`
   - Service account ID: `jimmyconnect-bot` (auto-filled)
   - Description: "Bot for tracking students"
4. Click "Create and Continue"
5. Click "Continue" (skip optional steps)
6. Click "Done"

### Step 4: Create & Download Key

1. Go to **APIs & Services** → **Credentials**
2. Under "Service Accounts", click `jimmyconnect-bot`
3. Go to **Keys** tab
4. Click "Add Key" → "Create new key"
5. Choose **JSON**
6. Click "Create"
7. **Save the JSON file** to your project root as `google_credentials.json`

**⚠️ IMPORTANT:** 
- Add `google_credentials.json` to `.gitignore`
- Never commit this file to GitHub
- Keep it secure!

### Step 5: Create Google Sheet

1. Go to https://sheets.google.com
2. Click "+ Create" → "Blank spreadsheet"
3. Name it: `jimmyconnect_students`
4. Share the sheet with your service account email:
   - In the JSON file, find `"client_email": "xxxx@xxxx.iam.gserviceaccount.com"`
   - Click "Share" in Google Sheets
   - Paste the email
   - Give "Editor" permissions
   - Uncheck "Notify people"
   - Click "Share"

### Step 6: Update .env

No additional environment variables needed! The bot will automatically:
- Detect `google_credentials.json`
- Create the spreadsheet if it doesn't exist
- Add headers automatically

### Step 7: Test

```bash
# Make sure virtual env is activated
python app.py
```

Send a test message to your WhatsApp bot. Check if the student appears in Google Sheets!

---

## Features

### ✅ Automatic Student Registration
- When a student messages the bot for the first time, they're added to the sheet
- Name, phone, and exam type are recorded

### ✅ Subscription Tracking
- When subscription is activated, sheet is updated with:
  - Subscription date
  - Expiry date (30 days later)
  - Status changed to "Active"

### ✅ Message Counting
- Each message increments the "Total Messages" counter
- Track student engagement

### ✅ Real-time Updates
- Last activity timestamp updates with each interaction
- Always current data

### ✅ Admin Dashboard
- `/admin/stats` - Get statistics from Google Sheets
- `/admin/students` - Get all student records
- `/admin/export-csv` - Export all data to CSV

---

## API Endpoints

### Get Statistics
```bash
curl https://your-app-url/admin/stats
```

**Response:**
```json
{
  "total_students": 150,
  "active_subscriptions": 45,
  "inactive_students": 105,
  "total_messages": 3200,
  "exam_breakdown": {
    "JAMB": 60,
    "WAEC": 45,
    "NECO": 30,
    "AWS": 15
  },
  "revenue_potential": 112500
}
```

### Get All Students
```bash
curl https://your-app-url/admin/students
```

**Response:**
```json
{
  "total": 150,
  "students": [
    {
      "Student ID": "STU_20260529123456_5678",
      "Full Name": "Ahmed Mohammed",
      "WhatsApp Phone": "+2348012345678",
      "Exam Type": "JAMB",
      "Subscription Status": "Active",
      "Subscription Date": "2026-05-29T12:34:56",
      "Expiry Date": "2026-06-28T12:34:56",
      "Total Messages": 45,
      "Last Activity": "2026-05-29T15:30:00",
      "Registration Date": "2026-05-29T10:00:00",
      "Notes": ""
    }
  ]
}
```

### Export to CSV
```bash
curl -X POST https://your-app-url/admin/export-csv
```

**Response:**
```json
{
  "status": "success",
  "file": "students_export_20260529_153000.csv"
}
```

---

## Using the Data

### In Google Sheets

1. **Add Formulas** - Use COUNTIF, SUMIF for analysis
2. **Create Charts** - Visualize student growth
3. **Set Filters** - Sort by status, exam type, etc.
4. **Automate Reports** - Use Apps Script for scheduled emails

### Example: Count Active JAMB Students
```
=COUNTIFS(D:D, "JAMB", E:E, "Active")
```

### Example: Revenue from Active Subscriptions
```
=COUNTIF(E:E, "Active") * 2500
```

---

## Troubleshooting

### Issue: "Google Sheets integration disabled"

**Solution:**
1. Check `google_credentials.json` exists in project root
2. Check file is valid JSON (not corrupted)
3. Check service account email is in `.env` (for reference)
4. Try again: `python app.py`

### Issue: "Spreadsheet 'jimmyconnect_students' not found"

**Solution:**
1. Create the sheet manually on Google Sheets
2. Name it exactly: `jimmyconnect_students`
3. Share with service account email
4. Restart bot: `python app.py`

### Issue: "Permission denied"

**Solution:**
1. Check service account email is shared in Google Sheets
2. Ensure permission level is "Editor"
3. Check credentials JSON file is valid
4. Create new key and try again

### Issue: Students not appearing in sheet

**Solution:**
1. Check bot logs: `python app.py` (should say "Google Sheets integration enabled")
2. Send test message to bot
3. Check if sheet has headers (should appear automatically)
4. Refresh Google Sheets page
5. Check if student is in the sheet under another name

---

## Best Practices

✅ **Do:**
- Backup Google Sheet regularly
- Review student data weekly
- Use Google Sheet for analytics
- Export data monthly
- Add custom notes for students

❌ **Don't:**
- Share `google_credentials.json` file
- Commit credentials to GitHub
- Delete sheet columns (breaks integration)
- Edit headers in sheet
- Modify formulas without testing

---

## Advanced Features

### Custom Automation (Google Apps Script)

Add to Google Sheet to send automated emails:

```javascript
function sendSubscriptionReminders() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getDataRange();
  const values = range.getValues();
  
  for (let i = 1; i < values.length; i++) {
    const expiryDate = new Date(values[i][6]);
    const today = new Date();
    const daysLeft = Math.floor((expiryDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysLeft <= 7 && daysLeft > 0) {
      const email = values[i][2]; // WhatsApp phone (as proxy)
      MailApp.sendEmail(
        "admin@jimmyconnect.com",
        `Reminder: ${values[i][1]} subscription expires in ${daysLeft} days`,
        `Student: ${values[i][1]}\nPhone: ${values[i][2]}\nExpires: ${expiryDate}`
      );
    }
  }
}
```

### Scheduled Reports

Add to Google Sheet to generate daily reports:

```javascript
function dailyReport() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getDataRange();
  const values = range.getValues();
  
  let activeCount = 0;
  let totalMessages = 0;
  
  for (let i = 1; i < values.length; i++) {
    if (values[i][4] === 'Active') activeCount++;
    totalMessages += parseInt(values[i][7]) || 0;
  }
  
  const report = `Daily Report: ${new Date().toDateString()}\n` +
                 `Active Subscriptions: ${activeCount}\n` +
                 `Total Messages: ${totalMessages}\n` +
                 `Revenue: ₦${activeCount * 2500}`;
  
  MailApp.sendEmail("admin@jimmyconnect.com", "Daily Report", report);
}
```

---

## Data Privacy

⚠️ **Important:**
- Google Sheets contains student personal data
- Follow GDPR/CCPA compliance if applicable
- Regular backups recommended
- Limit share access to authorized personnel only
- Delete data per student request (if applicable)

---

## Next Steps

1. ✅ Set up Google Cloud Project
2. ✅ Create service account & download key
3. ✅ Create Google Sheet
4. ✅ Add `google_credentials.json` to project
5. ✅ Update `.env` if needed
6. ✅ Install dependencies: `pip install -r requirements.txt`
7. ✅ Test: `python app.py`
8. ✅ Send test message to bot
9. ✅ Check Google Sheet for student record
10. ✅ Deploy to production

---

**Your bot is now tracking students in Google Sheets! 📊**
