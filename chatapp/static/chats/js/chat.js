<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Room</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'chats/css/style.css' %}">
</head>
<body>
    <div class="chat-container">
        <h2>Chat Room: {{ room_name }}</h2>
        <div id="chat-log" class="chat-log"></div>
        <div class="chat-input">
            <input type="text" id="username" placeholder="Your username" value="Anonymous">
            <input type="text" id="chat-message-input" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        const roomName = "{{ room_name|escapejs }}";
    </script>
    <script src="{% static 'chats/js/chat.js' %}"></script>
</body>
</html>