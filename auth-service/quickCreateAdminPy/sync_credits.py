#!/usr/bin/env python3
"""
Simple CSV Credit Management Script
Reads users.csv and SETS (replaces) credit amounts for each user.
Safe to run multiple times - credits will be set to exact CSV amounts.
"""

import csv
import requests
import sys
import os

# Configuration
AUTH_API = "http://localhost:3000"
ACCOUNTING_API = "http://localhost:3001"
CSV_FILE = "users.csv"

ADMIN_USER = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin@admin",
}

def log(message, status="INFO"):
    """Simple logging"""
    symbols = {"SUCCESS": "✓", "ERROR": "✗", "INFO": "►", "WARNING": "⚠"}
    print(f"{symbols.get(status, '•')} {message}")

def login_admin():
    """Login and get admin token"""
    try:
        response = requests.post(
            f"{AUTH_API}/api/auth/login",
            json=ADMIN_USER,
            timeout=10
        )
        if response.status_code == 200:
            token = response.json().get("accessToken")
            log("Admin login successful", "SUCCESS")
            return token
        else:
            log(f"Login failed: {response.text}", "ERROR")
            return None
    except Exception as e:
        log(f"Login error: {str(e)}", "ERROR")
        return None

def get_user_by_email(email, token):
    """Get user ID from email"""
    try:
        import urllib.parse
        encoded_email = urllib.parse.quote(email, safe="")
        response = requests.get(
            f"{AUTH_API}/api/admin/users/by-email/{encoded_email}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("user")
        return None
    except Exception:
        return None

def get_user_balance(email, token):
    """Get user's current credit balance from accounting service"""
    try:
        # First get user from auth to get their ID
        user = get_user_by_email(email, token)
        if not user:
            return None
        
        user_id = user.get('_id')
        
        # Get balance from accounting service
        response = requests.get(
            f"{ACCOUNTING_API}/api/credits/balance/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('totalCredits', 0)
        return 0
    except Exception:
        return 0

def set_credits(email, credits, token):
    """Set credits for a user by email (replaces existing credits)"""
    try:
        # Get current balance
        current_balance = get_user_balance(email, token)
        if current_balance is None:
            log(f"  User not found in accounting system: {email}", "ERROR")
            return False
        
        target_credits = int(credits)
        
        # If balance matches, skip
        if current_balance == target_credits:
            return True
        
        # Calculate difference
        diff = target_credits - current_balance
        
        if diff > 0:
            # Need to add credits (allocate)
            response = requests.post(
                f"{ACCOUNTING_API}/api/credits/allocate-by-email",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "email": email,
                    "credits": diff,
                    "notes": f"Adjust to {target_credits} via CSV sync (+{diff})"
                },
                timeout=10
            )
        else:
            # Need to remove credits
            user = get_user_by_email(email, token)
            if not user:
                return False
            
            user_id = user.get('_id')
            response = requests.delete(
                f"{ACCOUNTING_API}/api/credits/remove",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "userId": user_id,
                    "credits": abs(diff),
                    "notes": f"Adjust to {target_credits} via CSV sync ({diff})"
                },
                timeout=10
            )
        
        if response.status_code in [200, 201]:
            return True
        else:
            log(f"  API Error: {response.status_code} - {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"  Exception: {str(e)}", "ERROR")
        return False

def read_csv():
    """Read users and credits from CSV"""
    users = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows, comments, and non-create actions
                if not row.get('action') or row['action'].startswith('#') or row['action'].lower() != 'create':
                    continue
                
                # Only process rows with credits
                if row.get('credits'):
                    users.append({
                        'email': row['email'].strip(),
                        'username': row['username'].strip(),
                        'credits': row['credits'].strip()
                    })
        return users
    except FileNotFoundError:
        log(f"CSV file not found: {CSV_FILE}", "ERROR")
        return []
    except Exception as e:
        log(f"Error reading CSV: {str(e)}", "ERROR")
        return []

def main():
    print("=" * 60)
    print("Simple Credit Management - CSV Sync")
    print("=" * 60)
    print()
    
    # Check CSV exists
    if not os.path.exists(CSV_FILE):
        log(f"CSV file not found: {CSV_FILE}", "ERROR")
        log("Please create users.csv with email and credits columns", "INFO")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Read users from CSV
    users = read_csv()
    if not users:
        log("No users with credits found in CSV", "WARNING")
        input("\nPress Enter to exit...")
        sys.exit(0)
    
    log(f"Found {len(users)} users with credit amounts", "INFO")
    print()
    
    # Login as admin
    token = login_admin()
    if not token:
        log("Failed to login. Cannot proceed.", "ERROR")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print()
    log("Setting credits for each user...", "INFO")
    print()
    
    # Process each user
    success_count = 0
    error_count = 0
    
    for user_data in users:
        email = user_data['email']
        credits = user_data['credits']
        username = user_data['username']
        
        # Set credits using email (no need to look up user ID)
        if set_credits(email, credits, token):
            log(f"Set {credits} credits for {username} ({email})", "SUCCESS")
            success_count += 1
        else:
            log(f"Failed to set credits for {username} ({email})", "ERROR")
            error_count += 1
    
    # Summary
    print()
    print("=" * 60)
    log("Credit sync complete!", "SUCCESS")
    log(f"Success: {success_count} | Errors: {error_count}", "INFO")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
