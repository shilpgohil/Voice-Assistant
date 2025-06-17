const micButton = document.getElementById("mic-button");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");

// Check browser support
const isSpeechSupported = 'webkitSpeechRecognition' in window;
let recognition;

if (isSpeechSupported) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-IN';

    recognition.onstart = () => {
        micButton.textContent = "🎙️ Listening...";
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendButton.click();
        micButton.textContent = "Start Speaking";
    };

    recognition.onerror = (event) => {
        console.error("Speech error:", event.error);
        micButton.textContent = "Mic Error";
    };

    recognition.onend = () => {
        micButton.textContent = "Start Speaking";
    };

    micButton.onclick = () => {
        recognition.start();
    };
} else {
    micButton.disabled = true;
    micButton.textContent = "🎤 Mic not supported";
}

// Send text to server
sendButton.onclick = async () => {
    const question = userInput.value.trim();
    if (!question) return;

    addMessage("user", question);
    userInput.value = "";
    sendButton.disabled = true;

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await res.json();
        addMessage("bot", data.answer);
        speakText(data.answer);
    } catch (err) {
        console.error("Error:", err);
        addMessage("bot", "Sorry, there was a network issue.");
    } finally {
        sendButton.disabled = false;
    }
};

// Add messages to chat
function addMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = sender;
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Speak response
function speakText(text) {
    const synth = window.speechSynthesis;
    if (!synth) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN';
    synth.speak(utterance);
}
