from __future__ import annotations  # for typing the enclosing class

import abc

import Players.MinMaxPlayer as MinMax
from game import Connect4Game


class Player:
    game: Connect4Game

    def __init__(self, player_turn_id=None):
        self.player_turn_id = player_turn_id
        self.last_moves = []

    @abc.abstractmethod
    def choose_action(self, game: Connect4Game) -> tuple[int, int]:
        pass

    def play_against(self, opponent: Player, game: Connect4Game = Connect4Game()):
        if self.player_turn_id == opponent.player_turn_id:
            self.player_turn_id = 3 - self.player_turn_id
        yellow_goes_first = game.get_turn() == 1
        winner = game.get_win()
        while winner is None:
            if game.get_turn() == self.player_turn_id:
                game.place(self.choose_action(game))
            else:
                game.place(opponent.choose_action(game))

            winner = game.get_win()

        if winner != 0 and not yellow_goes_first:
            winner = 3 - winner
        return winner

    def compute_fitness(self):
        game = Connect4Game()
        adversary = MinMax.MinMaxPlayer(3 - game.get_turn())
        score = 1
        for _ in range(10):
            winner = self.play_against(adversary, game)
            if winner == self.player_turn_id:
                score += 1
        return score

