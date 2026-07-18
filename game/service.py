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

    def switch_player(self):
        self.current_player = (
            "O" if self.current_player == "X" else "X"
        )

    def is_draw(self):
        for row in self.board.grid:
            for cell in row:
                if cell is None:
                    return False
        return True

    def play(self, row, col):
        if self.game_over:
            raise ValueError("Game finished.")

        self.board.place_symbol(
            row,
            col,
            self.current_player
        )

        if WinnerChecker.check(
            self.board,
            row,
            col
        ):
            self.game_over = True
            self.winner = self.current_player
            return

        if self.is_draw():
            self.game_over = True
            return

        self.switch_player()

    def get_state(self):
        return {
            "board": self.board.grid,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "winner": self.winner
        }