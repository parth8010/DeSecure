# Quick Start Guide 🚀

Get your frontend up and running in 5 minutes!

## Step 1: Start the Backend (2 minutes)

```bash
# Navigate to backend folder
cd MainFile

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the server
python main.py
```

✅ Backend should be running at `http://localhost:8000`

## Step 2: Start the Frontend (2 minutes)

**Open a new terminal window:**

```bash
# Navigate to frontend folder
cd frontend

# Start a simple HTTP server (Python 3)
python -m http.server 3000
```

**Alternative (Node.js):**
```bash
npx http-server -p 3000
```

✅ Frontend should be running at `http://localhost:3000`

## Step 3: Use the Application (1 minute)

1. **Open browser:** `http://localhost:3000`

2. **Register an account:**
   - Click "Register here"
   - Fill in username, email, password
   - Click Register

3. **Generate an API key:**
   - Click "Generate New Key"
   - Enter a name
   - Click "Generate Key"
   - **Copy the key immediately!**

4. **Done!** You now have a working API key management system 🎉

## Testing Your API Key

```bash
# Replace YOUR_API_KEY with the key you generated
curl -X POST http://localhost:8000/api/keys/validate \
  -H "X-API-Key: YOUR_API_KEY"
```

## Troubleshooting

**Problem:** Cannot connect to backend
- Check if backend is running: `http://localhost:8000/health`
- Verify port 8000 is not in use

**Problem:** Frontend won't load
- Check if port 3000 is available
- Try a different port: `python -m http.server 8080`
- Update URL: `http://localhost:8080`

**Problem:** Login fails
- Clear browser cache and localStorage (F12 → Application → Clear storage)
- Check backend console for errors
- Try registering a new account

## Next Steps

- Read `README.md` for full documentation
- Check `DEPLOYMENT.md` for production deployment
- Customize `config.js` for your needs
- Explore `styles.css` to change the theme

---

**Need help?** Check the console (F12) for error messages!
