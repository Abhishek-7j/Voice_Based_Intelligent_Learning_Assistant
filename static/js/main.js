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

    // Gemini Image Options
    const imageUploadTrigger = document.getElementById('image-upload-trigger');
    const imageFileInput = document.getElementById('image-file-input');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image-btn');

    // Camera Panel Elements
    const cameraPanel = document.getElementById('camera-panel');
    const cameraBtn = document.getElementById('camera-btn');
    const cameraCloseBtn = document.getElementById('camera-close-btn');
    const webcam = document.getElementById('webcam');
    const captureCanvas = document.getElementById('capture-canvas');
    const captureBtn = document.getElementById('capture-btn');
    const visionResults = document.getElementById('vision-results');

    // Floating Audio Controller Elements
    const audioControlBar = document.getElementById('audio-control-bar');
    const audioStatusText = document.getElementById('audio-status-text');
    const audioBtnRetell = document.getElementById('audio-btn-retell');
    const audioBtnPause = document.getElementById('audio-btn-pause');
    const audioBtnStop = document.getElementById('audio-btn-stop');

    // Accessibility Elements
    const highContrastToggle = document.getElementById('high-contrast-toggle');
    const hotwordToggle = document.getElementById('hotword-toggle');
    const speechSpeedInput = document.getElementById('speech-speed');
    const speedLabel = document.getElementById('speed-label');

    // Stats Elements
    const sessionTime = document.getElementById('session-time');
    const sessionQueries = document.getElementById('session-queries');

    let currentMode = 'Teacher';
    let currentConversationId = null;
    let isRecording = false;
    let webcamStream = null;
    let currentUploadedImageBase64 = null;

    // Study Stats State
    let queryCount = 0;
    let startTime = Date.now();

    // Timer logic
    setInterval(() => {
        const elapsedSecs = Math.floor((Date.now() - startTime) / 1000);
        const mins = String(Math.floor(elapsedSecs / 60)).padStart(2, '0');
        const secs = String(elapsedSecs % 60).padStart(2, '0');
        sessionTime.textContent = `${mins}:${secs}`;
    }, 1000);

    // --- Speech Recognition ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;

    function stopSpeechPlayback() {
        if (ttsPlayer) {
            ttsPlayer.pause();
            ttsPlayer.currentTime = 0;
        }
        if (audioControlBar) {
            audioControlBar.style.display = 'none';
        }
    }

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            stopSpeechPlayback(); // Instantly pause TTS player when user starts mic recording
            isRecording = true;
            micBtn.classList.add('recording');
            voiceVisualizer.style.display = 'flex';
        };

        recognition.onend = () => {
            isRecording = false;
            micBtn.classList.remove('recording');
            voiceVisualizer.style.display = 'none';
            // If hotword activation is checked, restart listening for hotword
            if (hotwordToggle.checked && hotwordRecognition && isListeningForHotword) {
                try {
                    hotwordRecognition.start();
                } catch(e) {}
            }
        };

        recognition.onresult = (event) => {
            userInput.value = event.results[0][0].transcript;
            handleSendMessage();
        };
    }


    // --- Memory Toggle Listener ---
    const memoryToggle = document.getElementById('memory-toggle');
    if (memoryToggle) {
        if (localStorage.getItem('user-memory') === 'disabled') {
            memoryToggle.checked = false;
        }
        memoryToggle.addEventListener('change', () => {
            localStorage.setItem('user-memory', memoryToggle.checked ? 'enabled' : 'disabled');
        });
    }

    // --- Accessibility Theme Toggling ---
    highContrastToggle.addEventListener('change', () => {
        if (highContrastToggle.checked) {
            document.body.classList.add('theme-high-contrast');
            localStorage.setItem('high-contrast', 'enabled');
        } else {
            document.body.classList.remove('theme-high-contrast');
            localStorage.setItem('high-contrast', 'disabled');
        }
    });

    if (localStorage.getItem('high-contrast') === 'enabled') {
        highContrastToggle.checked = true;
        document.body.classList.add('theme-high-contrast');
    }

    // Speed Slider
    speechSpeedInput.addEventListener('input', () => {
        const rate = speechSpeedInput.value;
        speedLabel.textContent = rate;
        ttsPlayer.playbackRate = parseFloat(rate);
    });

    // --- Hands-Free Trigger (Hotword) Logic ---
    let hotwordRecognition = null;
    let isListeningForHotword = false;

    function initHotwordRecognition() {
        if (!SpeechRecognition) return;
        hotwordRecognition = new SpeechRecognition();
        hotwordRecognition.continuous = true;
        hotwordRecognition.interimResults = true;
        hotwordRecognition.lang = 'en-US';

        hotwordRecognition.onresult = (event) => {
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                const transcript = event.results[i][0].transcript.toLowerCase().trim();
                if (transcript.includes("hey assistant") || transcript.includes("assistant")) {
                    playChime();
                    isListeningForHotword = false;
                    hotwordRecognition.stop();
                    setTimeout(() => {
                        if (recognition) {
                            try {
                                recognition.start();
                            } catch(e) {}
                        }
                    }, 400);
                    break;
                }
            }
        };

        hotwordRecognition.onend = () => {
            if (hotwordToggle.checked && !isRecording) {
                try {
                    hotwordRecognition.start();
                } catch(e) {}
            }
        };
    }

    function playChime() {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            
            // Double high chime
            osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
            gain.gain.setValueAtTime(0.08, ctx.currentTime);
            osc.start();
            osc.stop(ctx.currentTime + 0.12);
            
            setTimeout(() => {
                const osc2 = ctx.createOscillator();
                const gain2 = ctx.createGain();
                osc2.connect(gain2);
                gain2.connect(ctx.destination);
                osc2.frequency.setValueAtTime(659.25, ctx.currentTime); // E5
                gain2.gain.setValueAtTime(0.08, ctx.currentTime);
                osc2.start();
                osc2.stop(ctx.currentTime + 0.12);
            }, 150);
        } catch (err) {
            console.error("Audio Context Chime Error:", err);
        }
    }

    hotwordToggle.addEventListener('change', () => {
        if (hotwordToggle.checked) {
            if (!hotwordRecognition) initHotwordRecognition();
            isListeningForHotword = true;
            try {
                hotwordRecognition.start();
            } catch(e) {}
        } else {
            isListeningForHotword = false;
            if (hotwordRecognition) {
                try {
                    hotwordRecognition.stop();
                } catch(e) {}
            }
        }
    });

    // Keyboard Hotkey (Spacebar to start/stop mic, Esc to pause TTS)
    window.addEventListener('keydown', (e) => {
        // Skip hotkeys if user is currently typing in the input box
        if (document.activeElement === userInput) {
            return;
        }

        if (e.code === 'Space') {
            e.preventDefault();
            if (recognition) {
                isRecording ? recognition.stop() : recognition.start();
            }
        } else if (e.code === 'Escape') {
            e.preventDefault();
            ttsPlayer.pause();
        }
    });

    // --- Image Preview / Handling ---
    imageUploadTrigger.addEventListener('click', () => {
        imageFileInput.click();
    });

    imageFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            currentUploadedImageBase64 = event.target.result;
            imagePreview.src = currentUploadedImageBase64;
            imagePreviewContainer.style.display = 'flex';
        };
        reader.readAsDataURL(file);
    });

    function clearImagePreview() {
        currentUploadedImageBase64 = null;
        imagePreview.src = '';
        imagePreviewContainer.style.display = 'none';
        imageFileInput.value = '';
    }

    removeImageBtn.addEventListener('click', clearImagePreview);

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
        if (!text && !currentUploadedImageBase64) return;

        // Reset text box but keep a copy of values for sending
        const textToSend = text || (currentUploadedImageBase64 ? "Analyze this uploaded photo." : "");
        const imageToSend = currentUploadedImageBase64;

        userInput.value = '';
        appendMessage('user', textToSend);
        
        // Render image in chat feed locally
        if (imageToSend) {
            const chatImgWrapper = document.createElement('div');
            chatImgWrapper.className = 'message user chat-inline-img-wrapper';
            chatImgWrapper.style.padding = '8px';
            chatImgWrapper.style.maxWidth = '180px';
            chatImgWrapper.style.marginTop = '-12px';
            
            const chatImg = document.createElement('img');
            chatImg.src = imageToSend;
            chatImg.style.width = '100%';
            chatImg.style.borderRadius = '8px';
            chatImg.style.border = '1px solid var(--border-color)';
            
            chatImgWrapper.appendChild(chatImg);
            chatHistory.appendChild(chatImgWrapper);
            chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: 'smooth' });
        }

        clearImagePreview();
        thinkingIndicator.style.display = 'block';

        // Increment stats query count
        queryCount++;
        sessionQueries.textContent = queryCount;

        try {
            const selectedVoice = voiceSelect.value;
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    text: textToSend, 
                    mode: currentMode, 
                    conversation_id: currentConversationId,
                    voice: selectedVoice,
                    image_data: imageToSend
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

                // Cache conversation history locally
                if (currentConversationId) {
                    const cachedKey = `cached_history_${currentConversationId}`;
                    let localHistory = [];
                    const existing = localStorage.getItem(cachedKey);
                    if (existing) {
                        try { localHistory = JSON.parse(existing); } catch(e) {}
                    }
                    localHistory.push({ role: 'user', content: textToSend });
                    localHistory.push({ role: 'ai', content: data.response });
                    localStorage.setItem(cachedKey, JSON.stringify(localHistory));
                }

                if (data.audio_url && autoplayToggle.checked) {
                    ttsPlayer.src = data.audio_url;
                    // Apply current playback speed rate
                    ttsPlayer.playbackRate = parseFloat(speechSpeedInput.value);
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
        let conversations = [];
        try {
            const response = await fetch('/history');
            conversations = await response.json();
            // Cache conversations list
            localStorage.setItem('cached_conversations', JSON.stringify(conversations));
        } catch (err) {
            console.warn("Failed to load conversations from server, attempting local storage fallback:", err);
            const cached = localStorage.getItem('cached_conversations');
            if (cached) {
                try { conversations = JSON.parse(cached); } catch(e) {}
            }
        }

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
        let messages = [];
        try {
            thinkingIndicator.style.display = 'block';
            const response = await fetch(`/history/${convId}`);
            messages = await response.json();
            // Cache individual chat history
            localStorage.setItem(`cached_history_${convId}`, JSON.stringify(messages));
        } catch (err) {
            console.warn("Failed to fetch messages for session from server, attempting local storage fallback:", err);
            const cached = localStorage.getItem(`cached_history_${convId}`);
            if (cached) {
                try { messages = JSON.parse(cached); } catch(e) {}
            }
        } finally {
            thinkingIndicator.style.display = 'none';
        }

        // Clear current messages
        chatHistory.innerHTML = '';
        messages.forEach(msg => {
            appendMessage(msg.role === 'user' ? 'user' : 'ai', msg.content);
        });
    }

    async function deleteConversation(convId) {
        if (!confirm("Are you sure you want to delete this chat session?")) return;
        try {
            await fetch(`/clear/${convId}`, { method: 'POST' });
        } catch (err) {
            console.warn("Could not delete session from server:", err);
        }

        // Remove from local cache
        localStorage.removeItem(`cached_history_${convId}`);
        const cached = localStorage.getItem('cached_conversations');
        if (cached) {
            try {
                let conversations = JSON.parse(cached);
                conversations = conversations.filter(c => c.id !== convId);
                localStorage.setItem('cached_conversations', JSON.stringify(conversations));
            } catch(e) {}
        }

        if (currentConversationId === convId) {
            startNewChat();
        }
        loadConversations();
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
        clearImagePreview();
        ttsPlayer.pause();
        audioControlBar.style.display = 'none';
        
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
        
        visionResults.textContent = "AI capturing frame...";
        
        setTimeout(() => {
            const dataUrl = captureCanvas.toDataURL('image/jpeg');
            currentUploadedImageBase64 = dataUrl;
            imagePreview.src = dataUrl;
            imagePreviewContainer.style.display = 'flex';
            
            visionResults.innerHTML = `<strong>✨ Image captured!</strong> You can now type a question below to analyze this photo.`;
            
            // Close camera panel after a short delay
            setTimeout(stopCamera, 1000);
        }, 800);
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

    // --- TTS Player Listeners ---
    ttsPlayer.addEventListener('play', () => {
        audioControlBar.style.display = 'flex';
        audioStatusText.textContent = "Speaking...";
        audioBtnPause.innerHTML = '<i class="fas fa-pause"></i>';
    });

    ttsPlayer.addEventListener('pause', () => {
        audioStatusText.textContent = "Paused";
        audioBtnPause.innerHTML = '<i class="fas fa-play"></i>';
    });

    ttsPlayer.addEventListener('ended', () => {
        audioControlBar.style.display = 'none';
    });

    // --- Audio Control Widget Actions ---
    audioBtnPause.addEventListener('click', () => {
        if (ttsPlayer.paused) {
            // Apply speed rate on resume
            ttsPlayer.playbackRate = parseFloat(speechSpeedInput.value);
            ttsPlayer.play();
        } else {
            ttsPlayer.pause();
        }
    });

    audioBtnStop.addEventListener('click', () => {
        ttsPlayer.pause();
        ttsPlayer.currentTime = 0;
        audioControlBar.style.display = 'none';
    });

    audioBtnRetell.addEventListener('click', () => {
        ttsPlayer.currentTime = 0;
        ttsPlayer.playbackRate = parseFloat(speechSpeedInput.value);
        ttsPlayer.play();
    });

    // --- Event Listeners ---
    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleSendMessage(); });

    micBtn.addEventListener('click', () => {
        if (!recognition) return alert("Speech recognition not supported in this browser.");
        stopSpeechPlayback(); // Instantly stop active TTS when tapping mic
        isRecording ? recognition.stop() : recognition.start();
    });

    // --- Adaptive Pacing Quick Action Chips (Section 5.3 & 7.3 Project Report) ---
    const chipBtns = document.querySelectorAll('.chip-btn');
    chipBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            if (action === 'simplify') {
                userInput.value = "Simplify that in simpler terms";
                handleSendMessage();
            } else if (action === 'differently') {
                userInput.value = "Explain that differently using a real-world analogy";
                handleSendMessage();
            } else if (action === 'repeat') {
                if (ttsPlayer && ttsPlayer.src) {
                    ttsPlayer.currentTime = 0;
                    ttsPlayer.playbackRate = parseFloat(speechSpeedInput.value);
                    ttsPlayer.play();
                } else {
                    userInput.value = "Repeat the last answer";
                    handleSendMessage();
                }
            } else if (action === 'quiz') {
                const quizBtn = document.querySelector('.mode-btn[data-mode="Quiz"]');
                if (quizBtn) quizBtn.click();
                userInput.value = "Quiz me";
                handleSendMessage();
            }
        });
    });

    // --- Screen-Reader & Keyboard Accessibility Shortcuts (Section 5.2 Project Report) ---
    window.addEventListener('keydown', (e) => {
        if (e.altKey) {
            const key = e.key.toLowerCase();
            if (key === 'm') {
                e.preventDefault();
                micBtn.click(); // Alt+M: Toggle Microphone
            } else if (key === 's') {
                e.preventDefault();
                audioBtnStop.click(); // Alt+S: Stop / Silence Audio
            } else if (key === 'r') {
                e.preventDefault();
                audioBtnRetell.click(); // Alt+R: Repeat Last Answer
            } else if (key === 'k') {
                e.preventDefault();
                userInput.focus(); // Alt+K: Focus Search Bar
            }
        }
    });

    const imageGenBtn = document.getElementById('image-gen-btn');
    if (imageGenBtn) {
        imageGenBtn.addEventListener('click', () => {
            const promptVal = prompt("Enter a prompt for AI Image Generation (e.g. 'Milky Way galaxy', 'Quantum computer'):");
            if (promptVal && promptVal.trim()) {
                userInput.value = `Generate an image of ${promptVal.trim()}`;
                handleSendMessage();
            }
        });
    }

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
    cameraBtn.addEventListener('click', startCamera);
    cameraCloseBtn.addEventListener('click', stopCamera);
    captureBtn.addEventListener('click', captureAndAnalyze);

    // Export Handler
    exportHistoryBtn.addEventListener('click', exportHistory);

    // --- Visual Revision Flashcards Deck ---
    const flashcardDeck = [
        {
            category: "Science",
            term: "Superposition",
            definition: "A principle of quantum mechanics where a particle exists in multiple states (0 and 1) simultaneously until measured."
        },
        {
            category: "Coding",
            term: "Recursion",
            definition: "A programming technique where a function calls itself to break down complex problems into simpler sub-problems."
        },
        {
            category: "Study Skill",
            term: "Active Recall",
            definition: "Testing yourself on a topic rather than re-reading notes. Proven to lock concepts into long-term memory."
        },
        {
            category: "History",
            term: "D-Day Landings",
            definition: "June 6, 1944: The Allied invasion of Normandy, which marked the beginning of the liberation of Western Europe in WWII."
        },
        {
            category: "Science",
            term: "Entanglement",
            definition: "A quantum phenomenon where two linked particles instantaneously affect each other's state regardless of distance."
        }
    ];

    let currentCardIndex = 0;
    const flashcardEl = document.getElementById('flashcard');
    const cardCategoryEl = document.getElementById('card-category');
    const cardFrontTextEl = document.getElementById('card-front-text');
    const cardBackTextEl = document.getElementById('card-back-text');
    const cardIndicatorEl = document.getElementById('card-indicator');
    const prevCardBtn = document.getElementById('prev-card-btn');
    const nextCardBtn = document.getElementById('next-card-btn');

    if (flashcardEl) {
        flashcardEl.addEventListener('click', () => {
            flashcardEl.classList.toggle('flipped');
        });
    }

    function updateFlashcard() {
        if (!flashcardEl) return;
        // Unflip card before updating content
        flashcardEl.classList.remove('flipped');
        
        setTimeout(() => {
            const card = flashcardDeck[currentCardIndex];
            cardCategoryEl.textContent = card.category;
            cardFrontTextEl.textContent = card.term;
            cardBackTextEl.textContent = card.definition;
            cardIndicatorEl.textContent = `${currentCardIndex + 1} / ${flashcardDeck.length}`;
        }, 150); // Small delay to sync with flipping back animation
    }

    if (prevCardBtn) {
        prevCardBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            currentCardIndex = (currentCardIndex - 1 + flashcardDeck.length) % flashcardDeck.length;
            updateFlashcard();
        });
    }

    if (nextCardBtn) {
        nextCardBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            currentCardIndex = (currentCardIndex + 1) % flashcardDeck.length;
            updateFlashcard();
        });
    }

    // Initial load configurations
    loadConversations();

    // --- Register Service Worker ---
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(reg => console.log('ServiceWorker registered with scope: ', reg.scope))
                .catch(err => console.error('ServiceWorker registration failed: ', err));
        });
    }

    // --- PWA Installation Logic ---
    const installAppBtn = document.getElementById('install-app-btn');
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome from automatically showing the prompt
        e.preventDefault();
        // Stash the event so it can be triggered later.
        deferredPrompt = e;
        // Update UI to show the install button
        if (installAppBtn) {
            installAppBtn.style.display = 'block';
        }
    });

    if (installAppBtn) {
        installAppBtn.addEventListener('click', async () => {
            if (!deferredPrompt) return;
            // Show the prompt
            deferredPrompt.prompt();
            // Wait for the user to respond to the prompt
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to install prompt: ${outcome}`);
            // We've used the prompt, and can't use it again, discard it
            deferredPrompt = null;
            // Hide the install button
            installAppBtn.style.display = 'none';
        });
    }

    window.addEventListener('appinstalled', () => {
        console.log('PWA application was installed successfully.');
        if (installAppBtn) {
            installAppBtn.style.display = 'none';
        }
    });
});
