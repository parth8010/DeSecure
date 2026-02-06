# 🚀 Quick Deploy to Railway - 5 Minutes

## Step 1: Generate Secret Key (30 seconds)

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
**Copy the output** - you'll need it in Step 4.

---

## Step 2: Push to GitHub (1 minute)

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

---

## Step 3: Deploy on Railway (2 minutes)

1. Go to **[railway.app](https://railway.app)**
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Click **"Add PostgreSQL"** from the dashboard

---

## Step 4: Set Environment Variables (1 minute)

Go to your service → **"Variables"** → Add these:

```
SECRET_KEY=<paste-the-key-from-step-1>
ENVIRONMENT=production
```

**Optional** (for production CORS):
```
CORS_ORIGINS=https://your-frontend-domain.com
```

---

## Step 5: Done! ✅

Your API is now live at: `https://your-app.railway.app`

**Test it:**
- Visit: `https://your-app.railway.app/docs`
- You should see the API documentation

---

## 🔍 Quick Troubleshooting

**Build Failed?**
- Check Railway logs tab
- Ensure all files are committed to GitHub

**Can't connect to database?**
- Make sure PostgreSQL is added to your Railway project
- Railway auto-sets `DATABASE_URL`

**CORS errors?**
- Add your frontend URL to `CORS_ORIGINS` variable
- Format: `https://domain1.com,https://domain2.com`

---

## 📚 Full Documentation

- **Complete Guide**: See `RAILWAY_DEPLOYMENT.md`
- **All Fixes**: See `FIXES_SUMMARY.md`

---

**That's it! Your API is live on Railway! 🎉**
