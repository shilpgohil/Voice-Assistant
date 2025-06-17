<script>
  const micButton = document.getElementById("mic-button");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const chatBox = document.getElementById("chat-box");

  const isSpeechSupported = 'webkitSpeechRecognition' in window;
  let recognition;
  let isListening = false;

  if (isSpeechSupported) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-IN';

    recognition.onstart = () => {
      isListening = true;
      micButton.textContent = "🎙️ Listening...";
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      userInput.value = transcript;
      sendButton.click();
    };

    recognition.onerror = (event) => {
      console.error("Speech error:", event.error);
      micButton.textContent = "Mic Error";
      isListening = false;
    };

    recognition.onend = () => {
      micButton.textContent = "Start Speaking";
      isListening = false;
    };

    micButton.onclick = () => {
      if (isListening) {
        recognition.stop(); // Stop if already listening
        return;
      }

      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(() => {
          recognition.start();
        })
        .catch(err => {
          alert("Microphone access is required.");
          console.error("Mic permission error:", err);
        });
    };
  } else {
    micButton.disabled = true;
    micButton.textContent = "🎤 Mic not supported";
  }

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

  function addMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = sender;
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function speakText(text) {
    const synth = window.speechSynthesis;
    if (!synth) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN';
    synth.speak(utterance);
  }
</script>
