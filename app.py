from flask import Flask, render_template, jsonify, request

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


@app.route("/move", methods=["POST"])
def move():

    data = request.get_json()

    row = data["row"]
    col = data["col"]

    try:
        game.play(row, col)

    except ValueError as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    return jsonify(game.get_state())


@app.route("/reset", methods=["POST"])
def reset():

    game.reset()

    return jsonify(game.get_state())


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )