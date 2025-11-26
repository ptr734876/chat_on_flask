from flask import Flask, render_template, request,redirect, url_for, session, jsonify
from database.initdb import initDB
import sqlite3
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
db_path = initDB('main.db')

def check_is_correct(p):
    return True

@app.route('/')
def main_page():
    if 'user_login' in session:
        return render_template('base.html', user_login=session['user_login'])
    return render_template('base.html')

@app.route('/register', methods=['POST', 'GET'])
def register_page():
    if 'user_login' in session:
        return redirect(url_for('main_page'))
    error = None
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        if password != password1:
            error = 'passwords are not the same'
        else:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE login = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            if not user:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute("INSERT INTO Users (login, password) VALUES (?, ?)", (username, password))
                conn.commit()
                
                cursor.execute("SELECT id FROM Users WHERE login = ?", (username,))
                new_id = cursor.fetchone()[0]

                cursor.execute("SELECT id, login FROM Users WHERE login != ?", (username,))
                all_users = cursor.fetchall()

                for user_id, user_login in (all_users):
                    chat_name = f"{user_login} - {username}"

                    cursor.execute("INSERT INTO Chats (name) VALUES (?)", (chat_name,))
                    chat_id = cursor.lastrowid

                    cursor.execute("INSERT INTO Users_Chats (user_id, chat_id) VALUES (?, ?)", (user_id, chat_id))
                    cursor.execute("INSERT INTO Users_Chats (user_id, chat_id) VALUES (?, ?)", (new_id, chat_id))
                conn.commit()
                conn.close()
                session['user_login'] = username
                session['user_id'] = new_id
                return redirect(url_for('Chatpage'))
            else:
                error =  'user already exist'

    return render_template('register.html', error = error)

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if 'user_login' in session:
        return redirect(url_for('main_page'))
    error = None
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if check_is_correct(username):
            if check_is_correct(password):
                pass
            else:
                error = 'password is uncorrect'
        else:
            error = 'username is uncorrect'

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM Users WHERE login = ?", (username,))
        user = cursor.fetchone()
        if user:
            real_password = user[2]
            if password == real_password:
                session['user_login'] = username
                session['user_id'] = user[0]
                conn.close()
                return redirect(url_for('Chatpage'))
            else:
                error = 'Wrong password'
        else:
            error = 'unknown user'
        conn.close()
        
    return render_template('login.html', error = error)

@app.route('/ChatPage')
def Chatpage():
    if 'user_login' not in session:
        return redirect(url_for('main_page'))
    current_user_login = session['user_login']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 
    
    cursor.execute("""
        SELECT c.id, c.name, 
                (SELECT m.messege_text FROM Messeges m 
                WHERE m.chat_id = c.id 
                ORDER BY m.sent_at DESC LIMIT 1) as last_message
        FROM Chats c
        JOIN Users_Chats uc ON c.id = uc.chat_id
        JOIN Users u ON u.id = uc.user_id
        WHERE u.login = ?
    """, (current_user_login,))
    
    chats = cursor.fetchall()
    conn.close()
    
    return render_template('chat.html', chats=chats, current_user=current_user_login)

@app.route('/get_messages/<int:chat_id>')
def get_messages(chat_id):
    if 'user_login' not in session:
        return jsonify([])
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.login, m.messege_text, m.sent_at 
        FROM Messeges m
        JOIN Users u ON m.user_id = u.id
        WHERE m.chat_id = ?
        ORDER BY m.sent_at ASC
    """, (chat_id,))
    
    messages = cursor.fetchall()
    conn.close()
    
    # Форматируем сообщения для JSON
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            'sender': msg[0],
            'text': msg[1],
            'time': msg[2]
        })
    
    return jsonify(formatted_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_login' not in session:
        return jsonify({'success': False})
    
    data = request.get_json()
    chat_id = data.get('chat_id')
    message_text = data.get('message')
    
    if not chat_id or not message_text:
        return jsonify({'success': False})
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем ID текущего пользователя
    cursor.execute("SELECT id FROM Users WHERE login = ?", (session['user_login'],))
    user_id = cursor.fetchone()[0]
    
    # Сохраняем сообщение
    cursor.execute("""
        INSERT INTO Messeges (chat_id, user_id, messege_text)
        VALUES (?, ?, ?)
    """, (chat_id, user_id, message_text))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.pop('user_login', None)
    session.pop('user_id', None)
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
