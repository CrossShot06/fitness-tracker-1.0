// Initial scroll on page load
document.addEventListener('DOMContentLoaded', function() {
    var chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

// Scroll after HTMX content updates
document.body.addEventListener('htmx:afterSwap', function(evt) {
    var chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        setTimeout(function() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 0);
    }
});
