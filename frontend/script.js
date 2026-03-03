/* ════════════════════════════════════════════════════════════
   DEEP RESEARCH ENGINE — script.js
   WebSocket-first, fallback to REST POST
   ════════════════════════════════════════════════════════════ */

// ── State ─────────────────────────────────────────────────────
let sessions = [];
let currentDepth = 'detailed';
let ws = null;
let isResearching = false;
let currentLoadingCard = null;

// ── Load persisted config ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const savedUrl = localStorage.getItem('dre_api_url');
    const savedKey = localStorage.getItem('dre_api_key');
    const savedDepth = localStorage.getItem('dre_depth') || 'detailed';
    const savedProvider = localStorage.getItem('dre_provider') || 'groq';

    // Populate Advanced fields only if previously saved
    if (savedUrl) document.getElementById('apiUrl').value = savedUrl;
    // Never pre-fill a stale API key
    if (savedKey) document.getElementById('apiKey').value = savedKey;

    selectDepth(savedDepth);
    document.getElementById('providerSelect').value = savedProvider;

    updateInputPills();
    checkHealth();

    // Textarea auto-resize
    const ta = document.getElementById('queryInput');
    ta.addEventListener('input', () => autoResizeTextarea(ta));

    // Save config on change — works even when Advanced is closed
    document.getElementById('apiUrl').addEventListener('change', saveConfig);
    document.getElementById('apiKey').addEventListener('change', saveConfig);
    document.getElementById('providerSelect').addEventListener('change', () => {
        updateInputPills();
        saveConfig();
    });
});

// ── Config helpers ────────────────────────────────────────────
function saveConfig() {
    localStorage.setItem('dre_api_url', document.getElementById('apiUrl').value.trim());
    localStorage.setItem('dre_api_key', document.getElementById('apiKey').value.trim());
    localStorage.setItem('dre_depth', currentDepth);
    localStorage.setItem('dre_provider', document.getElementById('providerSelect').value);
}

function getApiUrl() {
    // On a deployed server (HF Space, Render, etc.) always use same origin
    if (location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
        return location.origin;
    }

    // Local dev: if user explicitly saved a URL, respect it
    const saved = localStorage.getItem('dre_api_url');
    if (saved && saved.trim()) return saved.trim().replace(/\/$/, '');

    // Otherwise auto-detect: use the same port this page is being served from.
    // This means running on :8001 will call :8001, on :8000 will call :8000, etc.
    return `http://localhost:${location.port || 8000}`;
}

function getApiKey() {
    // Return empty string if nothing set — backend treats no key as open access
    return (document.getElementById('apiKey')?.value || localStorage.getItem('dre_api_key') || '').trim();
}

function getProvider() {
    return document.getElementById('providerSelect').value;
}

// ── Depth Selection ───────────────────────────────────────────
function selectDepth(value) {
    currentDepth = value;
    document.querySelectorAll('.depth-chip').forEach(chip => {
        chip.classList.toggle('active', chip.dataset.value === value);
    });
    updateInputPills();
    saveConfig();
}

function updateInputPills() {
    const provider = getProvider();
    const providerLabels = { groq: 'Groq', openai: 'GPT-4o', anthropic: 'Claude' };
    const depthLabels = { brief: 'Brief', detailed: 'Detailed', comprehensive: 'Deep Dive' };

    document.getElementById('inputProviderPill').textContent = providerLabels[provider] || provider;
    document.getElementById('inputDepthPill').textContent = depthLabels[currentDepth] || currentDepth;
}

// ── Health Check ──────────────────────────────────────────────
async function checkHealth() {
    const dot = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    const mobileDot = document.getElementById('mobileStatus');

    dot.className = 'status-dot checking';
    mobileDot.className = 'mobile-status-dot checking';
    text.textContent = 'Checking...';

    try {
        const resp = await fetch(`${getApiUrl()}/health`, { signal: AbortSignal.timeout(3000) });
        if (resp.ok) {
            dot.className = 'status-dot online';
            mobileDot.className = 'mobile-status-dot online';
            text.textContent = 'Engine Online';
        } else {
            throw new Error('non-200');
        }
    } catch {
        dot.className = 'status-dot offline';
        mobileDot.className = 'mobile-status-dot offline';
        text.textContent = 'Engine Offline';
    }
}

