# Frontend Deployment Guide

This guide will help you deploy the frontend web application to various hosting platforms.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

1. ✅ Backend server deployed and accessible
2. ✅ Backend URL for production environment
3. ✅ CORS configured on backend to allow your frontend domain
4. ✅ Tested the application locally

## 🌐 Deployment Options

### Option 1: Netlify (Easiest)

**Step 1: Prepare Files**
```bash
cd frontend
```

**Step 2: Update Config**
Edit `config.js`:
```javascript
API_BASE_URL: 'https://your-backend-url.railway.app'
```

**Step 3: Deploy**
- Go to https://app.netlify.com
- Drag and drop the `frontend` folder
- Your site is live!

**Custom Domain (Optional)**
- Go to Site Settings → Domain Management
- Add your custom domain
- Update DNS records as instructed

---

### Option 2: Vercel

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Update Config**
Edit `config.js` with production backend URL

**Step 3: Deploy**
```bash
cd frontend
vercel --prod
```

**Step 4: Follow Prompts**
- Login to Vercel
- Select project settings
- Deploy!

---

### Option 3: GitHub Pages

**Step 1: Create GitHub Repository**
```bash
cd frontend
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

**Step 2: Update Config**
Edit `config.js` with production backend URL

**Step 3: Enable GitHub Pages**
- Go to repository Settings
- Navigate to Pages section
- Select branch: `main`
- Select folder: `/ (root)` or create a `docs` folder
- Save

**Step 4: Access**
Your site will be available at:
```
https://yourusername.github.io/your-repo/
```

---

### Option 4: AWS S3 + CloudFront

**Step 1: Create S3 Bucket**
```bash
aws s3 mb s3://your-frontend-bucket
```

**Step 2: Configure Bucket for Static Hosting**
```bash
aws s3 website s3://your-frontend-bucket \
  --index-document index.html \
  --error-document index.html
