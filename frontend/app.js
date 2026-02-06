/**
 * Main Application Logic
 * Handles UI interactions, state management, and business logic
 */

// ============================================================================
// Application State
// ============================================================================

let currentUser = null;
let apiKeys = [];
let currentWallet = null;

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    await initializeApp();
});

async function initializeApp() {
    showLoading();
    
    // Check backend connection
    const isBackendAvailable = await api.healthCheck();
    if (!isBackendAvailable) {
        showNotification('Cannot connect to backend server. Please check if the server is running.', 'error');
        hideLoading();
        showAuthPage();
        return;
    }

    // Check if user is already logged in
    const token = localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
    if (token) {
        try {
            const user = await api.getCurrentUser();
            currentUser = user;
            await showDashboard();
        } catch (error) {
            // Token expired or invalid
            localStorage.removeItem(CONFIG.STORAGE_KEYS.TOKEN);
            localStorage.removeItem(CONFIG.STORAGE_KEYS.USER);
            showAuthPage();
        }
    } else {
        showAuthPage();
    }
    
    hideLoading();
}

// ============================================================================
// Page Navigation
// ============================================================================

function showLoading() {
    document.getElementById('loading-screen').style.display = 'flex';
    document.getElementById('app-container').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading-screen').style.display = 'none';
    document.getElementById('app-container').style.display = 'block';
}

function showAuthPage() {
    document.getElementById('auth-page').style.display = 'flex';
    document.getElementById('dashboard-page').style.display = 'none';
}

async function showDashboard() {
    document.getElementById('auth-page').style.display = 'none';
    document.getElementById('dashboard-page').style.display = 'block';
    
    // Update user info
    document.getElementById('user-info').textContent = currentUser.username;
    
    // Load API keys
    await loadApiKeys();
    
    // Load wallet
    await loadWallet();
    
    // Initialize deepfake detection
    initDeepfakeDetection();
}

function showLogin() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
    clearAuthError();
}

function showRegister() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
    clearAuthError();
}

// ============================================================================
// Authentication Handlers
// ============================================================================

async function handleLogin(event) {
    event.preventDefault();
    clearAuthError();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await api.login(email, password);
        
        // Save token and user data
        localStorage.setItem(CONFIG.STORAGE_KEYS.TOKEN, response.access_token);
        localStorage.setItem(CONFIG.STORAGE_KEYS.USER, JSON.stringify(response.user));
        
        currentUser = response.user;
        
        showNotification('Login successful!', 'success');
        await showDashboard();
        
    } catch (error) {
        showAuthError(error.message || 'Login failed. Please try again.');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    clearAuthError();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await api.register(email, username, password);
        
        // Save token and user data
        localStorage.setItem(CONFIG.STORAGE_KEYS.TOKEN, response.access_token);
        localStorage.setItem(CONFIG.STORAGE_KEYS.USER, JSON.stringify(response.user));
        
        currentUser = response.user;
        
        showNotification('Registration successful!', 'success');
        await showDashboard();
        
    } catch (error) {
        showAuthError(error.message || 'Registration failed. Please try again.');
    }
}

function handleLogout() {
    localStorage.removeItem(CONFIG.STORAGE_KEYS.TOKEN);
    localStorage.removeItem(CONFIG.STORAGE_KEYS.USER);
    currentUser = null;
    apiKeys = [];
    showNotification('Logged out successfully', 'success');
    showAuthPage();
    showLogin();
}

// ============================================================================
// API Key Management
// ============================================================================

