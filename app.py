from flask import Flask, render_template, jsonify

from game.game import Game

app = Flask(__name__)

game = Game()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state")
def state():
    """
    Returnează starea curentă a jocului.
    """
    return jsonify(game.get_state())


if __name__ == "__main__":
    app.run(debug=True)