// ── Sidebar / Layout ──────────────────────────────────────────
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
}

// ── Textarea helpers ──────────────────────────────────────────
function autoResizeTextarea(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendQuery();
    }
}

// ── Example Questions ─────────────────────────────────────────
function useExample(question) {
    const input = document.getElementById('queryInput');
    input.value = question;
    input.focus();
    autoResizeTextarea(input);
}

// ── Session Management ────────────────────────────────────────
function startNewSession() {
    // Clear all previous results
    const resultsContainer = document.getElementById('researchResults');
    if (resultsContainer) resultsContainer.innerHTML = '';

    // Show the welcome hero again
    const hero = document.getElementById('welcomeHero');
    if (hero) hero.style.display = '';

    // Clear & focus the input
    const input = document.getElementById('queryInput');
    input.value = '';
    input.style.height = 'auto';
    input.focus();

    // Scroll content area to top
    const mainContent = document.querySelector('.main-content');
    if (mainContent) mainContent.scrollTop = 0;
}

function addSessionToHistory(query, sessionId, depth, provider) {
    const item = { query, sessionId, depth, provider, timestamp: new Date() };
    sessions.unshift(item);
    renderSessionList();
}

function renderSessionList() {
    const list = document.getElementById('sessionList');
    if (sessions.length === 0) {
        list.innerHTML = '<div class="session-empty">No research sessions yet</div>';
        return;
    }

    list.innerHTML = sessions.slice(0, 20).map((s, i) => `
        <div class="session-item ${i === 0 ? 'active' : ''}" onclick="scrollToResult('${s.sessionId}')">
            <div class="session-item-icon">📋</div>
            <div class="session-item-text">
                <div class="session-item-query">${escHtml(s.query)}</div>
                <div class="session-item-meta">${s.depth} · ${formatTime(s.timestamp)}</div>
            </div>
        </div>
    `).join('');
}

function scrollToResult(sessionId) {
    const card = document.getElementById(`result-${sessionId}`);
    if (card) card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Pipeline Step Management ──────────────────────────────────
const PIPELINE_ORDER = ['plan', 'search', 'scrape', 'synthesize', 'done'];

function showPipeline() {
    document.getElementById('pipelineTracker').style.display = 'flex';
    resetPipeline();
}

function hidePipeline() {
    setTimeout(() => {
        document.getElementById('pipelineTracker').style.display = 'none';
    }, 2000);
}

function resetPipeline() {
    PIPELINE_ORDER.forEach(s => {
        const el = document.getElementById(`step-${s}`);
        if (el) el.className = 'pipeline-step';
    });
    document.querySelectorAll('.pipeline-connector').forEach(c => {
        c.className = 'pipeline-connector';
    });
}

function activatePipelineStep(stepName) {
    // Map API status messages to pipeline steps
    const mapping = {
        'starting': 'plan',
        'planning': 'plan',
        'searching': 'search',
        'search': 'search',
        'scraping': 'scrape',
        'scrape': 'scrape',
        'synthesizing': 'synthesize',
        'synthesize': 'synthesize',
        'complete': 'done',
        'done': 'done',
    };

    const step = mapping[stepName?.toLowerCase()] || null;
    if (!step) return;

    const idx = PIPELINE_ORDER.indexOf(step);
    if (idx === -1) return;

    // Mark all prior steps as done
    const connectors = document.querySelectorAll('.pipeline-connector');
    PIPELINE_ORDER.forEach((s, i) => {
        const el = document.getElementById(`step-${s}`);
        if (!el) return;
        if (i < idx) {
            el.className = 'pipeline-step done';
            if (connectors[i]) connectors[i].classList.add('done');
        } else if (i === idx) {
            el.className = 'pipeline-step active';
        } else {
            el.className = 'pipeline-step';
        }
    });
}

function completePipeline() {
    PIPELINE_ORDER.forEach((s, i) => {
        const el = document.getElementById(`step-${s}`);
        if (el) el.className = 'pipeline-step done';
    });
    document.querySelectorAll('.pipeline-connector').forEach(c => {
        c.classList.add('done');
    });
    hidePipeline();
}

// ── Main Query Sender ─────────────────────────────────────────
async function sendQuery() {
    if (isResearching) return;

    const input = document.getElementById('queryInput');
    const query = input.value.trim();
    if (!query) return;

    isResearching = true;
    input.disabled = true;
    document.getElementById('sendBtn').disabled = true;
    input.value = '';
    input.style.height = 'auto';

    // Hide welcome hero if visible
    const hero = document.getElementById('welcomeHero');
    if (hero) hero.style.display = 'none';

    const sessionId = 'sess_' + Date.now();
    const provider = getProvider();
    const depth = currentDepth;

    // Show pipeline
    showPipeline();
    activatePipelineStep('planning');

    // Show loading card
    currentLoadingCard = createLoadingCard(query, sessionId);
    document.getElementById('researchResults').prepend(currentLoadingCard);
    currentLoadingCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        await tryWebSocketResearch(query, sessionId, provider, depth);
    } catch (wsError) {
        console.warn('WebSocket failed, falling back to REST:', wsError);
        try {
            await tryRestResearch(query, sessionId, provider, depth);
        } catch (restError) {
            showErrorCard(sessionId, query, restError.message);
        }
    } finally {
        isResearching = false;
        input.disabled = false;
        document.getElementById('sendBtn').disabled = false;
        input.focus();
    }
}

