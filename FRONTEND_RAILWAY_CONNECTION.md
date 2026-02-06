# Connect Frontend to Railway Backend

## 🎯 Quick Setup Guide

Your frontend is already configured to automatically connect to Railway! Here's how to set it up:

---

## Step 1: Get Your Railway Backend URL

After deploying your backend to Railway:

1. Go to your Railway project dashboard
2. Click on your backend service
3. Go to "Settings" → "Networking"
4. Copy the public URL (looks like: `https://your-app-name.up.railway.app`)

**Example:** `https://desecure-backend.up.railway.app`

---

## Step 2: Update Frontend Configuration

Open `frontend/config.js` and update the `RAILWAY_URL`:

```javascript
const CONFIG = {
    // Replace with YOUR Railway backend URL
    RAILWAY_URL: 'https://your-app-name.up.railway.app',
    LOCAL_URL: 'http://localhost:8000',
    
    // Keep this as false for normal development
    FORCE_RAILWAY: false,
    
    // ... rest of config
};
```

**That's it!** The frontend will automatically:
- Use Railway backend when deployed to production
- Use local backend (`localhost:8000`) when developing locally

---

## Step 3: Test the Connection

### Option A: Test Locally (Pointing to Railway)

1. **Temporarily enable Railway in local dev:**
   ```javascript
   FORCE_RAILWAY: true,  // Change this in config.js
   ```

2. **Open the frontend:**
   ```bash
   cd frontend
   open index.html  # or just double-click index.html
   ```

3. **Test Registration/Login:**
   - Open browser console (F12)
   - You should see: `Backend URL: https://your-app-name.up.railway.app`
   - Try registering a new user
   - Check if it works!

### Option B: Test in Production

1. **Deploy frontend to a hosting service:**
   - GitHub Pages
   - Netlify
   - Vercel
   - Railway (separate service)

2. **It will automatically use Railway backend** (no changes needed!)

---

## 🔧 How Auto-Detection Works

Your `config.js` automatically detects the environment:

```javascript
get API_BASE_URL() {
    // If FORCE_RAILWAY is enabled → use Railway
    if (this.FORCE_RAILWAY) {
        return this.RAILWAY_URL;
    }
    
    // If on localhost → use local backend
    if (window.location.hostname === 'localhost' || 
        window.location.hostname === '127.0.0.1') {
        return this.LOCAL_URL;
    }
    
    // Otherwise (production) → use Railway
    return this.RAILWAY_URL;
}
```

---

## 🚀 Deploy Frontend to Railway (Optional)

You can also deploy your frontend to Railway:

### 1. Create a Simple Server

Create `frontend/server.js`:

```javascript
const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(__dirname));

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend running on port ${PORT}`);
});
```

### 2. Add package.json

Create `frontend/package.json`:

```json
{
  "name": "desecure-frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

### 3. Deploy to Railway

1. Go to Railway → "New Project" → "Deploy from GitHub"
2. Select your repo
3. Railway will auto-detect Node.js
4. Your frontend will be live!

---

## 🌐 Alternative: Deploy to Netlify (Easiest)

Netlify is perfect for static sites like yours:

### 1. Create `frontend/netlify.toml`:

```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 2. Deploy:

1. Go to [netlify.com](https://netlify.com)
2. "Add new site" → "Import from Git"
3. Select your GitHub repo
4. Set base directory: `frontend`
5. Deploy!

**Done!** Your frontend will automatically connect to Railway backend.

---

## ✅ Quick Test Checklist

After updating `RAILWAY_URL`, test these:

- [ ] Open frontend in browser
- [ ] Check console: Should show Railway URL
- [ ] Try user registration
- [ ] Try user login
- [ ] Generate an API key
- [ ] Create a wallet
- [ ] All should work with Railway backend!

---

## 🐛 Troubleshooting

### "CORS Error"

**Solution:** Add your frontend URL to backend CORS settings

In Railway dashboard → Backend service → Variables:
```
CORS_ORIGINS=https://your-frontend-url.netlify.app
```

### "Failed to fetch" or "Network Error"

**Check:**
1. Is Railway backend running? Visit: `https://your-app.railway.app/health`
2. Is the URL correct in `config.js`?
3. Check browser console for exact error
4. Verify Railway backend has no errors in logs

### Backend URL not updating

**Solution:**
1. Hard refresh browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear browser cache
3. Check `config.js` - make sure RAILWAY_URL is correct

---

## 📊 Connection Status

You can verify connection in browser console (F12):

```
🔧 Frontend Configuration:
  Environment: Production
  Backend URL: https://your-app.up.railway.app
```

---

## 🎯 Summary

**Local Development:**
- Frontend: Open `index.html` locally
- Backend: `http://localhost:8000`
- Config: Auto-detects localhost

**Production:**
- Frontend: Deploy to Netlify/Vercel/Railway
- Backend: `https://your-app.up.railway.app`
- Config: Auto-uses Railway URL

**Update these files:**
1. `frontend/config.js` → Update `RAILWAY_URL`
2. Railway Variables → Add `CORS_ORIGINS` if needed

That's it! Your frontend and backend are now connected! 🎉
