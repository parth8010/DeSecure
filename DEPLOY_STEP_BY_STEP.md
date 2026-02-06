# 🚀 Deploy to Railway - Follow Along

## Current Status
✅ Code is pushed to GitHub: https://github.com/parth8010/DeSecure
✅ All fixes applied
✅ Ready to deploy

---

## 📋 Step-by-Step Deployment

### Step 1: Go to Railway

**Open this link in your browser:**
```
https://railway.app/new
```

**Sign in with GitHub** (if not already signed in)

---

### Step 2: Create New Project

1. Click **"Deploy from GitHub repo"**
2. You'll see your repositories
3. Select: **`parth8010/DeSecure`**
4. Click **"Deploy Now"**

Railway will start deploying immediately!

---

### Step 3: Wait for Initial Deploy (~2-3 minutes)

You'll see:
- Build logs scrolling
- "Building..." status
- Then "Success" ✅

**Wait for this to complete before moving to next step!**

---

### Step 4: Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway creates database automatically

✅ `DATABASE_URL` is automatically set!

---

### Step 5: Set Environment Variables

1. Click on your **backend service** (not the database)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

**Add Variable 1:**
```
Name: SECRET_KEY
Value: rMJDgEI7wzgRyTxRh1jlLs3zCoD-GKNQOI45lbJ2iJc
```

**Add Variable 2:**
```
Name: ENVIRONMENT
Value: production
```

4. The service will **automatically redeploy** with these variables

---

### Step 6: Get Your Railway URL

1. Click on your backend service
2. Go to **"Settings"** tab
3. Scroll to **"Networking"** section
4. Look for **"Public Networking"**
5. You'll see a domain like:
   ```
   https://web-production-XXXX.up.railway.app
   ```
   or Railway will generate one for you

6. **Copy this URL!** You'll need it next.

---

### Step 7: Test Backend

**Open in browser:**
```
https://YOUR-RAILWAY-URL.up.railway.app/health
```

✅ **Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "..."
}
```

**Also test API docs:**
```
https://YOUR-RAILWAY-URL.up.railway.app/docs
```

✅ You should see FastAPI Swagger UI!

---

### Step 8: Update Frontend Config

1. **Open `frontend/config.js`** in your code editor

2. **Update line 7:**
   ```javascript
   RAILWAY_URL: 'https://YOUR-RAILWAY-URL.up.railway.app',
   ```

3. **Save the file**

---

### Step 9: Test Frontend Locally with Railway Backend

1. **Temporarily enable Railway:**
   
   In `frontend/config.js`:
   ```javascript
   FORCE_RAILWAY: true,  // Change to true
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   python -m http.server 3000
   ```

3. **Open browser:**
   ```
   http://localhost:3000
   ```

4. **Press F12** - Console should show:
   ```
   Backend URL: https://YOUR-RAILWAY-URL.up.railway.app
   ```

5. **Test Registration:**
   - Click "Sign Up"
   - Enter: email, username, password
   - Click "Register"
   - ✅ Should work with Railway backend!

---

### Step 10: Push Updated Config to GitHub (Optional)

```bash
git add frontend/config.js
git commit -m "Update frontend with Railway backend URL"
git push origin main
```

---

## ✅ Deployment Complete!

Your backend is now live on Railway! 🎉

**Your URLs:**
- Backend API: `https://YOUR-RAILWAY-URL.up.railway.app`
- API Docs: `https://YOUR-RAILWAY-URL.up.railway.app/docs`
- Health Check: `https://YOUR-RAILWAY-URL.up.railway.app/health`

**Frontend:**
- Running locally on: `http://localhost:3000`
- Connected to Railway backend ✅

---

## 🧪 Test Checklist

After deployment, verify:

- [ ] Backend health endpoint responds
- [ ] API docs load
- [ ] Frontend connects to Railway
- [ ] Can register a user
- [ ] Can login
- [ ] Can generate API keys
- [ ] Can create wallet

---

## 🐛 Troubleshooting

### Build Failed in Railway

**Check:**
- Railway logs (click on deployment to see logs)
- Ensure all files are in GitHub
- Check `requirements.txt` is correct

### Database Connection Error

**Check:**
- PostgreSQL database is added
- Railway should auto-set `DATABASE_URL`
- Check variables tab to confirm

### Frontend Can't Connect

**Check:**
- Railway backend is running (check health endpoint)
- RAILWAY_URL in config.js is correct
- FORCE_RAILWAY is set to true for testing

### CORS Error

**Solution:**
If you deploy frontend later, add to Railway variables:
```
CORS_ORIGINS=https://your-frontend-domain.com
```

---

## 📞 Ready to Deploy?

**Start here:** https://railway.app/new

**Follow steps 1-9 above!**

---

**After deployment, tell me your Railway URL and I'll help you test!**
