from flask import Flask, render_template
from game.game import Game

app = Flask(__name__)

# Instanța jocului (deocamdată există un singur joc în memorie)
game = Game()


@app.route("/")
def index():
    """
    Afișează pagina principală.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)