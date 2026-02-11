#!/usr/bin/env python3
"""
CSV User Management Script
Manages users in the auth service by reading from a CSV file.
Supports both creating and deleting users.
"""

import csv
import json
import requests
import sys
import os
import datetime
from typing import Dict, List

# Configuration
API_BASE_URL = "http://localhost:3000"
ACCOUNTING_API = "http://localhost:3001"
CSV_FILE = "users.csv"
LOG_FILE = "user_management.log"

ADMIN_USER = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin@admin",
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_message(message: str, log_type: str = "INFO"):
    """Log message to file and console"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{log_type}] {message}"
    
    # Write to log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    
    # Print to console with color
    color = Colors.GREEN if log_type == "SUCCESS" else Colors.RED if log_type == "ERROR" else Colors.YELLOW if log_type == "WARNING" else Colors.BLUE
    print(f"{color}{log_entry}{Colors.END}")

def login_admin() -> str:
    """Login as admin and return JWT token"""
    try:
        log_message("Logging in as admin...", "INFO")
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json=ADMIN_USER,
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json()["accessToken"]
            log_message("Admin login successful", "SUCCESS")
            return token
        else:
            log_message(f"Admin login failed: {response.text}", "ERROR")
            return None
    except Exception as e:
        log_message(f"Admin login error: {str(e)}", "ERROR")
        return None

def check_user_exists(email: str, token: str) -> Dict:
    """Check if user exists by email"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_BASE_URL}/api/users",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            users = response.json()
            for user in users:
                if user.get("email") == email:
                    return user
        return None
    except Exception:
        return None

def create_user(user_data: Dict, token: str, skip_existing: bool = True) -> bool:
    """Create a new user"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Check if user already exists
        existing_user = check_user_exists(user_data["email"], token)
        
        if existing_user:
            if skip_existing:
                log_message(f"⊘ User already exists, skipping: {user_data['username']} ({user_data['email']}) - Role: {existing_user.get('role', 'unknown')}", "WARNING")
                return True  # Return True to not count as error
            else:
                log_message(f"✗ User already exists: {user_data['username']} ({user_data['email']})", "ERROR")
                return False
        
        # Prepare payload
        payload = {
            "username": user_data["username"],
            "email": user_data["email"],
            "password": user_data["password"],
            "role": user_data.get("role", "enduser")
        }
        
        if user_data.get("fullName"):
            payload["fullName"] = user_data["fullName"]
        
        response = requests.post(
            f"{API_BASE_URL}/api/auth/signup",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            user_id = response.json().get("_id", "unknown")
            log_message(f"✓ Created user: {user_data['username']} ({user_data['email']}) - Role: {user_data.get('role', 'enduser')} - ID: {user_id}", "SUCCESS")
            return True
        else:
            log_message(f"✗ Failed to create user {user_data['username']}: {response.text}", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"✗ Error creating user {user_data['username']}: {str(e)}", "ERROR")
        return False

def delete_user(user_data: Dict, token: str) -> bool:
    """Delete a user by email"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # First, get user ID by email
        response = requests.get(
            f"{API_BASE_URL}/api/admin/users",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            users_data = response.json()
            users = users_data.get('users', [])
            target_user = None
            
            for user in users:
                if user.get("email") == user_data["email"]:
                    target_user = user
                    break
            
            if not target_user:
                log_message(f"✗ User not found: {user_data['email']}", "WARNING")
                return False
            
            # Delete the user
            user_id = target_user["_id"]
            delete_response = requests.delete(
                f"{API_BASE_URL}/api/admin/users/{user_id}",
                headers=headers,
                timeout=10
            )
            
            if delete_response.status_code in [200, 204]:
                log_message(f"✓ Deleted user: {user_data['username']} ({user_data['email']})", "SUCCESS")
                
                # Also remove credits from accounting service
                try:
                    balance_response = requests.get(
                        f"{ACCOUNTING_API}/api/credits/balance/{user_id}",
                        headers=headers,
                        timeout=10
                    )
                    
                    if balance_response.status_code == 200:
                        balance_data = balance_response.json()
                        total_credits = balance_data.get('totalCredits', 0)
                        
                        if total_credits > 0:
                            # Remove all credits
                            remove_response = requests.delete(
                                f"{ACCOUNTING_API}/api/credits/remove",
                                headers=headers,
                                json={
                                    "userId": user_id,
                                    "credits": total_credits,
                                    "notes": f"Removed credits due to user deletion"
                                },
                                timeout=10
                            )
                            
                            if remove_response.status_code == 200:
                                log_message(f"  ✓ Removed {total_credits} credits from accounting", "SUCCESS")
                            else:
                                log_message(f"  ⚠ Could not remove credits: {remove_response.text}", "WARNING")
                        else:
                            log_message(f"  → No credits to remove", "INFO")
                except Exception as credit_error:
                    log_message(f"  ⚠ Could not check/remove credits: {str(credit_error)}", "WARNING")
                
                return True
            else:
                log_message(f"✗ Failed to delete user {user_data['email']}: {delete_response.text}", "ERROR")
                return False
        else:
            log_message(f"✗ Failed to fetch users: {response.text}", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"✗ Error deleting user {user_data['email']}: {str(e)}", "ERROR")
        return False

def read_csv(filename: str) -> List[Dict]:
    """Read users from CSV file"""
    users = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Skip empty rows and comments
                if not row.get('action') or row['action'].startswith('#'):
                    continue
                
                # Clean up whitespace
                cleaned_row = {k: v.strip() if v else v for k, v in row.items()}
                users.append(cleaned_row)
        
        log_message(f"Read {len(users)} users from {filename}", "INFO")
        return users
        
    except FileNotFoundError:
        log_message(f"CSV file not found: {filename}", "ERROR")
        return []
    except Exception as e:
        log_message(f"Error reading CSV: {str(e)}", "ERROR")
        return []

def main():
    """Main function"""
    print("=" * 60)
    print("CSV User Management Script")
    print("=" * 60)
    print()
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        log_message(f"CSV file not found: {CSV_FILE}", "ERROR")
        log_message("Please create a users.csv file or copy from users_template.csv", "INFO")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Read users from CSV
    users = read_csv(CSV_FILE)
    
    if not users:
        log_message("No users to process", "WARNING")
        input("\nPress Enter to exit...")
        sys.exit(0)
    
    # Login as admin
    token = login_admin()
    
    if not token:
        log_message("Failed to login as admin. Cannot proceed.", "ERROR")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Process users
    create_count = 0
    delete_count = 0
    skip_count = 0
    error_count = 0
    
    print()
    log_message(f"Processing {len(users)} user actions...", "INFO")
    log_message("Note: Existing users will be skipped (not recreated)", "INFO")
    print()
    
    for user in users:
        action = user.get('action', '').lower()
        
        if action == 'create':
            # Check if user exists before attempting create
            existing = check_user_exists(user.get('email'), token)
            if existing:
                log_message(f"⊘ User already exists, skipping: {user.get('username')} ({user.get('email')})", "WARNING")
                skip_count += 1
            else:
                if create_user(user, token, skip_existing=True):
                    create_count += 1
                else:
                    error_count += 1
                
        elif action == 'delete':
            if delete_user(user, token):
                delete_count += 1
            else:
                error_count += 1
        else:
            log_message(f"Unknown action '{action}' for user {user.get('email')}", "WARNING")
    
    # Summary
    print()
    print("=" * 60)
    log_message("Processing complete!", "SUCCESS")
    log_message(f"Created: {create_count} | Skipped: {skip_count} | Deleted: {delete_count} | Errors: {error_count}", "INFO")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
