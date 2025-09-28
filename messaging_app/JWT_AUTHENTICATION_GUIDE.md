# 🔐 JWT Authentication API Usage Guide

## Overview

Your Django messaging app now has complete JWT (JSON Web Token) authentication implemented with the following features:

- ✅ JWT token-based authentication
- ✅ Session authentication (for browsable API)
- ✅ Secure user isolation (users only see their own data)
- ✅ Token refresh mechanism
- ✅ Proper permission controls

## 🚀 Getting Started

### 1. Authentication Endpoints

| Endpoint             | Method | Purpose               | Payload                                    |
| -------------------- | ------ | --------------------- | ------------------------------------------ |
| `/api/auth/login/`   | POST   | Get JWT tokens        | `{"username": "user", "password": "pass"}` |
| `/api/auth/refresh/` | POST   | Refresh access token  | `{"refresh": "refresh_token_here"}`        |
| `/api/auth/verify/`  | POST   | Verify token validity | `{"token": "access_token_here"}`           |

### 2. Protected API Endpoints

| Endpoint                            | Method    | Purpose                   | Authentication Required |
| ----------------------------------- | --------- | ------------------------- | ----------------------- |
| `/api/conversations/`               | GET, POST | List/Create conversations | ✅                      |
| `/api/messages/`                    | GET, POST | List/Create messages      | ✅                      |
| `/api/conversations/{id}/messages/` | GET, POST | Messages in conversation  | ✅                      |

## 📖 Usage Examples

### Step 1: Login and Get Tokens

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Response:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Step 2: Use Access Token for API Requests

```bash
curl -X GET http://127.0.0.1:8000/api/conversations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json"
```

### Step 3: Create a Conversation

```bash
curl -X POST http://127.0.0.1:8000/api/conversations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"participants": ["user_id_1", "user_id_2"]}'
```

### Step 4: Send a Message

```bash
curl -X POST http://127.0.0.1:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": "conversation_id_here",
    "message_body": "Hello, this is a test message!"
  }'
```

### Step 5: Refresh Token When Expired

```bash
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN_HERE"}'
```

## 🔧 Python Usage Example

```python
import requests

# Login
login_response = requests.post('http://127.0.0.1:8000/api/auth/login/', json={
    'username': 'your_username',
    'password': 'your_password'
})
tokens = login_response.json()

# Set up headers for authenticated requests
headers = {
    'Authorization': f'Bearer {tokens["access"]}',
    'Content-Type': 'application/json'
}

# Get conversations
conversations = requests.get('http://127.0.0.1:8000/api/conversations/', headers=headers)
print(conversations.json())

# Create conversation
new_conversation = requests.post('http://127.0.0.1:8000/api/conversations/',
    headers=headers,
    json={'participants': ['user_id_here']})

# Send message
message = requests.post('http://127.0.0.1:8000/api/messages/',
    headers=headers,
    json={
        'conversation': 'conversation_id',
        'message_body': 'Hello World!'
    })
```

## 🛡️ Security Features

1. **User Isolation**: Users can only see conversations and messages they participate in
2. **Token Expiration**: Access tokens expire in 60 minutes
3. **Refresh Tokens**: Refresh tokens expire in 7 days
4. **Token Rotation**: Refresh tokens are rotated on use
5. **Blacklist After Rotation**: Old refresh tokens are blacklisted

## ⚙️ Token Settings

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Algorithm**: HS256
- **Token Rotation**: Enabled
- **Blacklist After Rotation**: Enabled

## 🧪 Testing Your Implementation

You can use the provided test scripts:

- `test_jwt_auth.py` - Basic JWT endpoint testing
- `test_jwt_complete.py` - Comprehensive authentication testing

## 🚨 Important Notes

1. **Always use HTTPS in production**
2. **Keep tokens secure** - never expose them in client-side code
3. **Handle token expiration** - implement refresh logic
4. **Use proper error handling** for authentication failures
5. **Monitor token usage** for security

## 📚 API Response Examples

### Successful Conversation List

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "conversation_id": "abc-123-def",
      "participants": ["user1", "user2"],
      "created_at": "2025-09-28T19:00:00Z"
    }
  ]
}
```

### Authentication Error

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Token Expired Error

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

## 🎉 Congratulations!

Your messaging app now has complete JWT authentication implemented! Users can:

- ✅ Authenticate and receive JWT tokens
- ✅ Use tokens to access protected API endpoints
- ✅ Only access their own conversations and messages
- ✅ Refresh tokens when they expire
- ✅ Create conversations and send messages securely
