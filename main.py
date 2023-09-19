from game import Game
from player import Player, AIPlayer

if __name__ == '__main__':
    game = Game(players=[Player(id=0), AIPlayer(id=1)])
    while game.winner() == -1:
       game.show()
       print()
       game.take_action(game.players[game.turn].choose_action(game))

    game.show()
    print(f"Player {game.winner() + 1} won!")


