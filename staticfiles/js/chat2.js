document.addEventListener('DOMContentLoaded', function() {

    const body = document.querySelector('body');
    const chatroom_name = body.getAttribute('data-chatroom-name')
    const chatsocket = new WebSocket('ws://127.0.0.1:8000/ws/chatroom/'+chatroom_name);
    const form = document.getElementById('chat-form');
    const input = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    function scrolltoBottom(){
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    scrolltoBottom();

    form.addEventListener('submit', function(e){

        e.preventDefault();

        const message = input.value.trim();
        if(!message) return;

        chatsocket.send(JSON.stringify({body:message}));
        input.value = '';

    });

    chatsocket.onmessage = function(e){

        const data = JSON.parse(e.data);
        if(data.content){
            chatMessages.insertAdjacentHTML('beforeend',data.content);
            scrolltoBottom();
        }

    };

    chatsocket.onopen = () => console.log("Websocket connected");
    chatsocket.onclose = () => console.log("Websocket closed");
    chatsocket.onerror = err => console.log("Websocket Error:",err);
    
});
