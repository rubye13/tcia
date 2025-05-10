from flask import Flask
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "foodwise.db"

# Создание таблицы, если не существует
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            grams INTEGER NOT NULL,
            calories REAL NOT NULL,
            date TEXT NOT NULL
        )''')

@app.route('/')
def index():
    return "FoodWise: проект в разработке. База данных подключена."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)