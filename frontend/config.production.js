/**
 * Production Configuration Template
 * Copy this file to config.js for production deployment
 * OR just update RAILWAY_URL in config.js
 */

const CONFIG = {
    // YOUR RAILWAY BACKEND URL - UPDATE THIS!
    RAILWAY_URL: 'https://your-app-name.up.railway.app',
    LOCAL_URL: 'http://localhost:8000',
    
    // Automatically detect environment
    get API_BASE_URL() {
        if (window.location.hostname === 'localhost' || 
            window.location.hostname === '127.0.0.1') {
            return this.LOCAL_URL;
        }
        return this.RAILWAY_URL;
    },
    
    STORAGE_KEYS: {
        TOKEN: 'auth_token',
        USER: 'user_data'
    },
    
    TOKEN_EXPIRY_DAYS: 7,
    DEFAULT_KEY_EXPIRY_DAYS: 90
};

function getApiUrl(endpoint) {
    return `${CONFIG.API_BASE_URL}${endpoint}`;
}

console.log('🔧 Frontend Configuration:');
console.log('  Environment:', window.location.hostname === 'localhost' ? 'Development' : 'Production');
console.log('  Backend URL:', CONFIG.API_BASE_URL);
