import sqlite3
from database.initdb import initDB


db_path = initDB('main.db')

conn = sqlite3.connect(db_path)
curs = conn.cursor()
curs.execute('SELECT * FROM Chats')
users = curs.fetchall()
print(users)
conn.close()