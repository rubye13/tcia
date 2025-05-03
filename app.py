from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Пока обработка данных формы отсутствует
        pass
    return render_template_string(TEMPLATE)

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
    app.run(debug=True)
