// Modern AI Voice Assistant - Enhanced UI Version
class VoiceAssistant {
    constructor() {
        this.mediaRecorder = null;
        this.audioStream = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.conversationHistory = [];
        
        // DOM Elements
        this.voiceButton = document.getElementById('voice-button');
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = document.getElementById('status-text');
        this.conversationContent = document.getElementById('conversation-content');
        this.aiAudio = document.getElementById('ai-audio');
        this.clearButton = document.getElementById('clear-conversation');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.ensureSessionId();
        this.updateStatus('ready', 'Ready to listen');
    }
    
    setupEventListeners() {
        this.voiceButton.addEventListener('click', () => this.toggleRecording());
        this.clearButton.addEventListener('click', () => this.clearConversation());
        
        // Audio events
        this.aiAudio.addEventListener('ended', () => {
            this.updateStatus('ready', 'Ready to listen');
            // Auto-start recording after AI finishes speaking
            setTimeout(() => {
                if (!this.isRecording) {
                    this.startRecording();
                }
            }, 500);
        });
        
        this.aiAudio.addEventListener('error', (e) => {
            console.error('Audio playback error:', e);
            this.showError('Failed to play audio response', 'warning');
        });
    }
    
    ensureSessionId() {
        const url = new URL(window.location.href);
        let sessionId = url.searchParams.get('session_id');
        if (!sessionId) {
            sessionId = this.generateSessionId();
            url.searchParams.set('session_id', sessionId);
            window.history.replaceState({}, '', url.toString());
        }
        return sessionId;
    }
    
