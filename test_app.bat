@echo off
echo.
echo ========================================
echo   Starting Web Application for Testing
echo ========================================
echo.
echo Backend: Railway (Live)
echo URL: https://mindful-abundance-production.up.railway.app
echo.
echo Starting frontend server...
echo Open browser to: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.
cd frontend
python -m http.server 3000
