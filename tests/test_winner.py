from game.board import Board
from game.winner import WinnerChecker

b = Board()

for c in range(5):
    b.place_symbol(10, c, "X")

print(WinnerChecker.check(b, 10, 4))