# 🚂 Railway Backend Integration Guide

Your backend is deployed on Railway! This guide will help you connect your frontend to your Railway backend.

## 🔧 Step 1: Get Your Railway Backend URL

1. Go to your Railway dashboard: https://railway.app
2. Select your backend project
3. Click on your service
4. Find the **Public Domain** (should look like: `https://your-app-name.up.railway.app`)
5. Copy this URL

## ⚙️ Step 2: Update Frontend Configuration

**Open `frontend/config.js` and update line 9:**

```javascript
RAILWAY_URL: 'https://your-backend-url.railway.app', // Replace with your actual Railway URL
```

**Example:**
```javascript
RAILWAY_URL: 'https://cybersecurity-platform-production.up.railway.app',
```

### Smart Environment Detection

The frontend now **automatically detects** which backend to use:

- 🏠 **Local Development** (`http://localhost:3000`) → Uses `http://localhost:8000`
- 🌐 **Production** (any other domain) → Uses Railway URL

No need to manually switch configurations!

## 🔒 Step 3: Configure CORS on Railway Backend

Your Railway backend needs to allow requests from your frontend domain.

### Option A: Allow All Origins (Development/Testing)

In `MainFile/main.py`, the CORS is already configured to allow all origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This is **already set up** and should work fine!

### Option B: Restrict to Specific Domains (Production - More Secure)

For production, you may want to restrict CORS to specific domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                          # Local development
        "https://your-frontend.netlify.app",              # Netlify deployment
        "https://your-frontend.vercel.app",               # Vercel deployment
        "https://yourdomain.com",                         # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Note:** Only update this if you deploy the frontend and need stricter security.

## ✅ Step 4: Test the Connection

### Test Locally First

1. **Update config.js** with your Railway URL
2. **Start the frontend:**
   ```bash
   cd frontend
   python -m http.server 3000
   ```
3. **Open browser:** http://localhost:3000
4. **Check console** (F12) - You should see:
   ```
   🔧 Frontend Configuration:
     Environment: Development
     Backend URL: http://localhost:8000
   ```

### Test with Railway Backend

To test the Railway connection locally:

**Temporary Test:** Update `config.js`:
```javascript
get API_BASE_URL() {
    // Force Railway URL for testing
    return this.RAILWAY_URL;
}
```

Then:
1. Open http://localhost:3000
2. Console should show: `Backend URL: https://your-backend-url.railway.app`
3. Try to register/login - it should connect to Railway!
4. **Revert the change** after testing

## 🚀 Step 5: Deploy Frontend

Now that your backend is on Railway, you can deploy your frontend to:

### Option A: Netlify (Recommended - Free & Easy)

1. Go to https://netlify.com
2. Drag and drop the `frontend` folder
3. Your frontend is live! (e.g., `https://your-frontend.netlify.app`)
4. It will automatically use Railway backend (no config change needed!)

### Option B: Vercel

```bash
cd frontend
npx vercel --prod
```

### Option C: GitHub Pages

```bash
cd frontend
git init
git add .
git commit -m "Initial commit"
git push origin main
# Enable GitHub Pages in repository settings
```

### Option D: Railway (Host Both on Railway!)

You can also deploy the frontend to Railway:

1. Create a new Railway service
2. Connect your repository
3. Deploy the `frontend` folder
4. Both frontend and backend on Railway!

## 🔍 Troubleshooting

### Issue: "Cannot connect to backend server"

**Check 1: Railway Backend Running**
```bash
curl https://your-backend-url.railway.app/health
```

Should return:
```json
{"status":"healthy","database":"connected","timestamp":"..."}
```

**Check 2: CORS Configured**
- Open browser console (F12)
- Look for CORS errors
- Ensure Railway backend has CORS enabled (it should already)

**Check 3: Railway URL Correct**
- Verify the URL in `config.js` matches your Railway domain
- Railway URLs usually end with `.railway.app` or `.up.railway.app`

### Issue: CORS Error in Production

If you get CORS errors when deployed:

1. Check your frontend domain
2. Add it to Railway backend CORS origins (if you restricted it)
3. Redeploy Railway backend

### Issue: 404 on Railway Backend

Make sure your Railway backend is:
- ✅ Deployed and running
- ✅ Port is set correctly (Railway sets `PORT` env variable)
- ✅ Domain is public (not private)

## 📝 Configuration Examples

### Development Setup
```javascript
// config.js
RAILWAY_URL: 'https://my-backend.railway.app',
LOCAL_URL: 'http://localhost:8000',

// Automatic detection works!
// localhost:3000 → uses localhost:8000
```

### Production Setup (Frontend Deployed)
```javascript
// config.js - NO CHANGES NEEDED!
// When frontend is on Netlify/Vercel:
// Automatically uses Railway URL
```

### Testing Railway Locally
```javascript
// Temporarily force Railway for testing
get API_BASE_URL() {
    return this.RAILWAY_URL; // Always use Railway
}
```

## 🌐 Full Deployment Architecture

```
┌─────────────────────────────────────────────┐
│  Frontend (Choose One)                      │
│  - Netlify (recommended)                    │
│  - Vercel                                   │
│  - GitHub Pages                             │
│  - Railway                                  │
└───────────────┬─────────────────────────────┘
                │ HTTPS Requests
                ↓
┌───────────────────────────────────────────┐
│  Backend on Railway                       │
│  https://your-backend.railway.app         │
│  - FastAPI server                         │
│  - PostgreSQL/SQLite database             │
│  - JWT authentication                     │
│  - API key management                     │
└───────────────────────────────────────────┘
```

## ✅ Quick Checklist

Before going live:

- [ ] Railway backend is deployed and accessible
- [ ] Got Railway backend URL (e.g., `https://xxx.railway.app`)
- [ ] Updated `RAILWAY_URL` in `frontend/config.js`
- [ ] Tested locally with Railway backend
- [ ] CORS is configured (allow_origins=["*"] works for testing)
- [ ] Frontend deployed to hosting service
- [ ] Tested registration, login, and API key generation
- [ ] All features working correctly

## 🎉 You're All Set!

Your frontend will now automatically:
- 🏠 Use `localhost:8000` when developing locally
- 🚂 Use Railway backend when deployed

No manual switching needed!

## 📞 Need Help?

**Check Railway Logs:**
```bash
railway logs
# or in Railway dashboard → Deployments → View Logs
```

**Check Frontend Console:**
- Open browser (F12)
- Look for error messages
- Check the "Backend URL" log message

**Test Railway Backend Directly:**
```bash
# Health check
curl https://your-backend-url.railway.app/health

# Test registration
curl -X POST https://your-backend-url.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass123"}'
```

---

**Happy Deploying! 🚀**
