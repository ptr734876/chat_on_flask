from flask import Flask, render_template, request,redirect, url_for
from database.initdb import initDB
import sqlite3
app = Flask(__name__)

db_path = initDB('main.db')

def check_is_correct(p):
    return True

@app.route('/')
def main_page():
    return render_template('base.html')

@app.route('/register', methods=['POST', 'GET'])
def register_page():
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
                conn.close()
                return redirect(url_for('Chatpage'))
            else:
                error =  'user already exist'

    return render_template('register.html', error = error)

@app.route('/login', methods=['POST', 'GET'])
def login_page():
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
                return redirect(url_for('Chatpage'))
            else:
                error = 'Wrong password'
        else:
            error = 'unknown user'


    return render_template('login.html', error = error)

@app.route('/ChatPage')
def Chatpage():
    current_user_login = "22"
    
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
    
    return render_template('chat.html', chats=chats)



app.run(debug=True)
