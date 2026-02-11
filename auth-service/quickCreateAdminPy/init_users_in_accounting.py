#!/usr/bin/env python3
"""
Initialize Users in Accounting Service
Makes each user authenticate once to trigger auto-creation in accounting database.
"""

import csv
import requests
import sys
import os

# Configuration
AUTH_API = "http://localhost:3000"
ACCOUNTING_API = "http://localhost:3001"
CSV_FILE = "users.csv"

def log(message, status="INFO"):
    """Simple logging"""
    symbols = {"SUCCESS": "✓", "ERROR": "✗", "INFO": "►", "WARNING": "⚠"}
    print(f"{symbols.get(status, '•')} {message}")

def read_csv():
    """Read users from CSV"""
    users = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows, comments, and non-create actions
                if not row.get('action') or row['action'].startswith('#') or row['action'].lower() != 'create':
                    continue
                
                users.append({
                    'username': row['username'].strip(),
                    'password': row['password'].strip(),
                })
        return users
    except FileNotFoundError:
        log(f"CSV file not found: {CSV_FILE}", "ERROR")
        return []
    except Exception as e:
        log(f"Error reading CSV: {str(e)}", "ERROR")
        return []

def login_user(username, password):
    """Login user and check balance to trigger auto-creation"""
    try:
        # Step 1: Login
        response = requests.post(
            f"{AUTH_API}/api/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code != 200:
            log(f"  Login failed for {username}: {response.status_code} - {response.text}", "ERROR")
            return False
        
        token = response.json().get("accessToken")
        
        # Step 2: Check balance (triggers auto-creation in accounting DB)
        balance_response = requests.get(
            f"{ACCOUNTING_API}/api/credits/balance",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if balance_response.status_code == 200:
            log(f"Initialized {username} in accounting service", "SUCCESS")
            return True
        else:
            log(f"  Balance check failed for {username}: {balance_response.status_code}", "WARNING")
            return False
            
    except Exception as e:
        log(f"  Error for {username}: {str(e)}", "ERROR")
        return False

def main():
    print("=" * 60)
    print("Initialize Users in Accounting Service")
    print("=" * 60)
    print()
    
    # Read users from CSV
    users = read_csv()
    if not users:
        log("No users found in CSV", "WARNING")
        input("\nPress Enter to exit...")
        sys.exit(0)
    
    log(f"Found {len(users)} users", "INFO")
    print()
    
    # Initialize each user
    success_count = 0
    error_count = 0
    
    for user_data in users:
        username = user_data['username']
        password = user_data['password']
        
        if login_user(username, password):
            success_count += 1
        else:
            error_count += 1
    
    # Summary
    print()
    print("=" * 60)
    log("Initialization complete!", "SUCCESS")
    log(f"Success: {success_count} | Errors: {error_count}", "INFO")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
