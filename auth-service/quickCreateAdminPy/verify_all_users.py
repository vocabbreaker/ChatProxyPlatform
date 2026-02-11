#!/usr/bin/env python3
"""
Verify All Users in MongoDB
Marks all users from CSV as verified so they can login.
"""

import csv
import os
from pymongo import MongoClient

# Configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "auth_db"  # Correct database name from .env
CSV_FILE = "users.csv"

def log(message, status="INFO"):
    """Simple logging"""
    symbols = {"SUCCESS": "✓", "ERROR": "✗", "INFO": "►", "WARNING": "⚠"}
    print(f"{symbols.get(status, '•')} {message}")

def read_users_from_csv():
    """Read user emails and roles from CSV"""
    users = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('action') or row['action'].startswith('#') or row['action'].lower() != 'create':
                    continue
                users.append({
                    'email': row['email'].strip(),
                    'role': row.get('role', 'enduser').strip()
                })
        return users
    except Exception as e:
        log(f"Error reading CSV: {str(e)}", "ERROR")
        return []

def main():
    print("=" * 60)
    print("Verify All Users - MongoDB Update")
    print("=" * 60)
    print()
    
    # Read users from CSV
    users = read_users_from_csv()
    if not users:
        log("No users found in CSV", "WARNING")
        input("\nPress Enter to exit...")
        return
    
    log(f"Found {len(users)} users to verify", "INFO")
    print()
    
    try:
        # Connect to MongoDB
        log("Connecting to MongoDB...", "INFO")
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        users_collection = db["users"]
        
        # Verify and fix role for each user
        success_count = 0
        error_count = 0
        
        for user_data in users:
            email = user_data['email']
            role = user_data['role']
            
            result = users_collection.update_one(
                {"email": email},
                {"$set": {"isVerified": True, "role": role}}
            )
            
            if result.matched_count > 0:
                log(f"Verified user: {email} (role: {role})", "SUCCESS")
                success_count += 1
            else:
                log(f"User not found: {email}", "WARNING")
                error_count += 1
        
        # Summary
        print()
        print("=" * 60)
        log("Verification complete!", "SUCCESS")
        log(f"Success: {success_count} | Not Found: {error_count}", "INFO")
        print("=" * 60)
        
        client.close()
        
    except Exception as e:
        log(f"MongoDB error: {str(e)}", "ERROR")
        log("Make sure MongoDB is running and pymongo is installed", "INFO")
        log("Install with: pip install pymongo", "INFO")
    
    print()

if __name__ == "__main__":
    main()
