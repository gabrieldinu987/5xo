from game.board import Board

b = Board()

b.place_symbol(10,10,"X")

print(b.grid[10][10])