from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>5XO</h1>
    <h2>Welcome!</h2>
    <p>The game will be implemented soon.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)