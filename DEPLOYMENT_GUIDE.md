# Railway Deployment Guide - Simple Steps

## Step 1: Create Railway Account (2 minutes)

1. Go to https://railway.app/
2. Click "Login" → Sign up with GitHub (easiest)
3. Verify your email
4. You get $5 free credit per month!

## Step 2: Install Railway CLI (Optional but helpful)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Or use the web dashboard (no installation needed)
```

## Step 3: Deploy Your Backend

### Option A: Using Railway Web Dashboard (EASIEST) ⭐

1. **Go to Railway Dashboard**
   - Visit https://railway.app/dashboard
   - Click "New Project"

2. **Deploy from GitHub (Recommended)**
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys!

3. **OR Deploy from Local Folder**
   - Click "Deploy from Local"
   - Select the `backend` folder
   - Railway will upload and deploy

4. **Set Environment Variables**
   - Click on your project
   - Go to "Variables" tab
   - Add these variables:
     ```
     SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
     DATABASE_URL=<Railway will auto-generate this>
     ```

5. **Get Your URL**
   - Go to "Settings" tab
   - Click "Generate Domain"
   - Copy your URL: `https://your-app.railway.app`
   - Share this with your Android developer!

### Option B: Using Railway CLI (Alternative)

```bash
# Login to Railway
railway login

# Initialize in your backend folder
cd D:\Hackethon\MainFile\backend
railway init

# Deploy
railway up

# Set environment variables
railway variables set SECRET_KEY=your-super-secret-key-here

# Get your URL
railway domain
```

## Step 4: Verify Deployment

Visit your Railway URL:
- `https://your-app.railway.app/` - Should show {"status": "online"}
- `https://your-app.railway.app/docs` - API documentation
- `https://your-app.railway.app/health` - Health check

## Step 5: Test Your API

Try registering a user:
```bash
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

## Step 6: Share with Android Developer

Give your buddy:
```
API Base URL: https://your-app.railway.app
API Documentation: https://your-app.railway.app/docs
```

## Important Notes

### Database
- Railway uses SQLite by default (file-based)
- For production, upgrade to PostgreSQL:
  1. In Railway dashboard, click "New"
  2. Select "PostgreSQL"
  3. Railway auto-connects it to your app!

### Environment Variables Needed
```
SECRET_KEY=<generate a random string>
PORT=<Railway sets this automatically>
```

### Generate a Secure Secret Key
Run this in Python:
```python
import secrets
print(secrets.token_hex(32))
```

Copy the output and use it as your SECRET_KEY.

## Troubleshooting

### Deployment Failed?
- Check Railway logs in dashboard
- Make sure all files are uploaded
- Verify requirements.txt is present

### Database Issues?
- Railway auto-handles SQLite
- File persists across deploys
- For better reliability, add PostgreSQL database

### App Sleeping?
- Free tier apps may sleep after inactivity
- First request wakes it up (may take 10-20 seconds)
- Keep-alive service or upgrade to prevent sleeping

## Cost

**Free Tier:**
- $5 credit per month
- Good for development and testing
- ~500 hours of runtime

**Paid:**
- $5/month for always-on
- Worth it when app is stable

## Next Steps

1. ✅ Deploy backend
2. ✅ Test API endpoints
3. ✅ Share URL with Android developer
4. ✅ Continue building features
5. ✅ Both work in parallel!

## Auto-Deploy (Bonus)

Connect to GitHub:
1. Push backend code to GitHub
2. Connect repository in Railway
3. Every push auto-deploys!
4. Continuous deployment = winning! 🚀

---

**Your backend is now LIVE and ready for Android app development!** 🎉
