from game.service import GameService

game = GameService()

game.play(10,10)

game.play(11,11)

print(game.get_state())