# Railway Deployment Guide

This guide will help you deploy the Cybersecurity Platform API to Railway.app.

## ✅ What's Already Fixed

All compatibility issues for Railway have been resolved:

1. ✅ **Database**: Automatically uses PostgreSQL on Railway, SQLite locally
2. ✅ **Port Binding**: Reads from `PORT` environment variable
3. ✅ **Dependencies**: All required packages in `requirements.txt`
4. ✅ **CORS**: Configurable via environment variables
5. ✅ **Build Config**: `nixpacks.toml` properly configured

## 🚀 Quick Deploy to Railway

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Create a new project on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your repository

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Set Environment Variables**
   - Go to your service → "Variables"
   - Add these required variables:
     ```
     SECRET_KEY=<generate-a-strong-random-key-here>
     ENVIRONMENT=production
     CORS_ORIGINS=https://your-frontend-domain.com
     ```

5. **Deploy!**
   - Railway will automatically detect `nixpacks.toml`
   - Your app will be deployed and accessible via a Railway URL

### Option 2: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and Deploy**
   ```bash
   railway init
   railway up
   ```

4. **Add PostgreSQL**
   ```bash
   railway add
   # Select PostgreSQL
   ```

5. **Set Environment Variables**
   ```bash
   railway variables set SECRET_KEY=<your-secret-key>
   railway variables set ENVIRONMENT=production
   ```

## 🔧 Environment Variables for Railway

Set these in your Railway project settings:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Auto-set | PostgreSQL connection (auto-provided by Railway) | `postgresql://...` |
| `PORT` | Auto-set | Port to bind to (auto-provided by Railway) | `8000` |
| `SECRET_KEY` | **YES** | JWT secret key - MUST BE CHANGED! | `your-secret-key-here` |
| `ENVIRONMENT` | **YES** | Set to `production` for Railway | `production` |
| `CORS_ORIGINS` | Optional | Comma-separated allowed origins | `https://app.example.com` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Optional | Token expiration time | `10080` (7 days) |
| `API_KEY_DEFAULT_EXPIRY_DAYS` | Optional | API key expiration | `90` |

## 🔑 Generate a Secure SECRET_KEY

Run this command to generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and set it as your `SECRET_KEY` environment variable in Railway.

## 🌐 Custom Domain (Optional)

1. Go to your Railway service settings
2. Click "Settings" → "Networking"
3. Add your custom domain
4. Update your DNS records as instructed
5. Update `CORS_ORIGINS` to include your domain

## 📊 Check Deployment Status

After deployment, verify your API is working:

1. **Health Check**
   ```bash
   curl https://your-app.railway.app/health
   ```

2. **API Documentation**
   Visit: `https://your-app.railway.app/docs`

## 🐛 Troubleshooting

### Build Fails

- Check Railway build logs
- Ensure `nixpacks.toml` is in root directory
- Verify all dependencies are in `requirements.txt`

### Database Connection Error

- Ensure PostgreSQL is added to your project
- Check that `DATABASE_URL` is set (Railway does this automatically)
- Verify the app can connect: Check logs for connection errors

### CORS Errors

- Add your frontend URL to `CORS_ORIGINS` environment variable
- Format: `https://your-domain.com,https://app.your-domain.com`
- Leave empty to allow all origins (not recommended for production)

### App Won't Start

- Check logs in Railway dashboard
- Verify `PORT` environment variable is being read
- Ensure all required environment variables are set

## 📦 What Gets Deployed

- ✅ FastAPI backend with all endpoints
- ✅ PostgreSQL database (automatic migrations on startup)
- ✅ API documentation at `/docs`
- ✅ Health check endpoints at `/` and `/health`

## 🔒 Security Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure `CORS_ORIGINS` to only allow your frontend
- [ ] Enable HTTPS (Railway provides this automatically)
- [ ] Review and limit API rate limits if needed

## 🎯 Next Steps

1. Deploy your frontend (can also be on Railway)
2. Update frontend API URL to point to Railway backend
3. Test all endpoints from your frontend
4. Set up monitoring and alerts

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)

## 🆘 Need Help?

- Railway Community: [discord.gg/railway](https://discord.gg/railway)
- FastAPI Docs: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- Check Railway logs for detailed error messages
