# 🧪 Test Your Web Application NOW

## ✅ Your Backend is Live!

**URL:** https://mindful-abundance-production.up.railway.app

**Status:**
- ✅ Health Check: Online
- ✅ Database: Connected (PostgreSQL)
- ✅ API Docs: Available
- ✅ Service: Running

---

## 🚀 Test Locally with Railway Backend

### Option 1: Quick Test (Use Railway Backend)

**Step 1: Enable Railway in Frontend**

Edit `frontend/config.js` line 12:
```javascript
FORCE_RAILWAY: true,  // Change from false to true
```

**Step 2: Start Frontend**
```bash
cd frontend
python -m http.server 3000
```

**Step 3: Open Browser**
```
http://localhost:3000
```

**Step 4: Press F12 - Check Console**

You should see:
```
🔧 Frontend Configuration:
  Environment: Development
  Backend URL: https://mindful-abundance-production.up.railway.app
```

✅ **Perfect! Frontend is connected to Railway backend!**

---

### Option 2: Test Without Editing (Production Mode)

**Deploy frontend to any hosting and it automatically uses Railway!**

Or just open `frontend/index.html` directly in browser (might have CORS issues).

---

## 🧪 Test All Features

### 1. Test User Registration

1. **Click "Sign Up" tab**
2. **Fill in:**
   - Email: `test@example.com`
   - Username: `testuser123`
   - Password: `SecurePass123!`
3. **Click "Register"**

✅ **Expected:**
- Success message appears
- User automatically logged in
- Dashboard shows

### 2. Test User Login

1. **Logout (if logged in)**
2. **Click "Sign In" tab**
3. **Enter credentials:**
   - Email: `test@example.com`
   - Password: `SecurePass123!`
4. **Click "Login"**

✅ **Expected:**
- Login successful
- Redirected to dashboard

### 3. Test API Key Generation

1. **Go to "API Keys" tab**
2. **Fill in:**
   - Name: `My Test Key`
   - Description: `Testing API key generation`
   - Expiry Days: `90`
3. **Click "Generate Key"**

✅ **Expected:**
- API key generated
- Full key shown (COPY IT - shown only once!)
- Key appears in list (masked)

### 4. Test Crypto Wallet

1. **Go to "Crypto Wallet" tab**
2. **Create Wallet:**
   - Enter password: `WalletPass123!`
   - Click "Create Wallet"

✅ **Expected:**
- Recovery phrase shown (SAVE IT!)
- Wallet address displayed
- Success message

3. **Sign Message:**
   - Enter wallet password: `WalletPass123!`
   - Enter message: `Hello Blockchain!`
   - Click "Sign Message"

✅ **Expected:**
- Signature generated
- Displayed in hex format

4. **Verify Signature:**
   - Copy the signature
   - Go to verify section
   - Paste message and signature
   - Click "Verify"

✅ **Expected:**
- Signature verified as valid

---

## 🌐 Test via Browser (Direct Backend Access)

### Test 1: Health Check

Open in browser:
```
https://mindful-abundance-production.up.railway.app/health
```

✅ **Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-02-06T23:39:04.806231"
}
```

### Test 2: API Documentation

Open in browser:
```
https://mindful-abundance-production.up.railway.app/docs
```

✅ **Expected:**
- FastAPI Swagger UI loads
- All endpoints listed
- Can test endpoints directly

### Test 3: Register via API Docs

1. **Open docs (link above)**
2. **Find `POST /api/auth/register`**
3. **Click "Try it out"**
4. **Enter:**
```json
{
  "email": "apitest@example.com",
  "username": "apiuser",
  "password": "password123"
}
```
5. **Click "Execute"**

✅ **Expected Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "apitest@example.com",
    "username": "apiuser"
  },
  "access_token": "eyJ..."
}
```

---

## 🐛 Troubleshooting

### Frontend Can't Connect

**Issue:** "Failed to fetch" error

**Check:**
1. Is `FORCE_RAILWAY: true` in `config.js`?
2. Open console (F12) - what's the Backend URL?
3. Test backend directly: https://mindful-abundance-production.up.railway.app/health

**Fix:**
```javascript
// In frontend/config.js
FORCE_RAILWAY: true,  // Must be true to use Railway
```

### CORS Error

**Issue:** "CORS policy blocked" in console

**Fix:**
Add to Railway environment variables:
```
CORS_ORIGINS=http://localhost:3000
```

Or leave empty to allow all (current default).

### Registration/Login Fails

**Check:**
1. Browser console for exact error
2. Network tab (F12) for request details
3. Backend logs in Railway dashboard

**Common Issues:**
- Email already exists → Use different email
- Password too weak → Use stronger password
- Network error → Check backend health

### Database Errors

**Check Railway:**
1. Is PostgreSQL database added?
2. Is `DATABASE_URL` set? (Railway does this automatically)
3. Check Railway logs for errors

---

## ✅ Success Checklist

After testing, you should be able to:

- [ ] Access backend health endpoint
- [ ] See API documentation
- [ ] Open frontend locally
- [ ] Frontend shows correct backend URL in console
- [ ] Register a new user
- [ ] Login with credentials
- [ ] Generate API keys
- [ ] View API keys (masked)
- [ ] Create crypto wallet
- [ ] Sign messages with wallet
- [ ] Verify signatures

---

## 🎯 Quick Start Commands

**Terminal 1 - Start Frontend:**
```bash
cd frontend
python -m http.server 3000
```

**Browser:**
```
http://localhost:3000
```

**Console (F12):**
Check that backend URL shows Railway URL

**Test:**
- Register → Login → Generate Keys → Create Wallet

---

## 📊 Expected Results

### Console Output (F12):
```
🔧 Frontend Configuration:
  Environment: Development
  Backend URL: https://mindful-abundance-production.up.railway.app
```

### After Registration:
```
✅ User registered successfully!
Welcome, [username]!
```

### After API Key Generation:
```
✅ API Key Generated!
Key: pk_live_xxxxxxxxxxxxxxxxxxxx
⚠️ Copy this key now - you won't see it again!
```

### After Wallet Creation:
```
✅ Wallet Created Successfully!
Recovery Phrase: [12 words]
⚠️ Save this recovery phrase securely!
```

---

## 🎉 You're Ready to Test!

**Your application is fully deployed and ready!**

1. ✅ Backend: Live on Railway
2. ✅ Database: PostgreSQL connected
3. ✅ Frontend: Configured and ready
4. ✅ All features: Available to test

**Start testing now and enjoy your deployed app! 🚀**

---

## 💬 Need Help?

If anything doesn't work:
1. Check browser console (F12) for errors
2. Test backend health endpoint
3. Verify `FORCE_RAILWAY: true` in config.js
4. See TESTING_GUIDE.md for detailed troubleshooting

**Happy Testing! 🎉**
