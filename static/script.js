document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-button');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    let recognition;
    let isRecording = false;
    let manuallyStopped = false;
    let currentUtterance = null;

    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isRecording = true;
            micButton.textContent = 'Stop Speaking';
            micButton.classList.add('recording');
            displayMessage('Listening...', 'ai');
            stopBotSpeaking();
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            if (finalTranscript) {
                displayMessage(finalTranscript, 'user');
                userInput.value = finalTranscript;
                sendMessage(finalTranscript);
            } else {
                userInput.value = interimTranscript;
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            displayMessage('Error: ' + event.error, 'ai');
            resetMicButton();
        };

        recognition.onend = () => {
            isRecording = false;
            resetMicButton();
        };
    } else {
        micButton.textContent = 'Speech Recognition Not Supported';
        micButton.disabled = true;
    }

    micButton.addEventListener('click', () => {
        if (isRecording) {
            manuallyStopped = true;
            recognition.stop();
        } else {
            manuallyStopped = false;
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

    function resetMicButton() {
        micButton.textContent = 'Start Speaking';
        micButton.classList.remove('recording');
    }

    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
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

    function speakText(text) {
        if (currentUtterance) {
            window.speechSynthesis.cancel();
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
