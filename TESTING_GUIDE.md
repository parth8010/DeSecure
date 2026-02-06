# 🧪 Testing Guide - Web Application

Complete guide to test your cybersecurity platform web application.

---

## 🎯 Testing Scenarios

### Scenario 1: Test Locally (Before Deployment)
### Scenario 2: Test with Railway Backend
### Scenario 3: Test Production Deployment

---

# Scenario 1: Test Locally 🏠

## Prerequisites

1. **Backend running locally:**
   ```bash
   python main.py
   ```
   Should show: `Uvicorn running on http://0.0.0.0:8000`

2. **Frontend ready:**
   ```bash
   cd frontend
   ```

---

## Method 1: Open HTML File Directly

**Simplest way to test:**

1. **Navigate to frontend folder**
2. **Double-click `index.html`**
3. **Or right-click → Open with → Your browser**

✅ **Expected:** App opens in browser

---

## Method 2: Use Python HTTP Server (Recommended)

**Better for testing (avoids CORS issues):**

```bash
cd frontend
python -m http.server 3000
```

**Open browser:**
```
http://localhost:3000
```

✅ **Expected:** App loads at localhost:3000

---

## Method 3: Use Node.js HTTP Server

```bash
cd frontend
npx http-server -p 3000
```

**Open browser:**
```
http://localhost:3000
```

---

## 🧪 Test Checklist - Local

Open browser console (F12) and check:

### 1. **Check Configuration**
   ```
   Console should show:
   🔧 Frontend Configuration:
     Environment: Development
     Backend URL: http://localhost:8000
   ```

### 2. **Test User Registration**
   - Click "Sign Up" tab
   - Fill in:
     - Email: `test@example.com`
     - Username: `testuser`
     - Password: `password123`
   - Click "Register"
   
   ✅ **Expected:** 
   - Success message appears
   - User is logged in
   - Dashboard shows

### 3. **Test User Login**
   - Logout if needed
   - Click "Sign In" tab
   - Enter credentials
   - Click "Login"
   
   ✅ **Expected:** 
   - Login successful
   - Dashboard loads

### 4. **Test API Key Generation**
   - Go to "API Keys" tab
   - Enter:
     - Name: `Test Key`
     - Description: `Testing API keys`
     - Expiry: `90` days
   - Click "Generate Key"
   
   ✅ **Expected:**
   - API key generated
   - Key displayed (copy it!)
   - Key appears in list

### 5. **Test Wallet Creation**
   - Go to "Crypto Wallet" tab
   - Enter password: `MySecurePassword123`
   - Click "Create Wallet"
   
   ✅ **Expected:**
   - Wallet created
   - Recovery phrase shown
   - Wallet ID displayed

### 6. **Test Wallet Sign Message**
   - Enter wallet password
   - Enter message: `Hello World`
   - Click "Sign Message"
   
   ✅ **Expected:**
   - Message signed
   - Signature displayed

---

# Scenario 2: Test with Railway Backend 🚂

## Prerequisites

1. **Backend deployed to Railway**
2. **Frontend config updated with Railway URL**

---

## Setup

### Option A: Force Railway in Local Frontend

**Edit `frontend/config.js`:**
```javascript
FORCE_RAILWAY: true,  // Change to true
```

**Open frontend:**
```bash
cd frontend
python -m http.server 3000
```

**Check console (F12):**
```
Backend URL: https://your-app.up.railway.app
```

### Option B: Deploy Frontend

Deploy to Netlify/GitHub Pages and test from there.

---

## 🧪 Test Checklist - Railway Backend

### 1. **Test Backend Health**

Open in browser:
```
https://your-app.up.railway.app/health
```

✅ **Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-02-07T..."
}
```

### 2. **Test API Documentation**

Open in browser:
```
https://your-app.up.railway.app/docs
```

✅ **Expected:** 
- FastAPI Swagger UI loads
- All endpoints listed

### 3. **Test Registration via API Docs**

In Swagger UI:
1. Find `POST /api/auth/register`
2. Click "Try it out"
3. Enter:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "password123"
   }
   ```
4. Click "Execute"

✅ **Expected:**
```json
{
  "message": "User registered successfully",
  "user": {...},
  "access_token": "eyJ..."
}
```

### 4. **Test Frontend with Railway**

Open frontend → Test all features (same as Scenario 1)

✅ **Expected:** Everything works the same!

---

# Scenario 3: Test Production Deployment 🌐

## Prerequisites

1. **Backend deployed to Railway**
2. **Frontend deployed to Netlify/GitHub Pages**

---

## 🧪 Full Production Test

### 1. **Access Your Live App**

**Netlify:**
```
https://your-app.netlify.app
```

**GitHub Pages:**
```
https://parth8010.github.io/DeSecure/
```

### 2. **Check Console (F12)**

✅ **Expected:**
```
Backend URL: https://your-app.up.railway.app
```

### 3. **Complete User Flow Test**

#### A. Registration
1. Open your production URL
2. Click "Sign Up"
3. Register new user
4. ✅ Should auto-login

#### B. Logout and Login
1. Logout
2. Click "Sign In"
3. Login with credentials
4. ✅ Should show dashboard

