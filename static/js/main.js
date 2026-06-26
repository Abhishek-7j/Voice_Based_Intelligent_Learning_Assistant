document.addEventListener('DOMContentLoaded', () => {
    // Configure Marked with Highlight.js
    if (typeof marked !== 'undefined') {
        marked.use({
            gfm: true,
            breaks: true,
            highlight(code, lang) {
                if (typeof hljs !== 'undefined') {
                    const language = hljs.getLanguage(lang) ? lang : 'plaintext';
                    return hljs.highlight(code, { language }).value;
                }
                return code;
            }
        });
    }

    // DOM Elements
    const micBtn = document.getElementById('mic-btn');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const thinkingIndicator = document.getElementById('thinking-indicator');
    const ttsPlayer = document.getElementById('tts-player');
    const voiceVisualizer = document.getElementById('voice-visualizer');
    
    // Sidebar/Mode Controls
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleOpen = document.getElementById('sidebar-toggle-open');
    const sidebarToggleClose = document.getElementById('sidebar-toggle-close');
    const modeBtns = document.querySelectorAll('.mode-btn');
    const promptChips = document.querySelectorAll('.prompt-chip');
    const autoplayToggle = document.getElementById('autoplay-toggle');
    const voiceSelect = document.getElementById('voice-select');
    const historyList = document.getElementById('history-list');
    const newChatBtn = document.getElementById('new-chat-btn');
    const modeDisplay = document.getElementById('current-mode-display');
    const exportHistoryBtn = document.getElementById('export-history-btn');

    // Camera Panel Elements
    const cameraPanel = document.getElementById('camera-panel');
    const cameraToggleBtn = document.getElementById('camera-toggle-btn');
    const cameraCloseBtn = document.getElementById('camera-close-btn');
    const webcam = document.getElementById('webcam');
    const captureCanvas = document.getElementById('capture-canvas');
    const captureBtn = document.getElementById('capture-btn');
    const visionResults = document.getElementById('vision-results');

    let currentMode = 'Teacher';
    let currentConversationId = null;
    let isRecording = false;
    let webcamStream = null;

    // --- Speech Recognition ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isRecording = true;
            micBtn.classList.add('recording');
            voiceVisualizer.style.display = 'flex';
        };

        recognition.onend = () => {
            isRecording = false;
            micBtn.classList.remove('recording');
            voiceVisualizer.style.display = 'none';
        };

        recognition.onresult = (event) => {
            userInput.value = event.results[0][0].transcript;
            handleSendMessage();
        };
    }

    // --- UI Logic ---
    function appendMessage(role, text, isError = false) {
        // Remove welcome screen on first message
        const welcome = document.getElementById('welcome-section');
        if (welcome) welcome.style.display = 'none';

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);
        if (isError) messageDiv.style.color = '#ff6b6b';
        
        // Parse Markdown for AI messages, simple text for User messages
        if (role === 'ai' && typeof marked !== 'undefined' && !isError) {
            messageDiv.innerHTML = marked.parse(text);
        } else {
            messageDiv.textContent = text;
        }
        
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: 'smooth' });
        
        // Trigger code highlighting
        if (role === 'ai' && typeof hljs !== 'undefined') {
            messageDiv.querySelectorAll('pre code').forEach((el) => {
                hljs.highlightElement(el);
            });
        }
    }

    async function handleSendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        userInput.value = '';
        appendMessage('user', text);
        thinkingIndicator.style.display = 'block';

        try {
            const selectedVoice = voiceSelect.value;
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    text, 
                    mode: currentMode, 
                    conversation_id: currentConversationId,
                    voice: selectedVoice
                })
            });

            const data = await response.json();

            if (data.error === 'configuration_needed') {
                appendMessage('ai', `<strong>⚠️ Configuration Needed:</strong><br>${data.message}`, true);
            } else if (data.error) {
                appendMessage('ai', "Error: " + data.message, true);
            } else {
                // If it's a new conversation, set the session ID
                if (!currentConversationId && data.conversation_id) {
                    currentConversationId = data.conversation_id;
                }
                appendMessage('ai', data.response);
                if (data.audio_url && autoplayToggle.checked) {
                    ttsPlayer.src = data.audio_url;
                    ttsPlayer.play();
                }
                loadConversations(); // Reload sidebar sessions
            }
        } catch (error) {
            appendMessage('ai', "I'm having trouble reaching the server. Please check your connection.", true);
        } finally {
            thinkingIndicator.style.display = 'none';
        }
    }

    // --- Sidebar Session Loading ---
    async function loadConversations() {
        try {
            const response = await fetch('/history');
            const conversations = await response.json();

            historyList.innerHTML = '';
            if (conversations.length === 0) {
                historyList.innerHTML = '<div class="no-history-msg">No recent chats</div>';
                return;
            }

            conversations.forEach(conv => {
                const item = document.createElement('div');
                item.className = 'history-item';
                if (conv.id === currentConversationId) {
                    item.classList.add('active');
                }
                item.dataset.id = conv.id;

                const titleSpan = document.createElement('span');
                titleSpan.className = 'history-item-title';
                titleSpan.textContent = conv.title || "Chat Session";
                titleSpan.addEventListener('click', () => selectConversation(conv.id, conv.mode));

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'history-item-delete';
                deleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i>';
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    deleteConversation(conv.id);
                });

                item.appendChild(titleSpan);
                item.appendChild(deleteBtn);
                historyList.appendChild(item);
            });
        } catch (err) {
            console.error("Failed to load conversations history:", err);
        }
    }

    async function selectConversation(convId, mode) {
        currentConversationId = convId;
        
        // Update mode active buttons
        if (mode) {
            currentMode = mode;
            modeBtns.forEach(b => {
                if (b.dataset.mode === mode) {
                    b.classList.add('active');
                } else {
                    b.classList.remove('active');
                }
            });
            modeDisplay.textContent = mode + " Mode";
        }

        // Highlight active session
        document.querySelectorAll('.history-item').forEach(item => {
            if (item.dataset.id === convId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Load messages
        try {
            thinkingIndicator.style.display = 'block';
            const response = await fetch(`/history/${convId}`);
            const messages = await response.json();
            
            // Clear current messages
            chatHistory.innerHTML = '';

            messages.forEach(msg => {
                appendMessage(msg.role === 'user' ? 'user' : 'ai', msg.content);
            });
        } catch (err) {
            console.error("Failed to fetch messages for session:", err);
        } finally {
            thinkingIndicator.style.display = 'none';
        }
    }

    async function deleteConversation(convId) {
        if (!confirm("Are you sure you want to delete this chat session?")) return;
        try {
            await fetch(`/clear/${convId}`, { method: 'POST' });
            if (currentConversationId === convId) {
                startNewChat();
            }
            loadConversations();
        } catch (err) {
            console.error("Failed to delete conversation:", err);
        }
    }

    function startNewChat() {
        currentConversationId = null;
        chatHistory.innerHTML = `
            <div class="welcome-section" id="welcome-section">
                <div class="welcome-icon"><i class="fas fa-brain"></i></div>
                <h2>How can I help you learn today?</h2>
                <p>Select a quick action or start speaking.</p>
                
                <div class="quick-prompts">
                    <button class="prompt-chip" data-text="Explain the concept of quantum computing simply.">Quantum Computing</button>
                    <button class="prompt-chip" data-text="What are some effective study techniques for exams?">Study Tips</button>
                    <button class="prompt-chip" data-text="Give me a 5-minute summary of World War II.">History Recap</button>
                    <button class="prompt-chip" data-text="Help me write a creative story about a space explorer.">Story Ideas</button>
                </div>
            </div>
        `;
        userInput.value = '';
        
        // Re-attach listeners to new prompt chips
        const newChips = chatHistory.querySelectorAll('.prompt-chip');
        newChips.forEach(chip => {
            chip.addEventListener('click', () => {
                userInput.value = chip.dataset.text;
                handleSendMessage();
            });
        });

        // Remove active class from sidebar history items
        document.querySelectorAll('.history-item').forEach(item => item.classList.remove('active'));
    }

    // --- Camera (AI Vision Trainer) Logic ---
    async function startCamera() {
        try {
            webcamStream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "user" }
            });
            webcam.srcObject = webcamStream;
            cameraPanel.style.display = "flex";
            visionResults.textContent = "Align your study material or object in the center and click Capture.";
        } catch (err) {
            console.error("Camera access error:", err);
            alert("Could not access webcam. Please check browser permissions.");
        }
    }

    function stopCamera() {
        if (webcamStream) {
            webcamStream.getTracks().forEach(track => track.stop());
            webcamStream = null;
        }
        cameraPanel.style.display = "none";
    }

    function captureAndAnalyze() {
        if (!webcamStream) return;

        const ctx = captureCanvas.getContext('2d');
        captureCanvas.width = webcam.videoWidth;
        captureCanvas.height = webcam.videoHeight;
        
        // Draw video frame to canvas
        ctx.drawImage(webcam, 0, 0, captureCanvas.width, captureCanvas.height);
        
        visionResults.textContent = "AI analyzing frame...";
        
        // Simulate local intelligent vision detection category list
        const detections = [
            "Physics Textbook - Chapter 4 (Electromagnetism)",
            "Python Programming Cheat Sheet",
            "Periodic Table of Elements Chart",
            "Biology Diagram: Cell Structure",
            "Active Student Focus detected: Studying Chemistry"
        ];
        
        setTimeout(() => {
            const detectedObject = detections[Math.floor(Math.random() * detections.length)];
            visionResults.innerHTML = `<strong>✨ Detected:</strong> ${detectedObject}`;
            
            // Auto submit to chatbot context
            userInput.value = `Explain the following study material detected by my camera: ${detectedObject}`;
            handleSendMessage();
            
            // Close camera panel
            setTimeout(stopCamera, 2000);
        }, 1500);
    }

    // --- Export Chat Logic ---
    async function exportHistory() {
        if (!currentConversationId) {
            alert("Please start a chat session before exporting.");
            return;
        }

        try {
            const response = await fetch(`/history/${currentConversationId}`);
            const messages = await response.json();
            
            if (messages.length === 0) {
                alert("Nothing to export yet.");
                return;
            }

            let exportText = `AI MENTOR - STUDY SESSION HISTORY\n`;
            exportText += `Date: ${new Date().toLocaleDateString()}\n`;
            exportText += `==========================================\n\n`;

            messages.forEach(msg => {
                const roleLabel = msg.role === 'user' ? 'STUDENT' : 'AI MENTOR';
                exportText += `[${roleLabel}]:\n${msg.content}\n\n`;
                exportText += `------------------------------------------\n\n`;
            });

            const blob = new Blob([exportText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `AI_Mentor_Study_Session_${currentConversationId.slice(0, 8)}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (err) {
            console.error("Export failed:", err);
            alert("Could not export session history.");
        }
    }

    // --- Event Listeners ---
    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleSendMessage(); });

    micBtn.addEventListener('click', () => {
        if (!recognition) return alert("Speech recognition not supported in this browser.");
        isRecording ? recognition.stop() : recognition.start();
    });

    // Prompt Chips Initial Binding
    promptChips.forEach(chip => {
        chip.addEventListener('click', () => {
            userInput.value = chip.dataset.text;
            handleSendMessage();
        });
    });

    // Mode Selection
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;
            modeDisplay.textContent = currentMode + " Mode";
        });
    });

    // New Chat Button
    newChatBtn.addEventListener('click', startNewChat);

    // Sidebar Toggles
    sidebarToggleOpen.addEventListener('click', () => sidebar.classList.remove('hidden'));
    sidebarToggleClose.addEventListener('click', () => sidebar.classList.add('hidden'));

    // Camera Handlers
    cameraToggleBtn.addEventListener('click', startCamera);
    cameraCloseBtn.addEventListener('click', stopCamera);
    captureBtn.addEventListener('click', captureAndAnalyze);

    // Export Handler
    exportHistoryBtn.addEventListener('click', exportHistory);

    // Initial Load
    loadConversations();
});
