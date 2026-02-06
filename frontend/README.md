# Cybersecurity Platform - Frontend Web Application

A modern, responsive web application for managing API keys and authentication. This frontend connects to the main backend server and provides a clean UI for user registration, login, and API key management.

## 🚀 Features

- **User Authentication**
  - User registration with email and username
  - Secure login system
  - JWT token-based authentication
  - Automatic session management

- **API Key Management**
  - Generate secure API keys
  - View all your API keys with masked values
  - Set custom expiry periods (1-365 days)
  - Rotate keys for security
  - Revoke/delete keys
  - Track key usage and expiration

- **Modern UI/UX**
  - Responsive design (mobile, tablet, desktop)
  - Clean and intuitive interface
  - Real-time notifications
  - Modal dialogs for key actions
  - Loading states and error handling

## 📁 Project Structure

```
frontend/
├── index.html      # Main HTML file with all UI components
├── styles.css      # Complete styling and responsive design
├── config.js       # Configuration (backend URL, settings)
├── api.js          # API service layer for backend communication
├── app.js          # Main application logic and UI handlers
└── README.md       # This file
```

## 🛠️ Setup Instructions

### Prerequisites

1. **Backend Server Running**
   - Make sure your backend server is running (from MainFile folder)
   - Default backend URL: `http://localhost:8000`
   - See `MainFile/README.md` for backend setup

### Installation

1. **Navigate to the frontend folder**
   ```bash
   cd frontend
   ```

2. **Configure Backend URL**
   - Open `config.js`
   - Update `API_BASE_URL` if your backend is not on localhost:8000
   ```javascript
   API_BASE_URL: 'http://localhost:8000'  // Change this if needed
   ```

3. **Serve the Application**
   
   You can use any static file server. Here are some options:

   **Option A: Python HTTP Server**
   ```bash
   # Python 3
   python -m http.server 3000
   ```

   **Option B: Node.js HTTP Server**
   ```bash
   # Install http-server globally (first time only)
   npm install -g http-server
   
   # Run server
   http-server -p 3000
   ```

   **Option C: VS Code Live Server**
   - Install "Live Server" extension in VS Code
   - Right-click `index.html` → "Open with Live Server"

4. **Access the Application**
   - Open browser: `http://localhost:3000`
   - You should see the login/register page

## 🎯 How to Use

### First Time Setup

1. **Register an Account**
   - Click "Register here" on the login page
   - Fill in username, email, and password (min 8 characters)
   - Click "Register"
   - You'll be automatically logged in

2. **Generate Your First API Key**
   - Click "Generate New Key" button
   - Enter a name (e.g., "Production API Key")
   - Add optional description
   - Set expiry days (default: 90 days)
   - Click "Generate Key"
   - **IMPORTANT:** Copy the key immediately - you won't see it again!

3. **Manage Your Keys**
   - View all your keys in the dashboard
   - Each key shows:
     - Name and description
     - Masked key preview (first 8 and last 4 characters)
     - Creation date
     - Expiry date
     - Last used date
     - Active/Expired status
   - Actions available:
     - **Rotate:** Generate new key, deactivate old one
     - **Revoke:** Permanently disable the key

### Using API Keys

Once you have generated an API key, you can use it to authenticate API requests:

```bash
# Example: Validate API key
curl -X POST http://localhost:8000/api/keys/validate \
  -H "X-API-Key: sk_your_generated_key_here"
```

## 🔧 Configuration Options

### Backend URL Configuration

Edit `config.js` to change the backend server URL:

```javascript
const CONFIG = {
    // Local development
    API_BASE_URL: 'http://localhost:8000',
    
    // Production (update to your deployed backend)
    // API_BASE_URL: 'https://your-backend.railway.app',
    
    // Other settings...
};
```

### Customization

You can customize the application by modifying:

- **styles.css** - Change colors, fonts, layout
- **config.js** - Update settings and defaults
- **app.js** - Modify behavior and features