#### C. Generate API Key
1. Go to API Keys tab
2. Create a new key
3. Copy the key (shown once!)
4. ✅ Key appears in list

#### D. Test API Key Validation
1. Open new browser tab
2. Go to Railway docs: `https://your-app.up.railway.app/docs`
3. Test `POST /api/keys/validate`
4. Add header: `X-API-Key: your-key-here`
5. ✅ Should validate successfully

#### E. Create Wallet
1. Go to Crypto Wallet tab
2. Enter password
3. Create wallet
4. **SAVE RECOVERY PHRASE!**
5. ✅ Wallet created

#### F. Sign Message
1. Enter wallet password
2. Enter message
3. Sign
4. ✅ Signature generated

#### G. Verify Signature
1. Copy signature
2. Go to verify tab
3. Paste message and signature
4. ✅ Should verify as valid

---

## 🐛 Debugging & Troubleshooting

### Browser Console Errors

**Open Console (F12) and check for:**

#### Error: "Failed to fetch"
**Cause:** Backend not running or wrong URL

**Fix:**
1. Check backend health: `curl https://your-app.up.railway.app/health`
2. Verify RAILWAY_URL in `config.js`
3. Check Railway deployment logs

#### Error: "CORS policy blocked"
**Cause:** Frontend domain not in CORS_ORIGINS

**Fix:**
Add to Railway variables:
```
CORS_ORIGINS=https://your-frontend-domain.com
```

#### Error: "Invalid token" or "Unauthorized"
**Cause:** Token expired or invalid

**Fix:**
1. Clear browser localStorage
2. Logout and login again
3. Register new user

#### Error: "Network Error"
**Cause:** Backend not accessible

**Fix:**
1. Test backend: `https://your-app.up.railway.app/health`
2. Check Railway logs
3. Verify DATABASE_URL is set

---

## 🔍 Network Tab Inspection

**Open Browser DevTools (F12) → Network Tab**

### What to Check:

1. **Click "Register"** and watch requests:
   - ✅ Request to: `POST /api/auth/register`
   - ✅ Status: `201 Created`
   - ✅ Response contains: `access_token`

2. **Click "Login"** and watch:
   - ✅ Request to: `POST /api/auth/login`
   - ✅ Status: `200 OK`
   - ✅ Response contains token

3. **Generate API Key:**
   - ✅ Request to: `POST /api/keys/generate`
   - ✅ Authorization header present
   - ✅ Response contains `api_key`

---

## ✅ Complete Test Checklist

### Backend Tests
- [ ] Health endpoint responds
- [ ] API docs load
- [ ] Database connected
- [ ] PostgreSQL working on Railway

### Frontend Tests
- [ ] App loads without errors
- [ ] Console shows correct backend URL
- [ ] All tabs visible
- [ ] No JavaScript errors

### Authentication Tests
- [ ] User registration works
- [ ] User login works
- [ ] Logout works
- [ ] Token stored in localStorage
- [ ] Protected routes require auth

### API Key Tests
- [ ] Can generate API key
- [ ] Key shown once during creation
- [ ] Keys listed in viewer (masked)
- [ ] Can delete/revoke key
- [ ] Expired keys detected
- [ ] Validation endpoint works

### Wallet Tests
- [ ] Can create wallet
- [ ] Recovery phrase generated
- [ ] Can sign messages
- [ ] Can verify signatures
- [ ] Password protection works
- [ ] Wrong password rejected

### Integration Tests
- [ ] Frontend → Backend communication
- [ ] Database persistence
- [ ] Token authentication
- [ ] CORS configured correctly
- [ ] Error handling works

---

## 🧪 Quick Test Script

**Test backend with cURL:**

```bash
# 1. Health check
curl https://your-app.up.railway.app/health

# 2. Register user
curl -X POST https://your-app.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'

# 3. Login (get token)
curl -X POST https://your-app.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# 4. Get user info (use token from step 3)
curl https://your-app.up.railway.app/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 Performance Testing

### Check Load Times:

1. **Open DevTools → Network**
2. **Reload page**
3. **Check:**
   - Page load: Should be < 2 seconds
   - API calls: Should be < 1 second
   - First paint: Should be < 1 second

---

## 🎯 Success Criteria

Your app is working correctly if:

✅ All endpoints respond
✅ No console errors
✅ User can register and login
✅ API keys can be generated
✅ Wallets can be created
✅ Database persists data
✅ CORS works in production
✅ Authentication protects routes

---

## 📝 Test Report Template

```
## Test Report - [Date]

### Environment
- Backend: [Railway URL]
- Frontend: [Deployment URL]
- Browser: [Chrome/Firefox/Safari]

### Test Results
- [ ] Backend Health: PASS/FAIL
- [ ] User Registration: PASS/FAIL
- [ ] User Login: PASS/FAIL
- [ ] API Key Generation: PASS/FAIL
- [ ] Wallet Creation: PASS/FAIL
- [ ] Message Signing: PASS/FAIL

### Issues Found
1. [Description]
2. [Description]

### Notes
[Any observations]
```

---

## 🆘 Getting Help

**If tests fail:**

1. Check this guide's troubleshooting section
2. Review Railway logs
3. Check browser console errors
4. Verify all environment variables set
5. Test backend endpoints directly

---

**Happy Testing! 🎉**
