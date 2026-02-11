"""
Sync admin user, assign all chatflows, and initialize credits
This creates the admin user in flowise-proxy database, assigns all chatflows,
and sets up 5000 credits in the accounting service
"""
import pymongo
import requests
from datetime import datetime

# MongoDB connection
MONGODB_URL = "mongodb://admin:65424b6a739b4198ae2a3e08b35deeda@mongodb-proxy:27017/flowise_proxy?authSource=admin"

# Services
AUTH_SERVICE_URL = "http://auth-service:3000"
ACCOUNTING_SERVICE_URL = "http://accounting-service:3001"

# Admin user info from auth-service
ADMIN_USER = {
    "_id": "698abefd8e7d94abc0c0bbc2",  # From auth-service
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin@admin",  # For authentication
    "role": "admin",
    "is_verified": True,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# Initial credits for admin
ADMIN_CREDITS = 5000

def get_admin_token():
    """Login to auth service and get admin token"""
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/api/auth/login",
            json={
                "username": ADMIN_USER["username"],
                "password": ADMIN_USER["password"]
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("accessToken") or data.get("token", {}).get("accessToken")
            if token:
                return token
            else:
                print(f"   ⚠️  No token in auth response")
                return None
        else:
            print(f"   ⚠️  Auth login failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ⚠️  Auth error: {str(e)}")
        return None

def sync_admin_and_chatflows():
    print("Connecting to MongoDB...")
    client = pymongo.MongoClient(MONGODB_URL)
    db = client.flowise_proxy
    
    # 1. Create admin user if not exists
    print("\n1. Checking admin user...")
    existing_user = db.users.find_one({"_id": ADMIN_USER["_id"]})
    
    if existing_user:
        print(f"   ✅ Admin user already exists: {existing_user['username']}")
    else:
        db.users.insert_one(ADMIN_USER)
        print(f"   ✅ Created admin user: {ADMIN_USER['username']}")
    
    # 2. Get all chatflows
    print("\n2. Getting all chatflows...")
    chatflows = list(db.Chatflow.find())
    print(f"   Found {len(chatflows)} chatflows")
    
    # 3. Assign all chatflows to admin
    print("\n3. Assigning chatflows to admin...")
    for chatflow in chatflows:
        chatflow_id = str(chatflow["_id"])
        
        # Check if already assigned
        existing = db.user_chatflows.find_one({
            "user_id": ADMIN_USER["_id"],
            "chatflow_id": chatflow_id
        })
        
        if existing:
            print(f"   ⏭️  Already assigned: {chatflow['name']}")
        else:
            assignment = {
                "user_id": ADMIN_USER["_id"],
                "chatflow_id": chatflow_id,
                "assigned_at": datetime.utcnow(),
                "is_active": True
            }
            db.user_chatflows.insert_one(assignment)
            print(f"   ✅ Assigned: {chatflow['name']} (ID: {chatflow_id})")
    
    print("\n✅ Sync complete!")
    print(f"\nAdmin user '{ADMIN_USER['username']}' now has access to {len(chatflows)} chatflow(s)")
    
    # 4. Initialize credits in accounting service
    print("\n4. Initializing credits in accounting service...")
    
    # Get admin token for authentication
    admin_token = get_admin_token()
    if not admin_token:
        print(f"   ❌ Could not get admin token - skipping credit allocation")
        print(f"   ℹ️  Make sure auth-service is running")
    else:
        try:
            # Allocate credits using admin token
            credit_response = requests.post(
                f"{ACCOUNTING_SERVICE_URL}/api/credits/allocate-by-email",
                headers={
                    "Authorization": f"Bearer {admin_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "email": ADMIN_USER["email"],
                    "credits": ADMIN_CREDITS,
                    "expiryDays": 3650,  # 10 years
                    "notes": "Initial credit allocation for admin user"
                },
                timeout=5
            )
            
            if credit_response.status_code == 201:
                data = credit_response.json()
                print(f"   ✅ Credits allocated: {ADMIN_CREDITS} credits")
                print(f"      Balance: {data.get('data', {}).get('current_credits', ADMIN_CREDITS)}")
            elif credit_response.status_code == 409:
                print(f"   ⏭️  Credits already allocated")
            else:
                print(f"   ⚠️  Credit allocation returned: {credit_response.status_code}")
                print(f"      Response: {credit_response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  Could not connect to accounting service at {ACCOUNTING_SERVICE_URL}")
            print(f"   ℹ️  Make sure accounting service is running")
        except Exception as e:
            print(f"   ⚠️  Error allocating credits: {str(e)}")
    
    print("\n" + "="*60)
    print(f"✅ SETUP COMPLETE!")
    print(f"   User: {ADMIN_USER['username']}")
    print(f"   Chatflows: {len(chatflows)}")
    print(f"   Credits: {ADMIN_CREDITS}")
    print("="*60)
    
    client.close()

if __name__ == "__main__":
    sync_admin_and_chatflows()

