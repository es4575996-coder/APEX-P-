import json
import os
from config import QA_DATABASE_FILE
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)

class QAEngine:
    def __init__(self):
        self.qa_db_file = QA_DATABASE_FILE
        self.load_qa_database()
    
    def load_qa_database(self):
        """Load Q&A database from JSON file"""
        if os.path.exists(self.qa_db_file):
            with open(self.qa_db_file, 'r') as f:
                self.qa_data = json.load(f)
        else:
            self.qa_data = {}
    
    def find_answer(self, user_query):
        """Find answer based on user query"""
        user_query_lower = user_query.lower().strip()
        
        # Check for exact matches first
        for category, questions in self.qa_data.items():
            for question_key, answer in questions.items():
                if question_key in user_query_lower or user_query_lower in question_key:
                    return {
                        "found": True,
                        "answer": answer,
                        "category": category,
                        "confidence": 1.0
                    }
        
        # Check for fuzzy matches
        best_match = None
        best_ratio = 0.5
        
        for category, questions in self.qa_data.items():
            for question_key, answer in questions.items():
                ratio = SequenceMatcher(None, user_query_lower, question_key).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = {
                        "found": True,
                        "answer": answer,
                        "category": category,
                        "confidence": ratio
                    }
        
        if best_match:
            return best_match
        
        return {
            "found": False,
            "answer": None,
            "category": None,
            "confidence": 0.0
        }
    
    def get_category_overview(self, category):
        """Get overview of a category"""
        category_upper = category.upper()
        if category_upper in self.qa_data:
            topics = list(self.qa_data[category_upper].keys())
            return {
                "found": True,
                "category": category_upper,
                "topics": topics,
                "count": len(topics)
            }
        return {
            "found": False,
            "category": category,
            "topics": [],
            "count": 0
        }
    
    def get_all_categories(self):
        """Get all available categories"""
        return list(self.qa_data.keys())
    
    def search_by_keyword(self, keyword):
        """Search for questions containing a keyword"""
        keyword_lower = keyword.lower()
        results = []
        
        for category, questions in self.qa_data.items():
            for question_key, answer in questions.items():
                if keyword_lower in question_key.lower() or keyword_lower in answer.lower():
                    results.append({
                        "question": question_key,
                        "answer": answer,
                        "category": category
                    })
        
        return results