async function loadApiKeys() {
    const container = document.getElementById('api-keys-container');
    container.innerHTML = '<div class="loading-keys"><div class="spinner"></div><p>Loading API keys...</p></div>';
    
    try {
        apiKeys = await api.listApiKeys();
        displayApiKeys();
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Failed to load API keys</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function displayApiKeys() {
    const container = document.getElementById('api-keys-container');
    
    if (apiKeys.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-key"></i>
                <h3>No API Keys Yet</h3>
                <p>Generate your first API key to get started</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = apiKeys.map(key => createApiKeyCard(key)).join('');
}

function createApiKeyCard(key) {
    const isExpired = key.is_expired;
    const statusClass = isExpired ? 'status-expired' : 'status-active';
    const statusText = isExpired ? 'Expired' : 'Active';
    
    const createdDate = new Date(key.created_at).toLocaleDateString();
    const expiresDate = key.expires_at ? new Date(key.expires_at).toLocaleDateString() : 'Never';
    const lastUsed = key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : 'Never';
    
    return `
        <div class="api-key-card">
            <div class="key-card-header">
                <div>
                    <div class="key-card-title">${escapeHtml(key.name)}</div>
                    ${key.description ? `<div class="key-card-description">${escapeHtml(key.description)}</div>` : ''}
                </div>
                <span class="key-status ${statusClass}">${statusText}</span>
            </div>
            
            <div class="key-preview">
                <code>${escapeHtml(key.key_preview)}</code>
                <button class="btn-icon" onclick="copyKeyPreview('${escapeHtml(key.key_preview)}')" title="Copy preview">
                    <i class="fas fa-copy"></i>
                </button>
            </div>
            
            <div class="key-info-grid">
                <div class="key-info-item">
                    <span class="key-info-label">Created</span>
                    <span class="key-info-value">${createdDate}</span>
                </div>
                <div class="key-info-item">
                    <span class="key-info-label">Expires</span>
                    <span class="key-info-value">${expiresDate}</span>
                </div>
                <div class="key-info-item">
                    <span class="key-info-label">Last Used</span>
                    <span class="key-info-value">${lastUsed}</span>
                </div>
                <div class="key-info-item">
                    <span class="key-info-label">Key ID</span>
                    <span class="key-info-value">#${key.key_id}</span>
                </div>
            </div>
            
            <div class="key-card-actions">
                <button class="btn btn-secondary btn-sm" onclick="handleRotateKey(${key.key_id}, '${escapeHtml(key.name)}')" ${isExpired ? 'disabled' : ''}>
                    <i class="fas fa-sync-alt"></i> Rotate
                </button>
                <button class="btn btn-danger btn-sm" onclick="handleRevokeKey(${key.key_id}, '${escapeHtml(key.name)}')">
                    <i class="fas fa-trash"></i> Revoke
                </button>
            </div>
        </div>
    `;
}

// ============================================================================
// Generate API Key
// ============================================================================

function showGenerateKeyModal() {
    document.getElementById('generate-key-modal').classList.add('show');
    document.getElementById('key-name').value = '';
    document.getElementById('key-description').value = '';
    document.getElementById('key-expiry').value = CONFIG.DEFAULT_KEY_EXPIRY_DAYS;
}

function closeGenerateKeyModal() {
    document.getElementById('generate-key-modal').classList.remove('show');
}

async function handleGenerateKey(event) {
    event.preventDefault();
    
    const name = document.getElementById('key-name').value;
    const description = document.getElementById('key-description').value;
    const expiryDays = parseInt(document.getElementById('key-expiry').value);
    
    try {
        const response = await api.generateApiKey(name, description, expiryDays);
        
        closeGenerateKeyModal();
        showGeneratedKey(response);
        
        // Reload keys list
        await loadApiKeys();
        
        showNotification('API key generated successfully!', 'success');
        
    } catch (error) {
        showNotification(error.message || 'Failed to generate API key', 'error');
    }
}

function showGeneratedKey(keyData) {
    document.getElementById('generated-key-value').textContent = keyData.api_key;
    document.getElementById('generated-key-name').textContent = keyData.name;
    document.getElementById('generated-key-expiry').textContent = 
        new Date(keyData.expires_at).toLocaleDateString();
    
    document.getElementById('show-key-modal').classList.add('show');
}

function closeShowKeyModal() {
    document.getElementById('show-key-modal').classList.remove('show');
}

function copyKey() {
    const keyValue = document.getElementById('generated-key-value').textContent;
    navigator.clipboard.writeText(keyValue);
    showNotification('API key copied to clipboard!', 'success');
}

function copyKeyPreview(preview) {
    navigator.clipboard.writeText(preview);
    showNotification('Key preview copied to clipboard!', 'success');
}

// ============================================================================
// Rotate and Revoke API Keys
// ============================================================================

async function handleRotateKey(keyId, keyName) {
    if (!confirm(`Rotate API key "${keyName}"?\n\nThe old key will be deactivated and a new key will be generated.`)) {
        return;
    }
    
    try {
        const response = await api.rotateApiKey(keyId);
        showGeneratedKey(response);
        await loadApiKeys();
        showNotification('API key rotated successfully!', 'success');
    } catch (error) {
        showNotification(error.message || 'Failed to rotate API key', 'error');
    }
}

async function handleRevokeKey(keyId, keyName) {
    if (!confirm(`Revoke API key "${keyName}"?\n\nThis action cannot be undone.`)) {
        return;
    }
    
    try {
        await api.revokeApiKey(keyId);
        await loadApiKeys();
        showNotification('API key revoked successfully!', 'success');
    } catch (error) {
        showNotification(error.message || 'Failed to revoke API key', 'error');
    }
}

// ============================================================================
// UI Helper Functions
// ============================================================================

function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle'
    };
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${icons[type]}"></i>
        <span class="notification-text">${escapeHtml(message)}</span>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function showAuthError(message) {
    const errorDiv = document.getElementById('auth-error');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}

function clearAuthError() {
    const errorDiv = document.getElementById('auth-error');
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// Quantum Wallet Functions
// ============================================================================

async function loadWallet() {
    const container = document.getElementById('wallet-container');
    const actionBtn = document.getElementById('wallet-action-btn');
    
    container.innerHTML = '<div class="loading-keys"><div class="spinner"></div><p>Loading wallet...</p></div>';
    
    try {
        currentWallet = await api.getWalletInfo();
        displayWallet();
        actionBtn.style.display = 'none';
    } catch (error) {
        // No wallet found
        currentWallet = null;
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-wallet"></i>
                <h3>No Wallet Yet</h3>
                <p>Create a quantum-proof crypto wallet to securely store your keys using post-quantum cryptography (Kyber512 + Dilithium2)</p>
                <button onclick="showCreateWalletModal()" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Create Wallet
                </button>
            </div>
        `;
        actionBtn.style.display = 'none';
    }
}

function displayWallet() {
    const container = document.getElementById('wallet-container');
    
    if (!currentWallet) {
        return;
    }
    
    const createdDate = new Date(currentWallet.created_at).toLocaleDateString();
    const lastUnlocked = currentWallet.last_unlocked_at ? 
        new Date(currentWallet.last_unlocked_at).toLocaleDateString() : 'Never';
    
    container.innerHTML = `
        <div class="api-key-card" style="border-left: 4px solid #9333ea;">
            <div class="key-card-header">
                <div>
                    <div class="key-card-title">
                        <i class="fas fa-shield-alt"></i> Quantum Wallet
                    </div>
                    <div class="key-card-description">Post-quantum cryptography secured</div>
                </div>
                <span class="key-status status-active">Active</span>
            </div>
            
            <div class="key-info-grid">
                <div class="key-info-item">
                    <span class="key-info-label">Wallet ID</span>
                    <span class="key-info-value">${escapeHtml(currentWallet.wallet_id)}</span>
                </div>
                <div class="key-info-item">
                    <span class="key-info-label">Algorithm</span>
                    <span class="key-info-value">${escapeHtml(currentWallet.algorithm)}</span>
                </div>
                <div class="key-info-item">
                    <span class="key-info-label">Created</span>
                    <span class="key-info-value">${createdDate}</span>
                </div>
                <div class="key-info-item">
                    <span class="key-info-label">Last Unlocked</span>
                    <span class="key-info-value">${lastUnlocked}</span>
                </div>
            </div>
            
            <div class="key-preview" style="margin-top: 15px;">
                <small style="color: #666;">Kyber Public Key (Encryption)</small>
                <code style="font-size: 11px;">${escapeHtml(currentWallet.kyber_public_key.substring(0, 60))}...</code>
            </div>
            
            <div class="key-preview" style="margin-top: 10px;">
                <small style="color: #666;">Dilithium Public Key (Signatures)</small>
                <code style="font-size: 11px;">${escapeHtml(currentWallet.dilithium_public_key.substring(0, 60))}...</code>
            </div>
            
            <div class="key-card-actions" style="margin-top: 20px;">
                <button class="btn btn-primary btn-sm" onclick="showSignMessageModal()">
                    <i class="fas fa-signature"></i> Sign Message
                </button>
                <button class="btn btn-secondary btn-sm" onclick="showWalletDetails()">
                    <i class="fas fa-info-circle"></i> View Details
                </button>
            </div>
        </div>
    `;
}

function handleWalletAction() {
    if (currentWallet) {
        showWalletDetails();
    } else {
        showCreateWalletModal();
    }
}

// ============================================================================
// Create Wallet Modal
// ============================================================================

function showCreateWalletModal() {
    document.getElementById('create-wallet-modal').classList.add('show');
    document.getElementById('wallet-password').value = '';
    document.getElementById('wallet-password-confirm').value = '';
}

function closeCreateWalletModal() {
    document.getElementById('create-wallet-modal').classList.remove('show');
}

async function handleCreateWallet(event) {
    event.preventDefault();
    
    const password = document.getElementById('wallet-password').value;
    const confirmPassword = document.getElementById('wallet-password-confirm').value;
    
    if (password !== confirmPassword) {
        showNotification('Passwords do not match!', 'error');
        return;
    }
    
    try {
        const response = await api.createWallet(password);
        
        closeCreateWalletModal();
        showRecoveryPhrase(response);
        
        showNotification('Wallet created successfully!', 'success');
        
    } catch (error) {
        showNotification(error.message || 'Failed to create wallet', 'error');
    }
}

// ============================================================================
// Recovery Phrase Modal
// ============================================================================

function showRecoveryPhrase(walletData) {
    const words = walletData.recovery_phrase.split(' ');
    const wordsHtml = words.map((word, index) => 
        `<div class="recovery-word"><span class="word-number">${index + 1}</span><span class="word-text">${word}</span></div>`
    ).join('');
    
    document.getElementById('recovery-phrase-words').innerHTML = wordsHtml;
    document.getElementById('created-wallet-id').textContent = walletData.wallet_id;
    document.getElementById('created-wallet-algorithm').textContent = walletData.algorithm;
    document.getElementById('phrase-saved-checkbox').checked = false;
    document.getElementById('confirm-saved-btn').disabled = true;
    
    // Enable button when checkbox is checked
    document.getElementById('phrase-saved-checkbox').onchange = function() {
        document.getElementById('confirm-saved-btn').disabled = !this.checked;
    };
    
    document.getElementById('recovery-phrase-modal').classList.add('show');
}

async function closeRecoveryPhraseModal() {
    document.getElementById('recovery-phrase-modal').classList.remove('show');
    await loadWallet();
}

// ============================================================================
// Sign Message Modal
// ============================================================================

function showSignMessageModal() {
    if (!currentWallet) {
        showNotification('No wallet found. Please create a wallet first.', 'error');
        return;
    }
    document.getElementById('sign-message-modal').classList.add('show');
    document.getElementById('sign-message-text').value = '';
    document.getElementById('sign-wallet-password').value = '';
}

function closeSignMessageModal() {
    document.getElementById('sign-message-modal').classList.remove('show');
}

async function handleSignMessage(event) {
    event.preventDefault();
    
    const message = document.getElementById('sign-message-text').value;
    const password = document.getElementById('sign-wallet-password').value;
    
    try {
        const response = await api.signMessage(currentWallet.wallet_id, password, message);
        
        closeSignMessageModal();
        showSignature(response.signature);
        
        await loadWallet(); // Refresh to update last unlocked time
        
        showNotification('Message signed successfully!', 'success');
        
    } catch (error) {
        showNotification(error.message || 'Failed to sign message', 'error');
    }
}

// ============================================================================
// Show Signature Modal
// ============================================================================

function showSignature(signature) {
    document.getElementById('signature-value').textContent = signature;
    document.getElementById('show-signature-modal').classList.add('show');
}

function closeShowSignatureModal() {
    document.getElementById('show-signature-modal').classList.remove('show');
}

function copySignature() {
    const signature = document.getElementById('signature-value').textContent;
    navigator.clipboard.writeText(signature);
    showNotification('Signature copied to clipboard!', 'success');
}

// ============================================================================
// Wallet Details
// ============================================================================

function showWalletDetails() {
    if (!currentWallet) return;
    
    const details = `
Wallet ID: ${currentWallet.wallet_id}
Algorithm: ${currentWallet.algorithm}
Created: ${new Date(currentWallet.created_at).toLocaleString()}
Last Unlocked: ${currentWallet.last_unlocked_at ? new Date(currentWallet.last_unlocked_at).toLocaleString() : 'Never'}

Kyber Public Key (Encryption):
${currentWallet.kyber_public_key}

Dilithium Public Key (Signatures):
${currentWallet.dilithium_public_key}
    `;
    
    alert(details);
}

// ============================================================================
// Close modals on outside click
// ============================================================================

document.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
});

// ============================================================================
// DEEPFAKE DETECTION FUNCTIONS
// ============================================================================

let currentUploadType = 'image';

// Initialize deepfake detection when DOM is ready
function initDeepfakeDetection() {
    // Get elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('deepfake-file-input');
    const imageBtn = document.getElementById('image-btn');
    const videoBtn = document.getElementById('video-btn');
    const audioBtn = document.getElementById('audio-btn');
    
    if (!uploadArea || !fileInput) {
        console.error('Deepfake elements not found');
        return;
    }
    
    // Click upload area to trigger file input
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Handle file selection
    fileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        
        await handleDeepfakeUpload(file);
        fileInput.value = ''; // Reset
    });
    
    // Handle type selector buttons
    [imageBtn, videoBtn, audioBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                const type = btn.getAttribute('data-type');
                selectUploadType(type);
            });
        }
    });
    
    console.log('Deepfake detection initialized');
}

function selectUploadType(type) {
    currentUploadType = type;
    
    // Update button states
    const buttons = document.querySelectorAll('.upload-type-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    document.getElementById(`${type}-btn`).classList.add('active');
    
    // Update file input and hint
    const fileInput = document.getElementById('deepfake-file-input');
    const hint = document.getElementById('upload-hint');
    
    if (type === 'image') {
        fileInput.accept = 'image/*';
        hint.textContent = 'Supported: JPG, PNG, JPEG';
    } else if (type === 'video') {
        fileInput.accept = 'video/*';
        hint.textContent = 'Supported: MP4, AVI, MOV';
    } else if (type === 'audio') {
        fileInput.accept = 'audio/*';
        hint.textContent = 'Supported: WAV, MP3';
    }
    
    // Hide previous results
    const resultDiv = document.getElementById('deepfake-result');
    if (resultDiv) {
        resultDiv.style.display = 'none';
    }
}

async function handleDeepfakeUpload(file) {
    const uploadArea = document.getElementById('upload-area');
    const originalHTML = uploadArea.innerHTML;
    
    // Show loading state
    uploadArea.innerHTML = `
        <div class="spinner"></div>
        <p>Analyzing ${currentUploadType}...</p>
        <small>This may take a few moments</small>
    `;
    
    try {
        let result;
        
        // Call appropriate API based on type
        if (currentUploadType === 'image') {
            result = await api.analyzeImageDeepfake(file);
        } else if (currentUploadType === 'video') {
            result = await api.analyzeVideoDeepfake(file);
        } else if (currentUploadType === 'audio') {
            result = await api.analyzeAudioDeepfake(file);
        }
        
        // Display results
        displayDeepfakeResult(result);
        showNotification('Analysis complete!', 'success');
        
    } catch (error) {
        console.error('Deepfake analysis error:', error);
        showNotification('Failed to analyze file: ' + error.message, 'error');
    } finally {
        // Reset upload area
        uploadArea.innerHTML = originalHTML;
    }
}

function displayDeepfakeResult(result) {
    const resultDiv = document.getElementById('deepfake-result');
    const verdictDiv = document.getElementById('result-verdict');
    const confidenceSpan = document.getElementById('result-confidence');
    const detailsDiv = document.getElementById('result-details');
    
    // Show result
    resultDiv.style.display = 'block';
    
    // Display verdict
    const verdict = result.verdict;
    verdictDiv.textContent = verdict;
    verdictDiv.className = 'result-verdict ' + verdict.toLowerCase();
    
    // Display confidence
    const confidencePercent = (result.confidence * 100).toFixed(1);
    confidenceSpan.textContent = `${confidencePercent}%`;
    
    // Display details if available
    if (result.details) {
        let detailsHTML = '<h4>Analysis Details:</h4><ul>';
        for (const [key, value] of Object.entries(result.details)) {
            const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            let formattedValue;
            if (typeof value === 'number') {
                formattedValue = value < 1 ? (value * 100).toFixed(1) + '%' : value.toFixed(2);
            } else {
                formattedValue = value;
            }
            detailsHTML += `<li><strong>${formattedKey}:</strong> ${formattedValue}</li>`;
        }
        detailsHTML += '</ul>';
        detailsDiv.innerHTML = detailsHTML;
    } else {
        detailsDiv.innerHTML = '';
    }
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