    generateSessionId() {
        return (window.crypto && crypto.randomUUID) 
            ? crypto.randomUUID() 
            : `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    updateStatus(state, message) {
        this.statusIndicator.className = `status-indicator ${state}`;
        this.statusText.textContent = message;
    }
    
    updateVoiceButton(state) {
        if (state === 'recording') {
            this.voiceButton.classList.add('recording');
            this.voiceButton.setAttribute('aria-label', 'Stop recording');
        } else {
            this.voiceButton.classList.remove('recording');
            this.voiceButton.setAttribute('aria-label', 'Start recording');
        }
    }
    
    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }
    
    async startRecording() {
        try {
            // Stop any playing audio
            if (!this.aiAudio.paused) {
                this.aiAudio.pause();
                this.aiAudio.currentTime = 0;
            }
            
            this.updateStatus('recording', 'Listening...');
            this.updateVoiceButton('recording');
            
            // Request microphone access
            this.audioStream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } 
            });
            
            this.mediaRecorder = new MediaRecorder(this.audioStream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            this.audioChunks = [];
            this.isRecording = true;
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                const sessionId = this.ensureSessionId();
                await this.sendToAI(audioBlob, sessionId);
                
                // Cleanup
                this.audioStream.getTracks().forEach(track => track.stop());
                this.isRecording = false;
            };
            
            this.mediaRecorder.start();
            
        } catch (error) {
            console.error('Error starting recording:', error);
            this.handleMicrophoneError(error);
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.updateVoiceButton('ready');
            this.updateStatus('processing', 'Processing...');
        }
    }
    
    async sendToAI(audioBlob, sessionId) {
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.webm');
        
        try {
            this.updateStatus('processing', 'Thinking...');
            
            const response = await fetch(`/agent/chat/${encodeURIComponent(sessionId)}`, {
                method: 'POST',
                body: formData,
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.error) {
                this.handleApiError(data.error, data);
                return;
            }
            
            // Add messages to conversation
            this.addMessage('user', data.transcription);
            this.addMessage('assistant', data.llm_response);
            
            // Play AI response
            if (data.audio_url) {
                this.updateStatus('speaking', 'Speaking...');
                this.aiAudio.src = data.audio_url;
                await this.aiAudio.play();
            } else {
                this.updateStatus('ready', 'Ready to listen');
            }
            
        } catch (error) {
            console.error('AI communication error:', error);
            this.handleNetworkError(error);
        }
    }
    
    addMessage(type, content) {
        // Remove welcome message if it exists
        const welcomeMessage = this.conversationContent.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const labelDiv = document.createElement('div');
        labelDiv.className = 'message-label';
        labelDiv.textContent = type === 'user' ? 'You' : 'AI Assistant';
        
        const contentDiv = document.createElement('div');
        contentDiv.textContent = content;
        
        messageDiv.appendChild(labelDiv);
        messageDiv.appendChild(contentDiv);
        
        this.conversationContent.appendChild(messageDiv);
        
        // Scroll to bottom
        this.conversationContent.scrollTop = this.conversationContent.scrollHeight;
        
        // Store in history
        this.conversationHistory.push({ type, content, timestamp: Date.now() });
    }
    
    showError(message, type = 'error') {
        const errorDiv = document.createElement('div');
        errorDiv.className = `${type}-message`;
        
        const iconSpan = document.createElement('span');
        iconSpan.innerHTML = type === 'error' ? '❌' : '⚠️';
        
        const textSpan = document.createElement('span');
        textSpan.textContent = message;
        
        errorDiv.appendChild(iconSpan);
        errorDiv.appendChild(textSpan);
        
        this.conversationContent.appendChild(errorDiv);
        this.conversationContent.scrollTop = this.conversationContent.scrollHeight;
        
        this.updateStatus('ready', 'Ready to listen');
        this.updateVoiceButton('ready');
    }
    
    handleApiError(errorType, data) {
        const errorMessages = {
            'stt_failure': 'I had trouble understanding your voice. Please try speaking more clearly.',
            'llm_failure': 'I had trouble processing your request. Please try again.',
            'tts_failure': 'I understood you, but had trouble generating speech.',
            'api_keys_missing': 'The AI assistant is not properly configured.',
            'general_failure': 'I\'m experiencing technical difficulties. Please try again later.'
        };
        
        const message = errorMessages[errorType] || 'An unexpected error occurred.';
        const messageType = errorType === 'tts_failure' ? 'warning' : 'error';
        
        // For TTS failure, still show the conversation
        if (errorType === 'tts_failure' && data.transcription && data.llm_response) {
            this.addMessage('user', data.transcription);
            this.addMessage('assistant', data.llm_response + ' (Voice response unavailable)');
        }
        
        this.showError(message, messageType);
    }
    
    handleNetworkError(error) {
        let message = 'Network error occurred.';
        
        if (error.message.includes('Failed to fetch')) {
            message = 'Cannot connect to the server. Please check your internet connection.';
        } else if (error.message.includes('Server error')) {
            message = 'Server is experiencing issues. Please try again later.';
        } else if (error.message.includes('timeout')) {
            message = 'Request timed out. Please try again.';
        }
        
        this.showError(message, 'error');
    }
    
    handleMicrophoneError(error) {
        let message = 'Could not access microphone.';
        
        if (error.name === 'NotAllowedError') {
            message = 'Microphone access denied. Please allow microphone permissions and try again.';
        } else if (error.name === 'NotFoundError') {
            message = 'No microphone found. Please connect a microphone and try again.';
        } else if (error.name === 'NotReadableError') {
            message = 'Microphone is being used by another application.';
        }
        
        this.showError(message, 'error');
        this.updateStatus('ready', 'Ready to listen');
        this.updateVoiceButton('ready');
    }
    
    clearConversation() {
        this.conversationContent.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">👋</div>
                <h4>Welcome!</h4>
                <p>Tap the microphone button below to start a conversation with your AI assistant.</p>
            </div>
        `;
        this.conversationHistory = [];
        
        // Clear server-side session (optional)
        const sessionId = this.ensureSessionId();
        fetch(`/agent/chat/${sessionId}/clear`, { method: 'DELETE' }).catch(() => {
            // Ignore errors - session will be cleared on next interaction
        });
    }
}

// Enhanced feature detection and initialization
document.addEventListener('DOMContentLoaded', () => {
    // Check for required browser features
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        document.body.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh; text-align: center; padding: 2rem;">
                <div>
                    <h2>Browser Not Supported</h2>
                    <p>This application requires a modern browser with microphone support.</p>
                    <p>Please use Chrome, Firefox, Safari, or Edge.</p>
                </div>
            </div>
        `;
        return;
    }
    
    // Check for secure context (HTTPS or localhost)
    if (!window.isSecureContext && location.hostname !== 'localhost') {
        console.warn('Microphone access requires HTTPS in production');
    }
    
    // Initialize the voice assistant
    window.voiceAssistant = new VoiceAssistant();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Space bar to toggle recording
        if (e.code === 'Space' && e.target === document.body) {
            e.preventDefault();
            window.voiceAssistant.toggleRecording();
        }
        
        // Escape to stop recording
        if (e.code === 'Escape' && window.voiceAssistant.isRecording) {
            window.voiceAssistant.stopRecording();
        }
    });
    
    // Add visual feedback for keyboard shortcuts
    const hint = document.createElement('div');
    hint.style.cssText = `
        position: fixed;
        bottom: 1rem;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.75rem;
        z-index: 1000;
        backdrop-filter: blur(8px);
    `;
    hint.textContent = 'Press SPACE to record • ESC to stop';
    document.body.appendChild(hint);
});