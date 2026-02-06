# Cybersecurity Platform - Backend API

Simple backend server that works with both Web and Android applications.

## Features

✅ **API Key Management**
- Generate secure API keys
- Auto-expiration (default 90 days)
- API key viewer with masked keys
- Key rotation support
- TLS 1.3 security

✅ **Authentication**
- User registration and login
- JWT token-based auth
- Secure password hashing (bcrypt)

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

Server will start at: `http://localhost:8000`

### 3. Test the API

Open browser: `http://localhost:8000/docs`

You'll see interactive API documentation (Swagger UI)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### API Key Management
- `POST /api/keys/generate` - Generate new API key
- `GET /api/keys` - List all API keys (viewer)
- `GET /api/keys/{key_id}` - Get specific key details
- `DELETE /api/keys/{key_id}` - Revoke API key
- `POST /api/keys/{key_id}/rotate` - Rotate API key
- `POST /api/keys/validate` - Validate API key

## Security Features

1. **TLS 1.3** - Modern encryption
2. **JWT Tokens** - Secure authentication
3. **Bcrypt** - Password hashing
4. **Auto-expiration** - Keys expire after set time
5. **Key masking** - Only show preview in viewer

## Database

Uses SQLite for development (file: `cybersecurity_platform.db`)

For production, switch to PostgreSQL in `database.py`

## Next Steps

After backend is running:
1. Test endpoints using Swagger UI
2. Build Flutter frontend
3. Connect Android app to this API

## Project Structure

```
backend/
├── main.py              # Main API server
├── models.py            # Database models
├── database.py          # Database config
├── auth.py              # Authentication
├── api_key_service.py   # API key logic
├── requirements.txt     # Dependencies
└── README.md           # This file
```
