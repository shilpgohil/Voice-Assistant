document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-button');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    let recognition;
    let isRecording = false;

    // Initialize Web Speech API
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true; // Enable continuous recognition
        recognition.interimResults = true; // Get interim results for better responsiveness
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            console.log('Recognition started. isRecording:', true);
            isRecording = true;
            micButton.textContent = 'Stop Speaking';
            micButton.classList.add('recording');
            displayMessage('Listening...', 'ai');
            // Stop bot speaking if it is currently speaking
            stopBotSpeaking();
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            if (finalTranscript) {
                displayMessage(finalTranscript, 'user');
                userInput.value = finalTranscript; // Populate input field with transcript
                sendMessage(finalTranscript); // Send transcript to backend
            } else {
                userInput.value = interimTranscript; // Show interim results in input field
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            displayMessage('Error: ' + event.error, 'ai');
            isRecording = false;
            micButton.textContent = 'Start Speaking';
            micButton.classList.remove('recording');
        };

        recognition.onend = () => {
            console.log('Recognition ended. isRecording:', false);
            isRecording = false;
            micButton.textContent = 'Start Speaking';
            micButton.classList.remove('recording');
            // Only reset manuallyStopped if it wasn't a manual stop
            if (!recognition.manuallyStopped) {
                recognition.manuallyStopped = false;
            }
        };

    } else {
        micButton.textContent = 'Speech Recognition Not Supported';
        micButton.disabled = true;
        console.warn('Web Speech API is not supported in this browser.');
    }

    micButton.addEventListener('click', () => {
        console.log('Mic button clicked. isRecording:', isRecording);
        if (isRecording) {
            recognition.manuallyStopped = true;
            recognition.stop();
        } else {
            recognition.manuallyStopped = false; // Reset flag before starting
            recognition.start();
        }
    });

    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            displayMessage(message, 'user');
            sendMessage(message);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });

    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
    }

    async function sendMessage(message) {
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message }),
            });
            const data = await response.json();
            if (data.answer) {
                displayMessage(data.answer, 'ai');
                speakText(data.answer);
            } else {
                displayMessage('Error: No answer received from bot.', 'ai');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            displayMessage('Error: Could not connect to the bot.', 'ai');
        }
    }

    let currentUtterance = null;

    function speakText(text) {
        if (currentUtterance) {
            window.speechSynthesis.cancel(); // Stop current speech
        }
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.onend = () => {
            currentUtterance = null;
        };
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            currentUtterance = null;
        };
        window.speechSynthesis.speak(utterance);
        currentUtterance = utterance;
    }

    async function stopBotSpeaking() {
        if (currentUtterance) {
            window.speechSynthesis.cancel();
            currentUtterance = null;
        }
        try {
            await fetch('/stop_speaking', {
                method: 'POST',
            });
        } catch (error) {
            console.error('Error stopping backend speaking:', error);
        }
    }
});