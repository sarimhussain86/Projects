console.log("hi");
console.log(window.location.host);
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const chatLog = document.getElementById('chat-log');

    if (data.type === 'message') {
        const messageElement = document.createElement('p');
        messageElement.className = 'message';
        messageElement.innerText = `${data.username}: ${data.message}`;
        messageElement.dataset.messageId = data.message_id;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    } else if (data.type === 'ack') {
        const messageElement = document.querySelector(`[data-message-id="${data.message_id}"]`);
        if (messageElement) {
            messageElement.classList.add('sent'); // Mark as acknowledged
        }
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function generateMessageId() {
    return 'msg_' + Math.random().toString(36).substr(2, 9);
}

function sendMessage() {
    const messageInput = document.getElementById('chat-message-input');
    const usernameInput = document.getElementById('username');
    const message = messageInput.value;
    const username = usernameInput.value || 'Anonymous';
    const messageId = generateMessageId();

    if (message.trim()) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'username': username,
            'message_id': messageId
        }));
        messageInput.value = '';
    }
}

document.getElementById('chat-message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});