import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    def __init__(self, credentials_file='google_credentials.json', sheet_name='jimmyconnect_students'):
        try:
            if not os.path.exists(credentials_file):
                logger.warning(f"Google credentials file not found: {credentials_file}")
                self.enabled = False
                return
            
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            self.creds = Credentials.from_service_account_file(
                credentials_file,
                scopes=scope
            )
            
            self.client = gspread.authorize(self.creds)
            
            try:
                self.sheet = self.client.open(sheet_name).sheet1
            except gspread.exceptions.SpreadsheetNotFound:
                logger.info(f"Creating new sheet: {sheet_name}")
                self.sheet = self.create_sheet(sheet_name)
            
            if not self.sheet.cell(1, 1).value:
                self.initialize_headers()
            
            self.enabled = True
            logger.info("Google Sheets integration enabled")
        except Exception as e:
            logger.error(f"Google Sheets initialization failed: {str(e)}")
            self.enabled = False
    
    def initialize_headers(self):
        headers = [
            'Student ID', 'Full Name', 'WhatsApp Phone', 'Exam Type',
            'Subscription Status', 'Subscription Date', 'Expiry Date',
            'Total Messages', 'Last Activity', 'Registration Date', 'Notes'
        ]
        self.sheet.insert_row(headers, index=1)
        logger.info("Headers initialized")
    
    def create_sheet(self, sheet_name):
        spreadsheet = self.client.create(sheet_name)
        return spreadsheet.sheet1
    
    def add_student(self, phone_number, name=None, exam_type='General'):
        if not self.enabled:
            return None
        
        try:
            existing = self.find_student_by_phone(phone_number)
            if existing:
                return existing
            
            student_id = f"STU_{datetime.now().strftime('%Y%m%d%H%M%S')}_{phone_number[-4:]}"
            row_data = [
                student_id, name or 'Not Provided', phone_number, exam_type,
                'Inactive', '', '', '0', datetime.now().isoformat(),
                datetime.now().isoformat(), ''
            ]
            
            self.sheet.append_row(row_data)
            logger.info(f"Student added: {phone_number}")
            
            return {
                'student_id': student_id,
                'name': name or 'Not Provided',
                'phone': phone_number,
                'exam_type': exam_type
            }
        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            return None
    
    def find_student_by_phone(self, phone_number):
        if not self.enabled:
            return None
        
        try:
            cell = self.sheet.find(phone_number)
            if cell:
                row = self.sheet.row_values(cell.row)
                return self.row_to_dict(row)
            return None
        except gspread.exceptions.CellNotFound:
            return None
        except Exception as e:
            logger.error(f"Error finding student: {str(e)}")
            return None
    
    def update_student(self, phone_number, **kwargs):
        if not self.enabled:
            return False
        
        try:
            cell = self.sheet.find(phone_number)
            if not cell:
                return False
            
            row_num = cell.row
            headers = self.sheet.row_values(1)
            
            for key, value in kwargs.items():
                if key in headers:
                    col_idx = headers.index(key) + 1
                    self.sheet.update_cell(row_num, col_idx, value)
            
            last_activity_col = headers.index('Last Activity') + 1
            self.sheet.update_cell(row_num, last_activity_col, datetime.now().isoformat())
            
            logger.info(f"Student {phone_number} updated")
            return True
        except Exception as e:
            logger.error(f"Error updating student: {str(e)}")
            return False
    
    def increment_message_count(self, phone_number):
        if not self.enabled:
            return False
        
        try:
            cell = self.sheet.find(phone_number)
            if not cell:
                return False
            
            row_num = cell.row
            headers = self.sheet.row_values(1)
            msg_col = headers.index('Total Messages') + 1
            current_count = int(self.sheet.cell(row_num, msg_col).value or 0)
            self.sheet.update_cell(row_num, msg_col, current_count + 1)
            return True
        except Exception as e:
            logger.error(f"Error incrementing message count: {str(e)}")
            return False
    
    def get_all_students(self):
        if not self.enabled:
            return []
        
        try:
            return self.sheet.get_all_records()
        except Exception as e:
            logger.error(f"Error getting all students: {str(e)}")
            return []
    
    def row_to_dict(self, row):
        try:
            headers = self.sheet.row_values(1)
            return dict(zip(headers, row))
        except Exception as e:
            logger.error(f"Error converting row to dict: {str(e)}")
            return {}
