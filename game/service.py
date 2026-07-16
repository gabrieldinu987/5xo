from game.board import Board
from game.winner import WinnerChecker


class GameService:

    def __init__(self):

        self.board = Board()

        self.current_player = "X"

        self.game_over = False

        self.winner = None

    def reset(self):

        self.board.reset()

        self.current_player = "X"

        self.game_over = False

        self.winner = None

    