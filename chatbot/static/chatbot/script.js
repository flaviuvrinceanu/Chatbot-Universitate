document.addEventListener('DOMContentLoaded', function() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBody = document.getElementById('chat-body');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if(e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if(message === "") return;

        appendMessage(message, 'user');  // show user message
        userInput.value = "";

        // Send message to Django server
        fetch("/chatbot/reply/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.reply, 'bot'); // show bot reply
        })
        .catch(err => {
            console.error(err);
            appendMessage("Error: could not get reply", 'bot');
        });
    }

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message');
        msgDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        msgDiv.textContent = text;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Helper function to get CSRF token from template
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