## 🎨 Technology Stack

- **Pure JavaScript** - No framework dependencies
- **HTML5 & CSS3** - Modern web standards
- **Font Awesome** - Icons
- **Fetch API** - HTTP requests
- **LocalStorage** - Session management

## 🔒 Security Features

1. **JWT Authentication** - Secure token-based auth
2. **HTTPS Ready** - Works with TLS/SSL
3. **CORS Support** - Configurable cross-origin requests
4. **Token Storage** - Secure localStorage management
5. **Password Requirements** - Minimum 8 characters
6. **Key Masking** - API keys are masked in the UI
7. **One-time Key Display** - Full keys shown only once

## 🐛 Troubleshooting

### Cannot Connect to Backend

**Problem:** "Cannot connect to backend server" notification

**Solutions:**
1. Check if backend server is running:
   ```bash
   cd MainFile
   python main.py
   ```
2. Verify backend URL in `config.js` matches your server
3. Check browser console (F12) for CORS errors
4. Ensure no firewall is blocking the connection

### Login/Register Not Working

**Problem:** Authentication fails

**Solutions:**
1. Check backend logs for errors
2. Verify database is accessible
3. Ensure backend is running and healthy: `http://localhost:8000/health`
4. Clear browser cache and localStorage
5. Check network tab (F12) for API response errors

### Keys Not Loading

**Problem:** Dashboard shows loading forever

**Solutions:**
1. Check authentication token is valid
2. Logout and login again
3. Check browser console for errors
4. Verify backend `/api/keys` endpoint is working

### Styling Issues

**Problem:** UI looks broken

**Solutions:**
1. Ensure all CSS files are loaded (check Network tab)
2. Clear browser cache
3. Check Font Awesome CDN is accessible
4. Try different browser

## 📱 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## 🚀 Deployment

### Deploy to Static Hosting

This is a static web application and can be deployed to any static hosting service:

1. **Netlify**
   - Drag and drop the `frontend` folder to Netlify
   - Update `config.js` with production backend URL
   - Deploy!

2. **Vercel**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **GitHub Pages**
   - Push to GitHub repository
   - Enable GitHub Pages in settings
   - Update `config.js` with production backend URL

4. **AWS S3 + CloudFront**
   - Upload files to S3 bucket
   - Configure bucket for static hosting
   - Set up CloudFront distribution

### Important: Update Backend URL

Before deploying, update `config.js`:

```javascript
// Production backend URL
API_BASE_URL: 'https://your-backend-url.com'
```

## 🔗 API Endpoints Used

This frontend connects to these backend endpoints:

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### API Key Management
- `POST /api/keys/generate` - Generate new API key
- `GET /api/keys` - List all user's API keys
- `GET /api/keys/{key_id}` - Get specific key details
- `DELETE /api/keys/{key_id}` - Revoke API key
- `POST /api/keys/{key_id}/rotate` - Rotate API key

### Health Check
- `GET /health` - Backend health check

## 📝 Notes

- API keys are shown in full only once during generation
- Keys expire automatically based on the set expiry period
- Expired keys are marked but not automatically deleted
- Session tokens expire after 7 days (configurable in backend)
- All API requests require valid JWT token (except auth endpoints)

## 🤝 Integration with Backend

This frontend is designed to work seamlessly with the FastAPI backend in the `MainFile` folder. Make sure:

1. Backend CORS is configured to allow your frontend origin
2. Backend is accessible from your frontend deployment
3. Both applications use the same authentication mechanism (JWT)

## 📄 License

Same license as the main project.

## 🆘 Need Help?

- Check backend logs for API errors
- Use browser DevTools (F12) to inspect network requests
- Verify backend health: `http://localhost:8000/health`
- Check console for JavaScript errors
- Ensure all file paths are correct

---

**Happy API Key Management! 🔐**