// ── WebSocket Research ────────────────────────────────────────
function tryWebSocketResearch(query, sessionId, provider, depth) {
    return new Promise((resolve, reject) => {
        const apiUrl = getApiUrl();
        const wsUrl = apiUrl.replace(/^http/, 'ws') + '/ws/research';

        let wsInstance;
        try {
            wsInstance = new WebSocket(wsUrl);
        } catch (e) {
            return reject(e);
        }

        const timeout = setTimeout(() => {
            wsInstance.close();
            reject(new Error('WebSocket connection timeout'));
        }, 5000);

        wsInstance.onopen = () => {
            clearTimeout(timeout);
            wsInstance.send(JSON.stringify({ query, session_id: sessionId, provider, depth }));
        };

        wsInstance.onerror = (e) => {
            clearTimeout(timeout);
            reject(new Error('WebSocket error'));
        };

        let receivedData = null;

        wsInstance.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);

                if (msg.type === 'status') {
                    // Advance pipeline based on status message
                    const txt = (msg.message || '').toLowerCase();
                    if (txt.includes('search')) activatePipelineStep('searching');
                    else if (txt.includes('scrap')) activatePipelineStep('scraping');
                    else if (txt.includes('synth') || txt.includes('report')) activatePipelineStep('synthesizing');
                    updateLoadingCardStatus(currentLoadingCard, msg.message);

                } else if (msg.type === 'chunk') {
                    // Intermediate chunk received
                    activatePipelineStep('synthesizing');

                } else if (msg.type === 'complete') {
                    activatePipelineStep('done');

                } else if (msg.error) {
                    wsInstance.close();
                    reject(new Error(msg.error));
                }

                // If response data embedded in complete message
                if (msg.answer || (msg.data && msg.data.answer)) {
                    receivedData = msg.answer ? msg : msg.data;
                }
            } catch (e) {
                console.warn('WS message parse error:', e);
            }
        };

        wsInstance.onclose = () => {
            if (receivedData) {
                completePipeline();
                renderResult(query, sessionId, provider, depth, receivedData.answer || receivedData, receivedData.sources || []);
                resolve();
            } else {
                // WS closed without data — fall back to REST
                reject(new Error('WebSocket closed without result'));
            }
        };
    });
}

// ── REST Research ──────────────────────────────────────────────
async function tryRestResearch(query, sessionId, provider, depth) {
    activatePipelineStep('searching');

    const headers = { 'Content-Type': 'application/json' };
    const key = getApiKey();
    if (key) headers['X-API-Key'] = key;

    // Simulate pipeline progression with timers
    const t1 = setTimeout(() => activatePipelineStep('scraping'), 2000);
    const t2 = setTimeout(() => activatePipelineStep('synthesizing'), 5000);

    try {
        const resp = await fetch(`${getApiUrl()}/research`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ query, session_id: sessionId, provider, depth, max_results: 5 })
        });

        clearTimeout(t1);
        clearTimeout(t2);

        if (!resp.ok) {
            const errText = await resp.text();
            if (resp.status === 403) throw new Error('Invalid API key — check Configuration.');
            throw new Error(`Server error ${resp.status}: ${errText}`);
        }

        const data = await resp.json();
        completePipeline();
        renderResult(query, sessionId, provider, depth, data.answer, data.sources || []);
    } catch (e) {
        clearTimeout(t1);
        clearTimeout(t2);
        throw e;
    }
}

