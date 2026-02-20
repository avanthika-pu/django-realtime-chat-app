# django-realtime-chat-app

Real-Time Chat Application (Django + Channels)

Features Implemented
- User Registration & Login
- Custom User Model (email-based login)
- One-to-one private chat
- Real-time messaging using WebSockets
- Online / Offline status indicator
- Typing indicator
- Message delivery ticks
- Logout functionality
- Message persistence in database

Tech Stack
- Django
- Django Channels
- WebSockets (ASGI)
- SQLite
- HTML / CSS / JavaScript


Setup Steps
1. Clone or open the project folder
2. Create virtual environment: python -m venv venv
3. Activate it and install dependencies: pip install django channels daphne
4. Run migrations: python manage.py migrate
5. Run server: python manage.py runserver
Testing
- Register two users
- Login in different browsers
- Open chat between them
- Verify online indicator, typing indicator and ticks
  
Notes
- User becomes online only when WebSocket connects
- Closing the tab makes the user offline
- Messages persist in database
