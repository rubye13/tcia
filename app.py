from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)
DB_NAME = "foodwise.db"

# Минимальный список продуктов
PRODUCTS = [
    "яблоко",
    "банан",
    "хлеб",
    "молоко",
    "рис",
    "курица"
]

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Пока обработка данных формы отсутствует
        pass
    return render_template_string(TEMPLATE, products=PRODUCTS)

TEMPLATE = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>FoodWise</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
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
                <button class="btn btn-success w-100" disabled>Добавить (пока не работает)</button>
            </div>
        </div>
    </form>

    <div class="alert alert-warning mt-3">
        ⚙️ Форма отправки пока не обрабатывается.
    </div>
</div>
</body>
</html>
"""

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
