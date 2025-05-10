from flask import Flask, render_template_string, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)
DB_NAME = "foodwise.db"

# Список продуктов с калорийностью на 100 г
PRODUCTS = {
    "яблоко": 52,
    "банан": 89,
    "хлеб": 265,
    "молоко": 42,
    "рис": 130,
    "курица": 239
}

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

# Добавление записи о приёме пищи
def add_meal(product, grams, calories):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('INSERT INTO meals (product, grams, calories, date) VALUES (?, ?, ?, ?)',
                     (product, grams, calories, str(date.today())))

# Получение всех приёмов пищи за сегодня
def get_today_meals():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT product, grams, calories FROM meals WHERE date = ?', (str(date.today()),))
        return cursor.fetchall()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product = request.form['product'].lower()
        grams = int(request.form['grams'])

        if product in PRODUCTS:
            cal_per_100g = PRODUCTS[product]
            calories = grams * cal_per_100g / 100
            add_meal(product, grams, calories)

        return redirect('/')

    meals = get_today_meals()
    total_calories = sum(row[2] for row in meals)

    if total_calories < 1200:
        tip = "Вы съели мало сегодня — добавьте что-то питательное!"
    elif total_calories > 2500:
        tip = "Калорий многовато — возможно, стоит сократить перекусы."
    else:
        tip = "Отличный баланс калорий!"

    return render_template_string(TEMPLATE, products=PRODUCTS.keys(), meals=meals, total=total_calories, tip=tip)

TEMPLATE = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>FoodWise</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light" style="min-height: 100vh;">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
  <div class="container">
    <a class="navbar-brand" href="/">FoodWise</a>
    <div>
      <a class="btn btn-outline-light me-2" href="/">Главная</a>
      <a class="btn btn-outline-light" href="/history">История</a>
    </div>
  </div>
</nav>
<div class="container mt-5">
    <h1 class="mb-4">FoodWise — Помощник по питанию</h1>

    <form method="post" class="mb-4">
        <div class="row g-2">
            <div class="col-md-4">
                <select class="form-select" name="product" required>
                    {% for name in products %}
                        <option value="{{ name }}">{{ name.capitalize() }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-4">
                <input type="number" name="grams" class="form-control" placeholder="Граммы" min="1" required>
            </div>
            <div class="col-md-4">
                <button class="btn btn-success w-100">Добавить</button>
            </div>
        </div>
    </form>

    <h4>Сегодняшние приёмы пищи:</h4>
    <ul class="list-group mb-3">
        {% for product, grams, cal in meals %}
            <li class="list-group-item">
                {{ product.capitalize() }} — {{ grams }} г → {{ cal|round(1) }} ккал
            </li>
        {% endfor %}
    </ul>

    <div class="alert alert-info">
        <strong>Итого:</strong> {{ total|round(1) }} ккал<br>
        <em>{{ tip }}</em>
    </div>
</div>
</body>
</html>
"""

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
