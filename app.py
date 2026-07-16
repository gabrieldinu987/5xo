from flask import Flask, render_template
from game.game import Game

app = Flask(__name__)

game = Game()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)