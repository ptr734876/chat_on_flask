# Chat on Flask

A real-time chat application built with Flask, allowing users to register, login, and communicate in private chats.

## Technologies Used

- **Flask**: Web framework for Python.
- **SQLite3**: Database for storing users, chats, and messages (built-in Python standard library).
- **HTML/CSS/JavaScript**: Frontend templates, styling, and AJAX for real-time messaging.
- **Jinja2**: Templating engine (included with Flask).

## Features Implemented

- **User Registration and Login**: Secure user authentication with session management.
- **Automatic Chat Creation**: Upon registration, private chats are automatically created between the new user and all existing users.
- **Chat Interface**: Displays a list of chats with the last message preview. Users can select a chat to view full message history.
- **Real-Time Messaging**: Send and receive messages in real-time using AJAX without page reloads.
- **Database Management**: SQLite database with tables for Users, Chats, Users_Chats (many-to-many relationship), and Messages.
- **Logout Functionality**: Secure logout to end user sessions.
- **Responsive Design**: Styled with CSS for a clean and user-friendly interface.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chat_on_flask
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`.

## Usage

- **Register**: Create a new account on the registration page.
- **Login**: Log in with your credentials.
- **Chat**: Select a chat from the sidebar to view and send messages.
- **Logout**: Click the logout button to end your session.

## Database Schema

- **Users**: Stores user information (id, login, password).
- **Chats**: Stores chat details (id, name, created_at).
- **Users_Chats**: Junction table for many-to-many relationship between users and chats.
- **Messages**: Stores messages (id, chat_id, user_id, message_text, sent_at).

## API Endpoints

- `GET /`: Main page.
- `POST/GET /register`: User registration.
- `POST/GET /login`: User login.
- `GET /ChatPage`: Chat interface (requires login).
- `GET /get_messages/<chat_id>`: Retrieve messages for a chat (JSON).
- `POST /send_message`: Send a message (JSON).
- `GET /logout`: Logout.

## Site Link

The application is deployed at: https://ptr734876.pythonanywhere.com/
