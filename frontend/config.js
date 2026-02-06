/**
 * Configuration File
 * Automatically detects environment and uses appropriate backend URL
 */

const CONFIG = {
    // Backend API URLs
    RAILWAY_URL: 'https://mindful-abundance-production.up.railway.app',
    LOCAL_URL: 'http://localhost:8000',
    
    // Force Railway backend even in local development
    // Set to false if you want to use local backend
    FORCE_RAILWAY: true,
    
    // Automatically detect environment
    get API_BASE_URL() {
        // Force Railway URL if enabled
        if (this.FORCE_RAILWAY) {
            return this.RAILWAY_URL;
        }
        
        // Use local backend when on localhost
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.LOCAL_URL;
        }
        return this.RAILWAY_URL;
    },
    
    // Local storage keys
    STORAGE_KEYS: {
        TOKEN: 'auth_token',
        USER: 'user_data'
    },
    
    // App settings
    TOKEN_EXPIRY_DAYS: 7,
    DEFAULT_KEY_EXPIRY_DAYS: 90
};

// Utility function to get full API endpoint
function getApiUrl(endpoint) {
    return `${CONFIG.API_BASE_URL}${endpoint}`;
}

// Log current configuration (helpful for debugging)
console.log('🔧 Frontend Configuration:');
console.log('  Environment:', window.location.hostname === 'localhost' ? 'Development' : 'Production');
console.log('  Backend URL:', CONFIG.API_BASE_URL);
