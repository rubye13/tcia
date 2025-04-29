from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "FoodWise — простой счётчик калорий. Разработка в процессе."

if __name__ == "__main__":
    app.run(debug=True)