```

**Step 3: Set Bucket Policy**
Create `bucket-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-frontend-bucket/*"
    }
  ]
}
```

Apply policy:
```bash
aws s3api put-bucket-policy \
  --bucket your-frontend-bucket \
  --policy file://bucket-policy.json
```

**Step 4: Update Config**
Edit `config.js` with production backend URL

**Step 5: Upload Files**
```bash
cd frontend
aws s3 sync . s3://your-frontend-bucket \
  --exclude ".git/*" \
  --exclude "*.md"
```

**Step 6: Create CloudFront Distribution (Optional)**
- Go to AWS CloudFront console
- Create distribution
- Set origin to your S3 bucket
- Configure SSL certificate
- Deploy

---

### Option 5: Firebase Hosting

**Step 1: Install Firebase CLI**
```bash
npm install -g firebase-tools
```

**Step 2: Login to Firebase**
```bash
firebase login
```

**Step 3: Initialize Project**
```bash
cd frontend
firebase init hosting
```

Select options:
- Use existing project or create new one
- Public directory: `.` (current directory)
- Single-page app: `Yes`
- GitHub deployment: Optional

**Step 4: Update Config**
Edit `config.js` with production backend URL

**Step 5: Deploy**
```bash
firebase deploy --only hosting
```

---

### Option 6: Cloudflare Pages

**Step 1: Push to Git Repository**
```bash
cd frontend
git init
git add .
git commit -m "Initial commit"
git push origin main
```

**Step 2: Connect to Cloudflare Pages**
- Go to Cloudflare Pages dashboard
- Click "Create a project"
- Connect your Git repository
- Configure build settings:
  - Build command: (leave empty)
  - Build output directory: `/`

**Step 3: Update Config**
Edit `config.js` with production backend URL

**Step 4: Deploy**
- Cloudflare will automatically deploy
- Get your deployment URL

---

## 🔧 Production Configuration

### Update Backend URL

**config.js:**
```javascript
const CONFIG = {
    // Production backend URL
    API_BASE_URL: 'https://your-backend.railway.app',
    
    // Or use environment detection
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:8000'
        : 'https://your-backend.railway.app',
    
    STORAGE_KEYS: {
        TOKEN: 'auth_token',
        USER: 'user_data'
    },
    
    TOKEN_EXPIRY_DAYS: 7,
    DEFAULT_KEY_EXPIRY_DAYS: 90
};
```

### Backend CORS Configuration

Ensure your backend allows requests from your frontend domain.

**MainFile/main.py:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # Local development
        "https://your-frontend.netlify.app",  # Production
        "https://yourdomain.com"           # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔒 Security Considerations

### 1. HTTPS Only
Always serve your frontend over HTTPS in production:
- Most hosting platforms provide free SSL
- Never send tokens over HTTP

### 2. Environment Variables
For sensitive configurations, consider:
```javascript
// Use build-time environment variables
const CONFIG = {
    API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000'
};
```

### 3. Content Security Policy
Add CSP headers (configure in hosting platform):
```
Content-Security-Policy: default-src 'self'; 
  script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; 
  style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
  img-src 'self' data: https:;
  connect-src 'self' https://your-backend.railway.app;
```

### 4. API Key Storage
- Keys are stored in localStorage (acceptable for this use case)
- Never log API keys to console in production
- Clear storage on logout

---

## 🧪 Testing Production Build

Before deploying:

1. **Test with Production Backend**
   ```javascript
   // Temporarily update config.js
   API_BASE_URL: 'https://your-production-backend.com'
   ```
   
2. **Open Local Files**
   - Test authentication flow
   - Generate API keys
   - Test all features
   
3. **Check Browser Console**
   - No errors
   - No CORS issues
   - API calls successful

4. **Test on Different Devices**
   - Desktop browser
   - Mobile browser
   - Different screen sizes

---

## 📊 Monitoring & Analytics

### Add Google Analytics (Optional)

Add to `index.html` before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Error Tracking

Consider adding error tracking like Sentry:
```html
<script src="https://browser.sentry-cdn.com/sentry.min.js"></script>
<script>
  Sentry.init({ dsn: 'YOUR_SENTRY_DSN' });
</script>
```

---

## 🚀 Continuous Deployment

### Netlify Auto-Deploy

Create `netlify.toml`:
```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Push to GitHub, connect to Netlify, and auto-deploy on push!

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Frontend

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        with:
          args: deploy --prod --dir=frontend
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```

---

## 🐛 Common Deployment Issues

### Issue: 404 on Refresh
**Solution:** Configure SPA routing:
- Netlify: Create `_redirects` file:
  ```
  /*    /index.html   200
  ```
- Vercel: Create `vercel.json`:
  ```json
  {
    "rewrites": [{ "source": "/(.*)", "destination": "/" }]
  }
  ```

### Issue: CORS Errors
**Solution:** 
- Update backend CORS settings
- Add your frontend domain to allowed origins
- Check browser network tab for details

### Issue: API Not Connecting
**Solution:**
- Verify backend URL in `config.js`
- Test backend health endpoint
- Check backend is deployed and running

### Issue: Fonts/Icons Not Loading
**Solution:**
- Check CDN links are accessible
- Consider self-hosting Font Awesome
- Check CSP headers

---

## 📝 Post-Deployment Checklist

After deployment:

- [ ] Frontend accessible at deployment URL
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Can generate API keys
- [ ] Can view API keys
- [ ] Can rotate keys
- [ ] Can revoke keys
- [ ] Logout works correctly
- [ ] No console errors
- [ ] Mobile responsive working
- [ ] HTTPS enabled
- [ ] Custom domain configured (if applicable)

---

## 🔄 Updating Deployment

To update your deployed frontend:

1. Make changes locally
2. Test thoroughly
3. Update files
4. Deploy:
   - **Netlify/Vercel:** Push to Git (auto-deploys)
   - **S3:** Run `aws s3 sync`
   - **Manual:** Re-upload files

---

## 📞 Support

If you encounter issues:

1. Check browser console for errors
2. Verify backend is accessible
3. Check CORS configuration
4. Test with different browsers
5. Review hosting platform logs

---

**Your frontend is now ready for the world! 🌍**
