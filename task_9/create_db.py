import sqlite3

db_connection = sqlite3.connect('project.sqlite')
db_cursor = db_connection.cursor()
with open('create_db.sql', 'r', encoding='utf-8') as f:
    text = f.read()
db_cursor.executescript(text)
db_cursor.close()
db_connection.close()
