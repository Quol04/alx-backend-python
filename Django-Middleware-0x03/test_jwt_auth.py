#!/usr/bin/env python3
"""
Test script to verify JWT authentication is working correctly.
Run this script while the Django server is running.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_jwt_authentication():
    """Test JWT authentication flow"""
    print("🔐 Testing JWT Authentication for Messaging App")
    print("=" * 50)
    
    # Test 1: Access protected endpoint without authentication (should fail)
    print("\n1️⃣ Testing protected endpoint without authentication...")
    response = requests.get(f"{BASE_URL}/api/conversations/")
    print(f"Status: {response.status_code}")
    if response.status_code == 401:
        print("✅ Correctly rejected unauthenticated request")
    else:
        print("❌ Should have rejected unauthenticated request")
    
    # Test 2: Check JWT endpoints exist
    print("\n2️⃣ Testing JWT endpoint availability...")
    endpoints_to_test = [
        "/api/auth/login/",
        "/api/auth/refresh/", 
        "/api/auth/verify/"
    ]
    
    for endpoint in endpoints_to_test:
        response = requests.post(f"{BASE_URL}{endpoint}")
        print(f"POST {endpoint}: {response.status_code}")
        if response.status_code in [400, 405]:  # Bad request or method not allowed (but endpoint exists)
            print(f"✅ {endpoint} endpoint is available")
        elif response.status_code == 404:
            print(f"❌ {endpoint} endpoint not found")
        else:
            print(f"ℹ️ {endpoint} returned {response.status_code}")
    
    # Test 3: Try to login (this will fail without valid credentials but shows the endpoint works)
    print("\n3️⃣ Testing login endpoint structure...")
    login_data = {
        "username": "test_user",
        "password": "test_password"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login/", data=login_data)
    print(f"Login attempt status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Login endpoint working (rejected invalid credentials)")
    elif response.status_code == 400:
        print("✅ Login endpoint working (bad request format)")
    else:
        print(f"ℹ️ Login endpoint returned: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print("Non-JSON response")
    
    print("\n" + "=" * 50)
    print("🎉 JWT Authentication Test Complete!")
    print("\n📋 To test full authentication:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Use those credentials to get JWT tokens")
    print("3. Include 'Authorization: Bearer <token>' in API requests")

if __name__ == "__main__":
    try:
        test_jwt_authentication()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Django server.")
        print("Make sure the server is running: python manage.py runserver")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")