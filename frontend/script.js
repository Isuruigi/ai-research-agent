// Configuration
const API_URL = 'http://localhost:8000';  // Use local server for testing
const API_KEY = 'your-secret-api-key-change-this'; // Match what you set in HF Spaces secrets

let currentSessionId = null;

// Auto-resize textarea
document.getElementById('userInput').addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Use example question
function useExample(question) {
    const input = document.getElementById('userInput');
    input.value = question;
    input.focus();

    // Auto-resize textarea
    input.style.height = 'auto';
    input.style.height = (input.scrollHeight) + 'px';
}

// Start new chat
function startNewChat() {
    currentSessionId = null;
    document.getElementById('messages').innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
            </div>
            <h2>How can I help with your research today?</h2>
            <p>Ask me to research any topic and I'll provide comprehensive, cited information.</p>
            
            <div class="example-questions">
                <div class="example-card" onclick="useExample('What are the latest breakthroughs in quantum computing?')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
                    </svg>
                    <span>Latest breakthroughs in quantum computing</span>
                </div>
                <div class="example-card" onclick="useExample('Explain the impact of artificial intelligence on healthcare')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                    </svg>
                    <span>Impact of AI on healthcare</span>
                </div>
                <div class="example-card" onclick="useExample('What is climate change and how does it affect global ecosystems?')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                    </svg>
                    <span>Climate change and global ecosystems</span>
                </div>
                <div class="example-card" onclick="useExample('How does blockchain technology work and what are its applications?')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                        <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                    </svg>
                    <span>Blockchain technology and applications</span>
                </div>
            </div>
        </div>
    `;
    document.getElementById('userInput').value = '';
}

// Send message
async function sendMessage() {
    const input = document.getElementById('userInput');
    const query = input.value.trim();

    if (!query) return;

    // Disable input
    input.disabled = true;
    document.getElementById('sendBtn').disabled = true;

    // Remove welcome message if present
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    // Add user message
    addMessage('user', query);
    input.value = '';
    input.style.height = 'auto';

    // Add thinking indicator
    const thinkingDiv = addThinkingIndicator();

    try {
        // Generate session ID if first message
        if (!currentSessionId) {
            currentSessionId = 'session_' + Date.now();
        }

        const response = await fetch(`${API_URL}/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY
            },
            body: JSON.stringify({
                query: query,
                session_id: currentSessionId,
                max_results: 5,
                provider: document.getElementById('providerSelect').value
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Remove thinking indicator
        thinkingDiv.remove();

        // Add AI response
        addMessage('ai', data.answer || 'I received your question but encountered an issue generating a response.');

    } catch (error) {
        console.error('Error:', error);
        thinkingDiv.remove();
        addMessage('ai', 'Sorry, I encountered an error. Please try again.');
    } finally {
        // Re-enable input
        input.disabled = false;
        document.getElementById('sendBtn').disabled = false;
        input.focus();
    }
}

// Parse simple markdown
function parseMarkdown(text) {
    // Convert **bold** to <strong>bold</strong>
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Convert *italic* to <em>italic</em>
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Convert line breaks
    text = text.replace(/\n/g, '<br>');

    return text;
}

// Add message to chat
function addMessage(role, content) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const header = role === 'user' ? 'You' : 'AI Research Agent';

    // Parse markdown for AI messages
    const formattedContent = role === 'ai' ? parseMarkdown(content) : content;

    messageDiv.innerHTML = `
        <div class="message-header">${header}</div>
        <div class="message-content">${formattedContent}</div>
    `;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    return messageDiv;
}

// Add thinking indicator
function addThinkingIndicator() {
    const messagesDiv = document.getElementById('messages');
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message ai';
    thinkingDiv.innerHTML = `
        <div class="message-header">AI Research Agent</div>
        <div class="thinking">
            <div class="thinking-dot"></div>
            <div class="thinking-dot"></div>
            <div class="thinking-dot"></div>
        </div>
    `;
    messagesDiv.appendChild(thinkingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return thinkingDiv;
}

// Focus input on load
window.addEventListener('load', () => {
    document.getElementById('userInput').focus();
});
