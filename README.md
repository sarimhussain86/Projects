# Django Socket Chat App

This is a real-time chat application built with **Django**, **Django Channels**, and **WebSocket**. It allows multiple users to join chat rooms, send messages instantly, and receive **acknowledgments** (green checkmarks) to confirm message delivery. The app uses **Daphne** as the ASGI server, **Nginx** as a reverse proxy and static file server, and **Redis** as the channel layer backend. I developed this on a Windows machine (Django/Daphne) with WSL2 Ubuntu (Nginx/Redis), overcoming challenges like static file errors and WebSocket configuration.

## Features
- **Real-time Messaging**: Users can send and receive messages instantly in chat rooms via WebSocket.
- **Acknowledgments**: Green checkmarks (✓) confirm message delivery.
- **Custom Usernames**: Users can set usernames (defaults to "Anonymous").
- **Responsive UI**: Clean interface with CSS styling and JavaScript for dynamic updates.
- **No Message Duplication**: Fixed issue where users received their own messages twice.
- **Cross-Platform Setup**: Runs on Windows (Django/Daphne) and WSL2 Ubuntu (Nginx/Redis).

## Prerequisites
- **Python 3.8+** (for Django)
- **Redis** (for channel layer)
- **Nginx** (for reverse proxy and static files)
- **WSL2 Ubuntu** (optional, for Nginx/Redis)
- **Git** (to clone the repository)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/django-socket-chat-app.git
cd django-socket-chat-app
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # Linux/WSL2
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
Or manually install:
```bash
pip install django channels daphne
```

### 4. Configure Redis
Install and start Redis (I set this up myself in WSL2 Ubuntu):
```bash
sudo apt update
sudo apt install redis-server
sudo service redis start
redis-cli ping  # Should return PONG
```

### 5. Configure Django
Update `chatapp/settings.py` with your Windows IP (from `ipconfig`, e.g., `192.168.1.100`):
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.100', '*']
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Set Up Nginx (WSL2 Ubuntu)
Create/edit `/etc/nginx/sites-available/chatapp`:
```nginx
server {
    listen 80;
    server_name localhost 127.0.0.1;

    location /static/ {
        alias /mnt/d/PycharmProjects/chatapp_socket/chatapp/staticfiles/;
        expires 30d;
        access_log off;
        types {
            text/css css;
            application/javascript js;
        }
    }

    location /ws/ {
        proxy_pass http://192.168.1.100:8000;  # Your Windows IP
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    location / {
        proxy_pass http://192.168.1.100:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Link and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/chatapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Run Daphne
```bash
cd chatapp
daphne -b 0.0.0.0 -p 8000 chatapp.asgi:application
```

### 9. Test the App
- Open `http://127.0.0.1/chats/room/testroom/` in two browser tabs.
- Send messages (e.g., "Hello!" as "User1").
- Verify real-time messaging and green checkmarks for **acknowledgments**.

## Project Structure
```
django-socket-chat-app/
├── chatapp/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/
│   │   ├── chats/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── js/
│   │   │   │   └── chat.js
│   ├── staticfiles/  (after collectstatic)
│   ├── templates/
│   │   ├── chats/
│   │   │   └── chat.html
│   ├── chats/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── routing.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
├── venv/
├── manage.py
├── requirements.txt
├── README.md
```

- **`chatapp/`**: Project settings, ASGI, and URLs.
- **`chats/`**: Chat app logic (views, consumers, routing).
- **`static/`**: CSS and JavaScript files.
- **`templates/chats/`**: HTML templates.
- **`staticfiles/`**: Collected static files for serving.

## Key Components

### Backend
- **settings.py**: Configures Django, Channels, and static files.
- **asgi.py**: Routes HTTP and WebSocket requests.
- **consumers.py**: Handles WebSocket connections, broadcasting, and **acknowledgments**.
- **routing.py**: Maps WebSocket URLs to `ChatConsumer`.
- **urls.py/views.py**: Renders `chat.html` for chat rooms.

### Frontend
- **chat.html**: Chat interface with links to `style.css` and `chat.js`.
- **style.css**: Styles the chat container, log, and input.
- **chat.js**: Manages WebSocket communication, message display, and **acknowledgments**.

## Challenges and Solutions
1. **400 Bad Request**:
   - Issue: `Invalid HTTP_HOST header` when accessing `127.0.0.1:8000`.
   - Solution: Added `127.0.0.1` and Windows IP to `ALLOWED_HOSTS`.

2. **Static File Errors**:
   - Issue: MIME type (`text/html`) and 404 errors for `style.css` and `chat.js`.
   - Solution: Temporarily embedded CSS/JS in `chat.html`, then fixed Nginx `alias` and `types`.

3. **WebSocket 404**:
   - Issue: `runserver` didn’t support WebSocket.
   - Solution: Used Daphne for ASGI.

4. **Message Duplication**:
   - Issue: Users received their own messages twice.
   - Solution: Modified `ChatConsumer` to exclude sender in `chat_message`.

## Troubleshooting
- **Static Files Not Loading**:
  - Verify `staticfiles/chats/css/style.css` and `chat.js` exist.
  - Run `python manage.py collectstatic`.
  - Check Nginx logs: `sudo cat /var/log/nginx/error.log`.
- **WebSocket Fails**:
  - Ensure Redis is running: `redis-cli ping`.
  - Check Daphne logs for errors.
- **Nginx Errors**:
  - Verify `alias` path in Nginx config.
  - Test config: `sudo nginx -t`.