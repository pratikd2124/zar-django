document.addEventListener("DOMContentLoaded", function() {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const openingScreen = document.querySelector(".opening-screen");
    const chatbot = document.querySelector(".chatbot");
    const closeBtn = document.querySelector(".close-btn");
    const chatbox = document.querySelector(".chatbox");
    const sendBtn = document.querySelector("#send-btn");
    const textarea = document.querySelector(".chat-input textarea");

    // Show opening screen when toggler button is clicked
    chatbotToggler.addEventListener("click", function() {
        openingScreen.classList.add("show");

        // After 2 seconds, hide opening screen and show chatbot
        setTimeout(() => {
            openingScreen.classList.remove("show");
            openingScreen.classList.add("hidden");
            openingScreen.style.display = 'none';
            chatbot.style.display = "flex";
            setTimeout(() => {
                chatbot.classList.add("show");
            }, 50);
        }, 2000);
    });

    // Close chatbox when close button is clicked
    closeBtn.addEventListener("click", function() {
        chatbot.classList.remove("show");
        setTimeout(() => {
            chatbot.style.display = "none";
        }, 300);
    });

    // Show chatbox when toggler button is clicked
    chatbotToggler.addEventListener("click", function() {
        chatbot.style.display = "flex";
        chatbot.style.animation = "slideIn 0.3s forwards";
    });

    // Close chatbox when close button is clicked
    closeBtn.addEventListener("click", function() {
        chatbot.style.animation = "slideOut 0.3s forwards";
        setTimeout(() => (chatbot.style.display = "none"), 300);
    });

    // Handle sending messages
    sendBtn.addEventListener("click", sendMessage);
    textarea.addEventListener("keypress", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    function sendMessage() {
        const message = textarea.value.trim();
        if (message === "") return;

        // Create outgoing message
        const outgoing = document.createElement("li");
        outgoing.classList.add("chat", "outgoing");
        outgoing.innerHTML = `<span class="material-symbols-outlined">
                    <img src="https://www.zarluxury.com/static/images/user.png" style="width:2rem;margin-right:10px" alt="">
                </span><p>${message}</p>`;
        chatbox.appendChild(outgoing);

        // Clear textarea
        textarea.value = "";

        // Scroll to the bottom
        chatbox.scrollTop = chatbox.scrollHeight;

        // Show "typing..." animation
        const typingAnimation = document.createElement("li");
        typingAnimation.classList.add("chat", "incoming");
        typingAnimation.innerHTML = `
            <span class="material-symbols-outlined">
                <img src="https://www.zarluxury.com/static/images/ZAR-icon.ico" style="width:2rem" alt="">
            </span>
            <p>Typing...</p>
        `;
        chatbox.appendChild(typingAnimation);

        // Scroll to show "typing..." animation
        chatbox.scrollTop = chatbox.scrollHeight;

        // Send POST request to the server
        fetch('/chatbot/chat-bot-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Ensure this is correctly retrieved
                },
                body: JSON.stringify({ message: message }) // Message is being sent here
            })
            .then(response => response.json())
            .then(data => {
                // Remove the "typing..." animation
                chatbox.removeChild(typingAnimation);

                // Process the response
                const newMessage = data.NewMessage; // The response from your server
                const status = data.status; // Status response, if needed

                // Display the chatbot's reply
                const incoming = document.createElement("li");
                incoming.classList.add("chat", "incoming");
                incoming.innerHTML = `
                <span class="material-symbols-outlined">
                    <img src="https://www.zarluxury.com/static/images/ZAR-icon.ico" style="width:2rem" alt="">
                </span>
                <p>${newMessage}</p>
            `;
                chatbox.appendChild(incoming);

                // Scroll to the latest message
                chatbox.scrollTop = chatbox.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});