/**
 * API Service Layer
 * Handles all communication with the backend server
 */

class ApiService {
    constructor() {
        this.baseUrl = CONFIG.API_BASE_URL;
    }

    /**
     * Get authorization headers
     */
    getAuthHeaders() {
        const token = localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
        return {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        };
    }

    /**
     * Generic API request handler
     */
    async request(endpoint, options = {}) {
        try {
            const url = `${this.baseUrl}${endpoint}`;
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...this.getAuthHeaders(),
                    ...options.headers
                }
            });

            const data = await response.json();

            if (!response.ok) {
                // Handle different error formats
                let errorMessage = 'Request failed';
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    // FastAPI validation errors
                    errorMessage = data.detail.map(err => err.msg).join(', ');
                } else if (data.message) {
                    errorMessage = data.message;
                }
                throw new Error(errorMessage);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ========================================================================
    // Authentication Endpoints
    // ========================================================================

    /**
     * Register a new user
     */
    async register(email, username, password) {
        return await this.request('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify({ email, username, password })
        });
    }

    /**
     * Login user
     */
    async login(email, password) {
        return await this.request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    /**
     * Get current user info
     */
    async getCurrentUser() {
        return await this.request('/api/auth/me', {
            method: 'GET'
        });
    }

    // ========================================================================
    // API Key Management Endpoints
    // ========================================================================

    /**
     * Generate a new API key
     */
    async generateApiKey(name, description, expiryDays) {
        return await this.request('/api/keys/generate', {
            method: 'POST',
            body: JSON.stringify({
                name,
                description,
                expiry_days: expiryDays
            })
        });
    }

    /**
     * List all API keys
     */
    async listApiKeys() {
        return await this.request('/api/keys', {
            method: 'GET'
        });
    }

    /**
     * Get specific API key details
     */
    async getApiKey(keyId) {
        return await this.request(`/api/keys/${keyId}`, {
            method: 'GET'
        });
    }

    /**
     * Revoke an API key
     */
    async revokeApiKey(keyId) {
        return await this.request(`/api/keys/${keyId}`, {
            method: 'DELETE'
        });
    }

    /**
     * Rotate an API key
     */
    async rotateApiKey(keyId) {
        return await this.request(`/api/keys/${keyId}/rotate`, {
            method: 'POST'
        });
    }

    /**
     * Validate an API key
     */
    async validateApiKey(apiKey) {
        return await this.request('/api/keys/validate', {
            method: 'POST',
            headers: {
                'X-API-Key': apiKey
            }
        });
    }

    // ========================================================================
    // Quantum-Proof Crypto Wallet Endpoints
    // ========================================================================

    /**
     * Create a new quantum-proof wallet
     */
    async createWallet(password) {
        return await this.request('/api/wallet/create', {
            method: 'POST',
            body: JSON.stringify({ password })
        });
    }

    /**
     * Get wallet information
     */
    async getWalletInfo() {
        return await this.request('/api/wallet/info', {
            method: 'GET'
        });
    }

    /**
     * Sign a message with wallet
     */
    async signMessage(walletId, password, message) {
        return await this.request('/api/wallet/sign', {
            method: 'POST',
            body: JSON.stringify({
                wallet_id: walletId,
                password: password,
                message: message
            })
        });
    }

    /**
     * Verify a signature
     */
    async verifySignature(walletId, message, signature) {
        return await this.request('/api/wallet/verify', {
            method: 'POST',
            body: JSON.stringify({
                wallet_id: walletId,
                message: message,
                signature: signature
            })
        });
    }

    /**
     * Encrypt message for recipient
     */
    async encryptMessage(recipientWalletId, message, senderWalletId, senderPassword) {
        return await this.request('/api/wallet/encrypt', {
            method: 'POST',
            body: JSON.stringify({
                recipient_wallet_id: recipientWalletId,
                message: message,
                sender_wallet_id: senderWalletId,
                sender_password: senderPassword
            })
        });
    }

    /**
     * Decrypt message
     */
    async decryptMessage(walletId, password, encryptedPackage) {
        return await this.request('/api/wallet/decrypt', {
            method: 'POST',
            body: JSON.stringify({
                wallet_id: walletId,
                password: password,
                encrypted_package: encryptedPackage
            })
        });
    }

    // ========================================================================
    // Health Check
    // ========================================================================

    /**
     * Check if backend is accessible
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    /**
     * Analyze image for deepfake
     */
    async analyzeImageDeepfake(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
        const response = await fetch(`${this.baseUrl}/api/deepfake/analyze-image`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze image');
        }

        return await response.json();
    }

    /**
     * Analyze video for deepfake
     */
    async analyzeVideoDeepfake(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
        const response = await fetch(`${this.baseUrl}/api/deepfake/analyze-video`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze video');
        }

        return await response.json();
    }

    /**
     * Analyze audio for deepfake
     */
    async analyzeAudioDeepfake(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
        const response = await fetch(`${this.baseUrl}/api/deepfake/analyze-audio`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze audio');
        }

        return await response.json();
    }
}

// Create global API service instance
const api = new ApiService();
