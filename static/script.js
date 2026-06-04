// AI Chat Application - Frontend Logic

// DOM Elements
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const messagesContainer = document.getElementById('messagesContainer');
const welcomeScreen = document.getElementById('welcomeScreen');
const loadingIndicator = document.getElementById('loadingIndicator');
const clearBtn = document.getElementById('clearBtn');
const sendIcon = document.getElementById('sendIcon');
const loadingSpinner = document.getElementById('loadingSpinner');
const messagesEnd = document.getElementById('messagesEnd');

// State
let messages = [];

// Event Listeners
chatForm.addEventListener('submit', handleSendMessage);
messageInput.addEventListener('keypress', handleKeyPress);
clearBtn.addEventListener('click', clearChat);
messageInput.addEventListener('input', adjustTextAreaHeight);

// Handle message submission
async function handleSendMessage(e) {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to UI
    addMessage(message, 'user');
    messageInput.value = '';
    adjustTextAreaHeight();

    // Show loading indicator
    showLoading();

    try {
        // Send to backend
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                model: 'qwen'
            })
        });

        if (!response.ok) {
            const error = await response.json();
            addMessage(`Error: ${error.error}`, 'assistant');
            hideLoading();
            return;
        }

        const data = await response.json();

        // Add AI response to UI
        const responseText = `
Summary: ${data.summary}

Sentiment: ${data.sentiment}/100

Response: ${data.response}

[Response time: ${data.duration}s]
        `.trim();

        addMessage(responseText, 'assistant');
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'assistant');
    } finally {
        hideLoading();
        focusInput();
    }
}

// Handle Enter key
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
}

// Add message to chat
function addMessage(content, role) {
    // Hide welcome screen on first message
    if (messages.length === 0) {
        welcomeScreen.style.display = 'none';
        clearBtn.style.display = 'flex';
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;

    const metadata = document.createElement('div');
    metadata.className = 'message-metadata';
    metadata.textContent = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });

    messageDiv.appendChild(bubble);
    messageDiv.appendChild(metadata);
    messagesContainer.appendChild(messageDiv);

    // Store message
    messages.push({ content, role, timestamp: new Date() });

    // Scroll to bottom
    scrollToBottom();
}

// Show loading indicator
function showLoading() {
    welcomeScreen.style.display = 'none';
    loadingIndicator.style.display = 'flex';
    sendButton.disabled = true;
    sendIcon.style.display = 'none';
    loadingSpinner.style.display = 'flex';
}

// Hide loading indicator
function hideLoading() {
    loadingIndicator.style.display = 'none';
    sendButton.disabled = false;
    sendIcon.style.display = 'block';
    loadingSpinner.style.display = 'none';
}

// Clear chat
function clearChat() {
    messagesContainer.innerHTML = '';
    welcomeScreen.style.display = 'flex';
    clearBtn.style.display = 'none';
    messages = [];
    messageInput.value = '';
    adjustTextAreaHeight();
    focusInput();
}

// Scroll to bottom
function scrollToBottom() {
    messagesEnd.scrollIntoView({ behavior: 'smooth' });
}

// Adjust textarea height
function adjustTextAreaHeight() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// Focus input
function focusInput() {
    messageInput.focus();
}

// Initialize
messageInput.focus();