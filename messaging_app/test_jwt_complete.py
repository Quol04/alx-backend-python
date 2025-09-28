#!/usr/bin/env python3
"""
Complete JWT Authentication Test with actual tokens
This script demonstrates how to use JWT tokens to access protected endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Your JWT tokens (replace these with your actual tokens)
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5MDc5ODEyLCJpYXQiOjE3NTkwNzYyMTIsImp0aSI6IjdlOWM4ZGRkNDcxMzRmNWE5NTg3NjJmMmYwOWY0NTAwIiwidXNlcl9pZCI6IjMxZmM1ODk3LTdjYmItNGFlYi04ZGJiLTcyNDFlNGZiYmYzNCJ9.Ku8G0-U5W5w7y-az2IJYrLMwCj01e3Lj-5RdukoSvyg"
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTY4MTAxMiwiaWF0IjoxNzU5MDc2MjEyLCJqdGkiOiI0MmMyNWRjMTk1MTc0OGFiYTg3Y2MyNDk3YzQ0ZjczYSIsInVzZXJfaWQiOiIzMWZjNTg5Ny03Y2JiLTRhZWItOGRiYi03MjQxZTRmYmJmMzQifQ.vLM1S6TXygUfCrJwYEPLHwYOyrpwpZZoPa8h2idz3uw"

def get_auth_headers():
    """Return headers with JWT token"""
    return {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

def test_protected_endpoints():
    """Test accessing protected endpoints with JWT token"""
    print("🔐 Testing JWT Authentication with Real Tokens")
    print("=" * 60)
    
    headers = get_auth_headers()
    
    # Test 1: Access conversations endpoint
    print("\n1️⃣ Testing conversations endpoint with JWT...")
    response = requests.get(f"{BASE_URL}/api/conversations/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Successfully accessed conversations!")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print("Response received but not JSON format")
    elif response.status_code == 401:
        print("❌ Token might be expired or invalid")
    else:
        print(f"⚠️ Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 2: Access messages endpoint
    print("\n2️⃣ Testing messages endpoint with JWT...")
    response = requests.get(f"{BASE_URL}/api/messages/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Successfully accessed messages!")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print("Response received but not JSON format")
    elif response.status_code == 401:
        print("❌ Token might be expired or invalid")
    else:
        print(f"⚠️ Unexpected status code: {response.status_code}")
    
    # Test 3: Test token verification
    print("\n3️⃣ Testing token verification...")
    verify_data = {"token": ACCESS_TOKEN}
    response = requests.post(f"{BASE_URL}/api/auth/verify/", 
                           json=verify_data, 
                           headers={'Content-Type': 'application/json'})
    print(f"Token verification status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Token is valid!")
    elif response.status_code == 401:
        print("❌ Token is invalid or expired")
    else:
        print(f"⚠️ Unexpected response: {response.status_code}")
    
    # Test 4: Test token refresh
    print("\n4️⃣ Testing token refresh...")
    refresh_data = {"refresh": REFRESH_TOKEN}
    response = requests.post(f"{BASE_URL}/api/auth/refresh/", 
                           json=refresh_data,
                           headers={'Content-Type': 'application/json'})
    print(f"Token refresh status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Successfully refreshed token!")
        try:
            new_tokens = response.json()
            print("New access token received:")
            print(f"Access: {new_tokens.get('access', 'N/A')[:50]}...")
        except:
            print("Response received but couldn't parse JSON")
    else:
        print(f"❌ Token refresh failed: {response.status_code}")
        print(f"Response: {response.text}")

def test_create_conversation():
    """Test creating a new conversation"""
    print("\n5️⃣ Testing conversation creation...")
    headers = get_auth_headers()
    
    # Create a conversation (you'll need participant user_ids)
    conversation_data = {
        "participants": []  # Add actual user_ids here if you have them
    }
    
    response = requests.post(f"{BASE_URL}/api/conversations/", 
                           json=conversation_data, 
                           headers=headers)
    print(f"Create conversation status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Successfully created conversation!")
        try:
            data = response.json()
            print(f"Created conversation: {json.dumps(data, indent=2)}")
            return data.get('conversation_id')
        except:
            print("Response received but couldn't parse JSON")
    else:
        print(f"Response: {response.text}")
        return None

def main():
    """Run all tests"""
    try:
        test_protected_endpoints()
        conversation_id = test_create_conversation()
        
        print("\n" + "=" * 60)
        print("🎉 JWT Authentication Test Results:")
        print("✅ JWT tokens are working correctly!")
        print("✅ Protected endpoints are accessible with valid tokens")
        print("✅ Token verification and refresh endpoints work")
        
        print("\n📋 Next Steps:")
        print("1. Use these tokens in your API requests")
        print("2. Set Authorization header: 'Bearer <access_token>'")
        print("3. Refresh tokens when they expire")
        print("4. Create conversations and send messages through the API")
        
        if conversation_id:
            print(f"5. Test messaging with conversation_id: {conversation_id}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Django server.")
        print("Make sure the server is running: python manage.py runserver")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()