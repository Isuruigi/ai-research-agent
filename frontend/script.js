// API Configuration
const API_URL = 'http://localhost:8000';
const API_KEY = 'your-secret-api-key-change-this'; // Set this in production
let sessionId = null;
let chatHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    autoResizeTextarea();
    loadChatHistory();
});

// Auto-resize textarea
function autoResizeTextarea() {
    const textarea = document.getElementById('userInput');
    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
        updateSendButton();
    });
}

// Update send button state
function updateSendButton() {
    const input = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    if (input.value.trim()) {
        sendBtn.classList.add('active');
    } else {
        sendBtn.classList.remove('active');
    }
}

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Set query from prompt chips
function setQuery(query) {
    document.getElementById('userInput').value = query;
    updateSendButton();
    sendMessage();
}

// Send message
async function sendMessage() {
    const input = document.getElementById('userInput');
    const query = input.value.trim();

    if (!query) return;

    // Validate query length (API requires 10-500 characters)
    if (query.length < 10) {
        addMessage('assistant', '⚠️ Please enter a research question with at least 10 characters.');
        return;
    }

    if (query.length > 500) {
        addMessage('assistant', '⚠️ Query is too long. Please keep it under 500 characters.');
        return;
    }

    // Hide welcome screen
    const welcomeScreen = document.getElementById('welcomeScreen');
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }

    // Clear input
    input.value = '';
    input.style.height = 'auto';
    updateSendButton();

    // Add user message
    addMessage('user', query);

    // Add research status indicators
    const statusId = addResearchStatus();

    // Scroll to bottom
    scrollToBottom();

    try {
        // Update status: Searching web
        updateResearchStatus(statusId, '🌐 Searching the web...');
        await sleep(1000);

        // Prepare request body
        const requestBody = {
            query: query,
            max_results: 5
        };

        // Only include session_id if it exists
        if (sessionId) {
            requestBody.session_id = sessionId;
        }

        // Call API
        const startTime = Date.now();
        const response = await fetch(`${API_URL}/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY
            },
            body: JSON.stringify(requestBody)
        });

        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMsg = errorData.detail || `HTTP ${response.status}`;
            throw new Error(errorMsg);
        }

        // Update status: Extracting content
        updateResearchStatus(statusId, '📄 Extracting content from sources...');
        await sleep(500);

        const data = await response.json();

        // Update status: Synthesizing
        updateResearchStatus(statusId, `📚 Synthesizing research report... (${elapsed}s)`);
        await sleep(500);

        // Remove status indicator
        removeResearchStatus(statusId);

        // Store session ID
        sessionId = data.session_id;

        // Add assistant response
        addMessage('assistant', data.response, data.sources);

        // Save to history
        saveChatHistory(query, data.response);

        // Scroll to bottom
        scrollToBottom();

    } catch (error) {
        removeResearchStatus(statusId);
        const errorMessage = error.message.includes('Failed to fetch')
            ? '❌ Cannot connect to server. Make sure it\'s running on http://localhost:8000'
            : `❌ Error: ${error.message}`;
        addMessage('assistant', errorMessage);
        scrollToBottom();
    }
}

// Sleep helper
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Add research status
function addResearchStatus() {
    const messagesContainer = document.getElementById('messages');
    const statusDiv = document.createElement('div');
    const statusId = 'status-' + Date.now();
    statusDiv.id = statusId;
    statusDiv.className = 'message message-assistant';
    statusDiv.innerHTML = `
        <div class="message-avatar avatar-assistant">🔬</div>
        <div class="message-content">
            <div class="research-status" id="${statusId}-text">
                🔍 Starting research...
            </div>
        </div>
    `;
    messagesContainer.appendChild(statusDiv);
    scrollToBottom();
    return statusId;
}

// Update research status
function updateResearchStatus(statusId, text) {
    const statusElement = document.getElementById(statusId + '-text');
    if (statusElement) {
        statusElement.textContent = text;
    }
    scrollToBottom();
}

// Remove research status
function removeResearchStatus(statusId) {
    const statusDiv = document.getElementById(statusId);
    if (statusDiv) {
        statusDiv.remove();
    }
}

// Add message to chat
function addMessage(role, content, sources = []) {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;

    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${escapeHtml(content)}</div>
            </div>
            <div class="message-avatar avatar-user">U</div>
        `;
    } else {
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = `
                <div class="sources-container">
                    <div class="sources-title">📚 ${sources.length} Sources</div>
                    ${sources.map((source, idx) => `
                        <a href="${source}" target="_blank" class="source-link">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                                <polyline points="15 3 21 3 21 9"></polyline>
                                <line x1="10" y1="14" x2="21" y2="3"></line>
                            </svg>
                            ${getDomain(source)}
                        </a>
                    `).join('')}
                </div>
            `;
        }

        messageDiv.innerHTML = `
            <div class="message-avatar avatar-assistant">🔬</div>
            <div class="message-content">
                <div class="message-text">${formatMarkdown(content)}</div>
                ${sourcesHtml}
            </div>
        `;
    }

    messagesContainer.appendChild(messageDiv);
}

// Scroll to bottom
function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
}

// Format markdown (simple)
function formatMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Get domain from URL
function getDomain(url) {
    try {
        const domain = new URL(url).hostname;
        return domain.replace('www.', '');
    } catch {
        return url;
    }
}

// Start new chat
function startNewChat() {
    sessionId = null;
    document.getElementById('messages').innerHTML = '';
    document.getElementById('welcomeScreen').style.display = 'flex';
    document.getElementById('userInput').value = '';
    updateSendButton();
}

// Save chat history
function saveChatHistory(query, response) {
    const chat = {
        query: query.substring(0, 50) + (query.length > 50 ? '...' : ''),
        timestamp: new Date().toISOString()
    };

    chatHistory.unshift(chat);
    if (chatHistory.length > 10) {
        chatHistory = chatHistory.slice(0, 10);
    }

    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    renderChatHistory();
}

// Load chat history
function loadChatHistory() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        chatHistory = JSON.parse(saved);
        renderChatHistory();
    }
}

// Render chat history
function renderChatHistory() {
    const container = document.getElementById('recentChats');
    if (!container) return;

    if (chatHistory.length === 0) {
        container.innerHTML = '<div style="color: var(--text-muted); font-size: 13px;">No recent research</div>';
        return;
    }

    container.innerHTML = chatHistory.map(chat => `
        <div class="chat-history-item" style="
            padding: 8px 12px;
            margin-bottom: 4px;
            border-radius: 6px;
            font-size: 13px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
        " onmouseover="this.style.background='var(--bg-tertiary)'" onmouseout="this.style.background='transparent'">
            ${chat.query}
        </div>
    `).join('');
}
