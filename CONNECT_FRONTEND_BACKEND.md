# 🔗 Connect Frontend to Railway Backend - Step by Step

## Current Status
✅ Frontend files exist in `/frontend/`
✅ Backend is ready to deploy to Railway
✅ Auto-detection system is already in place

---

## 🚀 3-Step Connection Process

### Step 1: Deploy Backend to Railway (If Not Done Yet)

1. **Go to [railway.app](https://railway.app)** and sign in

2. **Deploy Backend:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `parth8010/DeSecure`
   - Railway will automatically deploy

3. **Add PostgreSQL:**
   - Click "New" → "Database" → "Add PostgreSQL"

4. **Set Environment Variables:**
   
   Generate a secret key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   
   In Railway → Your Service → Variables, add:
   ```
   SECRET_KEY=rMJDgEI7wzgRyTxRh1jlLs3zCoD-GKNQOI45lbJ2iJc
   ENVIRONMENT=production
   ```

5. **Get Your Railway Backend URL:**
   - Go to Settings → Networking
   - Copy the domain (e.g., `https://desecure-backend.up.railway.app`)

---

### Step 2: Update Frontend Configuration

**Open `frontend/config.js`** and update line 7:

```javascript
const CONFIG = {
    // Replace this with YOUR Railway backend URL from Step 1
    RAILWAY_URL: 'https://YOUR-APP-NAME.up.railway.app',  // ← UPDATE THIS!
    LOCAL_URL: 'http://localhost:8000',
    
    FORCE_RAILWAY: false,  // Keep false for normal development
    
    // Rest stays the same...
```

**Example:**
```javascript
RAILWAY_URL: 'https://desecure-backend.up.railway.app',
```

---

### Step 3: Test the Connection

#### Option A: Test Locally with Railway Backend

1. **Enable Railway backend temporarily:**
   
   In `frontend/config.js`, change:
   ```javascript
   FORCE_RAILWAY: true,  // Temporarily use Railway even on localhost
   ```

2. **Open the frontend:**
   ```bash
   cd frontend
   # Then open index.html in your browser
   # Or use: python -m http.server 3000
   ```

3. **Test in browser console (F12):**
   ```
   🔧 Frontend Configuration:
     Backend URL: https://your-app.up.railway.app  ← Should show Railway URL
   ```

4. **Try these actions:**
   - Register a new user
   - Login
   - Generate an API key
   - All should work with Railway!

5. **After testing, revert:**
   ```javascript
   FORCE_RAILWAY: false,  // Back to auto-detection
   ```

#### Option B: Deploy Frontend and Test

Deploy your frontend to any hosting service, and it will automatically use Railway backend!

---

## 🌐 Deploy Frontend (Choose One)

### Option 1: GitHub Pages (Free & Easy)

1. **Create `frontend/.nojekyll`** (empty file)

2. **Push to GitHub:**
   ```bash
   git add frontend/
   git commit -m "Update frontend Railway URL"
   git push origin main
   ```

3. **Enable GitHub Pages:**
   - Go to your repo → Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/frontend`
   - Save

4. **Access your app:**
   - `https://parth8010.github.io/DeSecure/`

### Option 2: Netlify (Recommended)

1. **Go to [netlify.com](https://netlify.com)**

2. **Deploy:**
   - "Add new site" → "Import from Git"
   - Select `parth8010/DeSecure`
   - Base directory: `frontend`
   - Click "Deploy"

3. **Your app is live!**
   - Netlify gives you a URL like: `https://desecure.netlify.app`

### Option 3: Railway (All in One)

Deploy frontend to Railway too:

1. **In your Railway project, click "New Service"**
2. **Select "GitHub Repo"** → `parth8010/DeSecure`
3. **Configure:**
   - Root directory: `frontend`
   - Build command: (leave empty)
   - Start command: `python -m http.server $PORT`
4. **Deploy!**

---

## 🔧 Fix CORS (If Needed)

If you get CORS errors after deploying frontend:

**In Railway Dashboard → Backend Service → Variables:**

Add your frontend URL:
```
CORS_ORIGINS=https://your-frontend-domain.com
```

**Examples:**
```
CORS_ORIGINS=https://parth8010.github.io
```
or
```
CORS_ORIGINS=https://desecure.netlify.app
```

or for multiple:
```
CORS_ORIGINS=https://desecure.netlify.app,https://parth8010.github.io
```

**Then redeploy the backend** (Railway will auto-redeploy on variable change)

---

## ✅ Verification Checklist

After connection:

- [ ] Backend deployed to Railway
- [ ] `frontend/config.js` updated with Railway URL
- [ ] Frontend can access backend (test with F12 console)
- [ ] User registration works
- [ ] User login works
- [ ] API key generation works
- [ ] No CORS errors
- [ ] Frontend deployed (optional but recommended)

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" error

**Solution:**
1. Check if backend is running: `https://your-app.railway.app/health`
2. Verify RAILWAY_URL in `config.js` is correct
3. Check Railway logs for backend errors

### Issue: CORS Error

**Solution:**
Add frontend URL to `CORS_ORIGINS` in Railway environment variables (see above)

### Issue: "Invalid token" or "Unauthorized"

**Solution:**
- Clear browser cache and localStorage
- Register a new user
- Make sure frontend and backend are both pointing to the same Railway backend

### Issue: Backend shows "DATABASE_URL not set"

**Solution:**
Make sure you added PostgreSQL database in Railway project

---

## 📊 Current Configuration

**Your setup:**
- ✅ Backend: Ready for Railway (`https://your-app.up.railway.app`)
- ✅ Frontend: In `/frontend/` folder
- ✅ Auto-detection: Already configured
- ⚠️ Action needed: Update `RAILWAY_URL` in `frontend/config.js`

---

## 🎯 Quick Command Reference

**Test backend health:**
```bash
curl https://your-app.railway.app/health
```

**Test backend API docs:**
Open in browser: `https://your-app.railway.app/docs`

**Run frontend locally:**
```bash
cd frontend
python -m http.server 3000
# Then open http://localhost:3000
```

**Check frontend config in browser console:**
```javascript
console.log(CONFIG.API_BASE_URL);
```

---

## 🎉 You're Ready!

1. ✅ Deploy backend to Railway
2. ✅ Copy Railway URL
3. ✅ Update `frontend/config.js` with Railway URL
4. ✅ Test the connection
5. ✅ Deploy frontend (optional)

**Need the exact Railway URL? Check your Railway dashboard after deployment!**