// ── Render Result Card ─────────────────────────────────────────
function renderResult(query, sessionId, provider, depth, answer, sources) {
    // Remove loading card
    if (currentLoadingCard) {
        currentLoadingCard.remove();
        currentLoadingCard = null;
    }

    const depthLabels = { brief: 'Brief', detailed: 'Detailed', comprehensive: 'Deep Dive' };
    const providerNames = { groq: 'Groq · Llama 3', openai: 'GPT-4o', anthropic: 'Claude 3.5' };

    const renderedMarkdown = renderMarkdown(answer || '_No response generated._');
    const sourcesHtml = buildSourcesHtml(sources);
    const now = new Date();
    const depthLabel = depthLabels[depth] || depth;
    const providerLabel = providerNames[provider] || provider;

    const card = document.createElement('div');
    card.className = 'result-card';
    card.id = `result-${sessionId}`;

    // Store raw data for export (JSON-safe attributes)
    card.dataset.query = query;
    card.dataset.depth = depthLabel;
    card.dataset.provider = providerLabel;
    card.dataset.timestamp = now.toISOString();
    card.dataset.answer = answer || '';
    card.dataset.sources = JSON.stringify(sources || []);

    card.innerHTML = `
        <div class="result-header">
            <div class="result-header-left">
                <div class="result-label">Research Report</div>
                <div class="result-query">${escHtml(query)}</div>
            </div>
            <div class="result-header-right">
                <div class="result-badges">
                    <span class="badge depth">${depthLabel}</span>
                    <span class="badge provider">${providerLabel}</span>
                    <span class="badge time">${formatTime(now)}</span>
                </div>
                <div class="export-actions">
                    <button class="export-btn" onclick="exportToPDF('result-${sessionId}')" title="Export as PDF">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                            <line x1="8" y1="13" x2="16" y2="13"/>
                            <line x1="8" y1="17" x2="16" y2="17"/>
                        </svg>
                        PDF
                    </button>
                    <button class="export-btn secondary" onclick="exportToWord('result-${sessionId}')" title="Export as Word">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 4v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6H6a2 2 0 0 0-2 2z"/>
                            <path d="M14 2v6h6"/>
                            <path d="M9 13l2 4 4-8"/>
                        </svg>
                        Word
                    </button>
                    <button class="export-btn secondary" onclick="exportToMarkdown('result-${sessionId}')" title="Export as Markdown">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="18" height="18" rx="2"/>
                            <path d="M7 15v-6l5 5 5-5v6"/>
                        </svg>
                        Markdown
                    </button>
                    <button class="export-btn secondary" id="copy-btn-${sessionId}" onclick="copyResult('result-${sessionId}', this)" title="Copy to clipboard">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2"/>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                        </svg>
                        Copy
                    </button>
                </div>
            </div>
        </div>
        <div class="result-body">
            <div class="markdown-content">${renderedMarkdown}</div>
        </div>
        ${sourcesHtml}
    `;

    document.getElementById('researchResults').prepend(card);
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Syntax highlight
    card.querySelectorAll('pre code').forEach(block => {
        if (window.hljs) hljs.highlightElement(block);
    });

    addSessionToHistory(query, sessionId, depthLabel, providerLabel);
}

