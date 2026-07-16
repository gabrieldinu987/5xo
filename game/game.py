from game.service import GameService

class Game:
    """
    Reprezintă o partidă completă.
    """

    def __init__(self):
        self.service = GameService()

    def play(self, row, col):
        self.service.play(row, col)

    def reset(self):
        self.service.reset()

    def get_state(self):
        return self.service.get_state()