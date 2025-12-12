const fileListEl = document.getElementById('file-list');
const pdfUploadInput = document.getElementById('pdf-upload');
const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const resetBtn = document.getElementById('reset-btn');

// --- File Management ---

async function loadFiles() {
    try {
        const res = await fetch('/files');
        const data = await res.json();
        renderFiles(data.files);
    } catch (err) {
        console.error("Failed to load files:", err);
    }
}

function renderFiles(files) {
    fileListEl.innerHTML = '';
    if (files.length === 0) {
        fileListEl.innerHTML = '<li style="color: grey; padding: 0.5rem; font-style: italic;">No files uploaded.</li>';
        return;
    }
    files.forEach(file => {
        const li = document.createElement('li');
        li.className = 'file-item';
        // Check if file is string (old format) or object (new format)
        const name = file.name || file;
        const size = file.size ? `<span class="file-size">${file.size}</span>` : '';
        const link = file.url ? ` <a href="${file.url}" target="_blank" class="file-link" title="Open PDF">↗</a>` : '';

        li.innerHTML = `
            <div class="file-info">
                <span class="file-icon">📄</span> 
                <span class="file-name">${name}</span>
            </div>
            <div class="file-meta">
                ${size}
                ${link}
            </div>
        `;
        fileListEl.appendChild(li);
    });
}

resetBtn.addEventListener('click', async () => {
    if (!confirm("Are you sure you want to delete all files?")) return;

    // Optimistic UI update
    fileListEl.innerHTML = '<li style="color: grey; padding: 0.5rem; font-style: italic;">Deleting...</li>';

    try {
        const res = await fetch('/reset', { method: 'DELETE' });
        if (res.ok) {
            addSystemMessage("✅ System reset successfully.");
            // Force empty state immediately
            renderFiles([]);
        } else {
            alert("Failed to reset system.");
            loadFiles(); // Revert on failure
        }
    } catch (err) {
        console.error("Reset failed", err);
        loadFiles(); // Revert on error
    }
});

pdfUploadInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    // Optimistic UI update or loading state could go here
    const statusIdx = addSystemMessage(`Uploading ${file.name}...`);

    try {
        const res = await fetch('/ingest', {
            method: 'POST',
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            updateSystemMessage(statusIdx, `✅ Uploaded ${file.name} successfully!`);
            loadFiles(); // Refresh list

            // Show suggestions if available
            if (data.suggestions && data.suggestions.length > 0) {
                const suggestionsDiv = document.createElement('div');
                suggestionsDiv.className = 'suggestions-container';
                suggestionsDiv.innerHTML = '<p>💡 Suggested Questions:</p>';

                data.suggestions.forEach(q => {
                    const btn = document.createElement('button');
                    btn.className = 'suggestion-chip';
                    btn.innerText = q.replace(/^[0-9-.\s]+/, ''); // Remove leading numbers if any
                    btn.onclick = () => {
                        userInput.value = btn.innerText;
                        handleChat();
                    };
                    suggestionsDiv.appendChild(btn);
                });

                addMessageElement(suggestionsDiv);
            }

        } else {
            const errData = await res.json();
            updateSystemMessage(statusIdx, `❌ Upload failed: ${errData.detail}`);
        }
    } catch (err) {
        updateSystemMessage(statusIdx, `❌ Upload error: ${err.message}`);
    }

    // Reset input
    pdfUploadInput.value = '';
});

// --- Chat Logic ---

function addMessage(text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerText = text; // Secure text insertion

    msgDiv.appendChild(bubble);
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return msgDiv;
}

function addSystemMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ai';
    msgDiv.innerHTML = `<div class="bubble" style="font-style: italic; opacity: 0.8;">${text}</div>`;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return msgDiv;
}

function addMessageElement(element) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ai';
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.appendChild(element);
    msgDiv.appendChild(bubble);
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return msgDiv;
}

function updateSystemMessage(element, text) {
    element.querySelector('.bubble').innerText = text;
}

function addLoadingMessage() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ai';
    msgDiv.innerHTML = `
        <div class="bubble">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>`;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return msgDiv;
}

async function handleChat() {
    const question = userInput.value.trim();
    if (!question) return;

    // UI Updates
    addMessage(question, 'user');
    userInput.value = '';
    sendBtn.disabled = true;

    const loadingMsg = addLoadingMessage();

    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        chatHistory.removeChild(loadingMsg);

        if (res.ok) {
            const data = await res.json();
            const aiMsg = addMessage(data.answer, 'ai');

            // Append citations if any
            if (data.citations && data.citations.length > 0) {
                const citeDiv = document.createElement('div');
                citeDiv.className = 'citations';
                citeDiv.innerHTML = `<strong>Reference Sources:</strong>`;

                data.citations.forEach(cite => {
                    const item = document.createElement('span');
                    item.className = 'citation-item';
                    item.innerText = `- [${cite.source} p.${cite.page}] ${cite.content.substring(0, 50)}...`;
                    citeDiv.appendChild(item);
                });

                aiMsg.appendChild(citeDiv);
                chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll again for citations
            }
        } else {
            addMessage("Sorry, something went wrong.", 'ai');
        }
    } catch (err) {
        chatHistory.removeChild(loadingMsg);
        addMessage("Network error.", 'ai');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', handleChat);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChat();
});

// Init
loadFiles();