// ── Export: PDF ────────────────────────────────────────────────
function exportToPDF(cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;

    const query = card.dataset.query || 'Research Report';
    const depth = card.dataset.depth || '';
    const provider = card.dataset.provider || '';
    const ts = card.dataset.timestamp ? new Date(card.dataset.timestamp).toLocaleString() : '';
    const mdBody = card.querySelector('.markdown-content')?.innerHTML || '';
    const sourcesEl = card.querySelector('.sources-section');
    const sourcesHtml = sourcesEl ? sourcesEl.outerHTML : '';

    const printHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${escHtml(query)}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', system-ui, sans-serif; font-size: 13px; color: #111; background: #fff; padding: 28px 36px; line-height: 1.7; }
    .report-header { border-bottom: 2px solid #6c47ff; padding-bottom: 14px; margin-bottom: 22px; }
    .report-title { font-size: 11px; text-transform: uppercase; letter-spacing: .1em; color: #6c47ff; font-weight: 700; margin-bottom: 6px; }
    .report-query { font-size: 20px; font-weight: 700; color: #0a0a0a; line-height: 1.3; margin-bottom: 8px; }
    .report-meta { font-size: 11px; color: #666; display: flex; gap: 16px; flex-wrap: wrap; }
    .report-meta span { display: flex; align-items: center; gap: 4px; }
    .report-meta strong { color: #333; }
    h1,h2,h3,h4 { color: #0a0a0a; font-weight: 700; margin: 18px 0 8px; line-height: 1.3; }
    h1 { font-size: 18px; } h2 { font-size: 16px; } h3 { font-size: 14px; } h4 { font-size: 13px; }
    p { margin: 0 0 10px; color: #333; }
    ul,ol { margin: 0 0 10px 20px; color: #333; }
    li { margin-bottom: 4px; }
    code { background: #f4f4f8; border-radius: 4px; padding: 1px 5px; font-family: 'Fira Code', monospace; font-size: 12px; color: #6c47ff; }
    pre { background: #1e1e2e; border-radius: 8px; padding: 14px; overflow-x: auto; margin: 12px 0; }
    pre code { background: none; color: #cdd6f4; font-size: 12px; padding: 0; }
    blockquote { border-left: 3px solid #6c47ff; padding-left: 14px; color: #555; font-style: italic; margin: 12px 0; }
    strong { color: #0a0a0a; }
    a { color: #6c47ff; text-decoration: none; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12px; }
    th { background: #f0eeff; color: #333; font-weight: 600; padding: 8px 10px; text-align: left; border: 1px solid #e0daf0; }
    td { padding: 7px 10px; border: 1px solid #e0daf0; color: #444; }
    tr:nth-child(even) td { background: #fafafe; }
    hr { border: none; border-top: 1px solid #e5e5f0; margin: 18px 0; }
    .sources-section { margin-top: 28px; border-top: 1px solid #e5e5f0; padding-top: 16px; }
    .sources-title { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: #888; font-weight: 600; margin-bottom: 10px; }
    .source-card { display: flex; align-items: flex-start; gap: 10px; padding: 8px 10px; border: 1px solid #e8e8f0; border-radius: 8px; margin-bottom: 6px; text-decoration: none; color: inherit; page-break-inside: avoid; }
    .source-info { flex: 1; }
    .source-title { font-size: 12px; font-weight: 600; color: #0a0a0a; margin-bottom: 2px; }
    .source-url  { font-size: 11px; color: #6c47ff; word-break: break-all; }
    .source-favicon { width: 16px; height: 16px; border-radius: 3px; }
    .source-number { width: 20px; height: 20px; background: #6c47ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #fff; font-weight: 700; flex-shrink: 0; }
    .source-arrow { font-size: 14px; color: #bbb; margin-left: auto; }
    @media print {
      body { padding: 0; }
      pre { page-break-inside: avoid; }
      .source-card { page-break-inside: avoid; }
    }
  </style>
</head>
<body>
  <div class="report-header">
    <div class="report-title">Deep Research Engine — Research Report</div>
    <div class="report-query">${escHtml(query)}</div>
    <div class="report-meta">
      <span><strong>Generated:</strong> ${escHtml(ts)}</span>
      <span><strong>Depth:</strong> ${escHtml(depth)}</span>
      <span><strong>Provider:</strong> ${escHtml(provider)}</span>
    </div>
  </div>
  <div class="report-body">${mdBody}</div>
  ${sourcesHtml}
</body>
</html>`;

    // In body tag, trigger print after fonts load
    const printHtmlFinal = printHtml.replace(
        '<body>',
        '<body onload="setTimeout(()=>window.print(),500)">'
    );

    const slug = query.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);

    // Use Blob URL — avoids document.write() CSP restrictions on HF Space / iframes
    const blob = new Blob([printHtmlFinal], { type: 'text/html;charset=utf-8' });
    const blobUrl = URL.createObjectURL(blob);

    const newTab = window.open(blobUrl, '_blank');
    if (!newTab) {
        // Popup blocked — download as HTML so user can open it and Ctrl+P
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = `research-${slug}-${Date.now()}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
    setTimeout(() => URL.revokeObjectURL(blobUrl), 10000);
}

// ── Export: Word ───────────────────────────────────────────────
function exportToWord(cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;

    const query = card.dataset.query || 'Research Report';
    const depth = card.dataset.depth || '';
    const provider = card.dataset.provider || '';
    const ts = card.dataset.timestamp ? new Date(card.dataset.timestamp).toLocaleString() : '';
    const mdBody = card.querySelector('.markdown-content')?.innerHTML || '';
    const sourcesEl = card.querySelector('.sources-section');
    const sourcesHtml = sourcesEl ? sourcesEl.outerHTML : '';

    // Create a complete HTML document with specific Word properties embedded
    const wordHtml = `<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
      <meta charset="utf-8">
      <title>${escHtml(query)}</title>
      <style>
        body { font-family: 'Arial', sans-serif; padding: 20px; line-height: 1.5; color: #000; }
        h1, h2, h3, h4 { color: #333; margin-top: 15px; margin-bottom: 5px; }
        h1 { font-size: 24px; border-bottom: 2px solid #555; padding-bottom: 5px; }
        h2 { font-size: 20px; }
        p { margin-bottom: 10px; }
        code { font-family: 'Courier New', monospace; background: #f4f4f4; padding: 2px 4px; }
        pre { background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }
        .meta { color: #555; font-size: 12px; margin-bottom: 20px; }
        .sources-section { margin-top: 30px; border-top: 1px solid #ccc; padding-top: 15px; }
        a { color: #0066cc; text-decoration: underline; }
      </style>
    </head>
    <body>
      <h1>${escHtml(query)}</h1>
      <div class="meta">
        <strong>Generated:</strong> ${escHtml(ts)} | 
        <strong>Depth:</strong> ${escHtml(depth)} | 
        <strong>Provider:</strong> ${escHtml(provider)}
      </div>
      <div>${mdBody}</div>
      ${sourcesHtml}
    </body>
    </html>`;

    const slug = query.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);
    const filename = `research-${slug}-${Date.now()}.doc`;

    // Create Blob with application/msword mime type
    const blob = new Blob(['\ufeff', wordHtml], {
        type: 'application/msword;charset=utf-8'
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ── Export: Markdown ───────────────────────────────────────────
function exportToMarkdown(cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;

    const query = card.dataset.query || 'Research Report';
    const depth = card.dataset.depth || '';
    const provider = card.dataset.provider || '';
    const ts = card.dataset.timestamp ? new Date(card.dataset.timestamp).toLocaleString() : '';
    const answer = card.dataset.answer || '';
    let sources = [];
    try { sources = JSON.parse(card.dataset.sources || '[]'); } catch { }

    let md = `# Research Report: ${query}\n\n`;
    md += `> **Generated:** ${ts}  |  **Depth:** ${depth}  |  **Provider:** ${provider}\n\n`;
    md += `---\n\n`;
    md += answer + '\n';

    if (sources.length > 0) {
        md += `\n---\n\n## Sources\n\n`;
        sources.forEach((s, i) => {
            const title = s.title || s.url || `Source ${i + 1}`;
            const url = s.url || '';
            md += `${i + 1}. [${title}](${url})\n`;
        });
    }

    md += `\n---\n_Generated by Deep Research Engine_\n`;

    const slug = query.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);
    const filename = `deep-research-${slug}-${Date.now()}.md`;
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ── Export: Copy to Clipboard ──────────────────────────────────
async function copyResult(cardId, btn) {
    const card = document.getElementById(cardId);
    if (!card) return;
    const text = card.dataset.answer || card.querySelector('.markdown-content')?.innerText || '';
    try {
        await navigator.clipboard.writeText(text);
        const original = btn.innerHTML;
        btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Copied!`;
        btn.style.color = '#22c55e';
        btn.style.borderColor = 'rgba(34,197,94,0.4)';
        setTimeout(() => { btn.innerHTML = original; btn.style.color = ''; btn.style.borderColor = ''; }, 2000);
    } catch {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
    }
}

// ── Loading Card ───────────────────────────────────────────────
function createLoadingCard(query, sessionId) {
    const card = document.createElement('div');
    card.className = 'loading-card';
    card.id = `loading-${sessionId}`;
    card.innerHTML = `
        <div class="loading-header">
            <div class="loading-query">${escHtml(query)}</div>
            <div class="loading-label" id="loading-status-${sessionId}">Initializing research pipeline...</div>
        </div>
        <div class="loading-body">
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
        </div>
    `;
    return card;
}

function updateLoadingCardStatus(card, message) {
    if (!card) return;
    const statusEl = card.querySelector('[id^="loading-status-"]');
    if (statusEl) statusEl.textContent = message;
}

// ── Error Card ─────────────────────────────────────────────────
function showErrorCard(sessionId, query, errorMsg) {
    if (currentLoadingCard) {
        currentLoadingCard.remove();
        currentLoadingCard = null;
    }
    completePipeline();

    const card = document.createElement('div');
    card.className = 'result-card';
    card.id = `result-${sessionId}`;
    card.innerHTML = `
        <div class="result-header">
            <div class="result-header-left">
                <div class="result-label" style="color: var(--red)">Research Failed</div>
                <div class="result-query">${escHtml(query)}</div>
            </div>
            <div class="result-badges">
                <span class="badge" style="background:rgba(239,68,68,0.1);color:var(--red);border-color:rgba(239,68,68,0.2);">Error</span>
            </div>
        </div>
        <div class="result-body">
            <div style="padding: 20px; background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.2); border-radius: 12px;">
                <p style="color: var(--red); font-weight:600; margin-bottom: 8px;">⚠ Connection Error</p>
                <p style="color: var(--text-secondary); font-size: 14px;">${escHtml(errorMsg)}</p>
                <p style="color: var(--text-muted); font-size: 13px; margin-top: 12px;">
                    Make sure the backend is running at <code style="color:var(--accent-2)">${escHtml(getApiUrl())}</code>
                    and the API key is correct.
                </p>
            </div>
        </div>
    `;

    document.getElementById('researchResults').prepend(card);
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Sources HTML ───────────────────────────────────────────────
function buildSourcesHtml(sources) {
    if (!sources || sources.length === 0) return '';

    const items = sources.map((s, i) => {
        const domain = getDomain(s.url || '');
        const favicon = domain ? `https://www.google.com/s2/favicons?domain=${domain}&sz=32` : '';
        const title = s.title || domain || `Source ${i + 1}`;
        const url = s.url || '#';

        return `
            <a class="source-card" href="${escHtml(url)}" target="_blank" rel="noopener noreferrer">
                ${favicon
                ? `<img class="source-favicon" src="${favicon}" alt="" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">`
                : ''
            }
                <div class="source-number" style="${favicon ? 'display:none' : ''}">${i + 1}</div>
                <div class="source-info">
                    <div class="source-title">${escHtml(title)}</div>
                    <div class="source-url">${escHtml(url)}</div>
                </div>
                <span class="source-arrow">↗</span>
            </a>
        `;
    }).join('');

    return `
        <div class="sources-section">
            <div class="sources-title">${sources.length} Verified Source${sources.length !== 1 ? 's' : ''}</div>
            <div class="source-cards">${items}</div>
        </div>
    `;
}

// ── Markdown Renderer ──────────────────────────────────────────
function renderMarkdown(text) {
    if (window.marked) {
        marked.setOptions({
            gfm: true,
            breaks: true,
            highlight: (code, lang) => {
                if (window.hljs && lang && hljs.getLanguage(lang)) {
                    try { return hljs.highlight(code, { language: lang }).value; } catch (e) { }
                }
                return escHtml(code);
            }
        });
        return marked.parse(text);
    }
    // Fallback: basic parsing
    return escHtml(text)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

// ── Utilities ──────────────────────────────────────────────────
function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function getDomain(url) {
    try { return new URL(url).hostname.replace('www.', ''); }
    catch { return null; }
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
