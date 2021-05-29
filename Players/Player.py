from __future__ import annotations  # for typing the enclosing class

import abc
from game import Connect4Game


class Player:
    game: Connect4Game

    def __init__(self, player_turn_id=None):
        self.player_turn_id = player_turn_id
        self.last_moves = []

    @abc.abstractmethod
    def choose_action(self, game: Connect4Game) -> int:
        """
        The method to choose an action that returns a number in the interval [0, nb_col-1]
        :param game: the current Connect-4 game
        :return:
        """

    def play_against(self, opponent: Player, game: Connect4Game = Connect4Game()):
        """
        Make the agent play against another player on the given game or a new game.
        If both player have the same game turn id, self will change its game turn id
        Returns the winner
        :param opponent: another player
        :param game: The current game, if nothing specified then a new game
        :return: the winner (0 for draw, 1 for player 1, 2 for player 2
        """
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
