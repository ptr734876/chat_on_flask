from flask import Flask, render_template, request
from database.initdb import initDB
import sqlite3
app = Flask(__name__)

db_path = initDB('Users', {'login':'text not null', 'password':'text not null'}, 'Users.db')

def check_is_correct(p):
    pass

def check_is_exist(p):
    pass

@app.route('/')
def main_page():
    return render_template('base.html')

@app.route('/register', methods=['POST', 'GET'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        if password != password1:
            pass
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
                return 'registered'
            else:
                return 'user already exist'

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if check_is_correct(username):
            if check_is_correct(password):
                pass
            else:
                print('password is uncorrect')
        else:
            print('username is uncorrect')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM Users WHERE login = ?", (username,))
        user = cursor.fetchone()
        if user:
            real_password = user[2]
            if password == real_password:
                return 'CHATs'
            else:
                return 'Wrong password'
        else:
            return 'unknown user'


    return render_template('login.html')

app.run(debug=True)
