import random

import Players.Player as Player
from game import Connect4Game


class RandomPlayer(Player.Player):
    def choose_action(self, game: Connect4Game) -> int:
        return random.randint(0, 6)
