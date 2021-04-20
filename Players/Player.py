from __future__ import annotations  # for typing the enclosing class

import abc

from game import Connect4Game


class Player:
    game: Connect4Game

    def __init__(self, player_turn_id=None):
        self.player_turn_id = player_turn_id
        self.last_moves = []

    @abc.abstractmethod
    def choose_action(self, game: Connect4Game) -> tuple[int, int]:
        pass

    def play_against(self, opponent: Player, game: Connect4Game):
        my_turn = False
        yellow_goes_first = game.get_turn() == 1
        winner = game.get_win()
        while winner is None:
            if my_turn:
                game.place(self.choose_action(game))
            else:
                game.place(opponent.choose_action(game))

            winner = game.get_win()
            my_turn = not my_turn

        if winner != 0 and not yellow_goes_first:
            winner = 3 - winner
        return winner
