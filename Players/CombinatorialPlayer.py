from __future__ import annotations

import random
from typing import Collection

import numpy as np

from Players.MinMaxPlayer import MinMaxPlayer
from Players.Player import Player
from game import Connect4Game


class RandomPlayer(Player):
    def choose_action(self, game: Connect4Game) -> int:
        return random.randint(0, 6)


class CombinatorialPlayer(Player):
    def __str__(self):
        return " ".join(self.chromosomes)

    @staticmethod
    def get_random_hypothetical_game_history():
        game = Connect4Game()
        player = RandomPlayer(3 - game.get_turn())
        while game.get_win() is None:
            placement = player.choose_action(game)
            if placement is not None:
                game.place(placement)
        return game.history


        # history = ""
        # for _ in range(6 * 7):
        #     available = "abcdefg"
        #     for c in available:
        #         if history.count(c) + history.count(c.upper()) >= 6:
        #             available = available.replace(c, "")
        #     column = random.choice(available)
        #     history += column if lower_turn else column.upper()
        #     lower_turn = not lower_turn
        # return history

    @staticmethod
    def get_minmax_game_history(difficulty=2):
        game = Connect4Game()
        player = MinMaxPlayer(3 - game.get_turn())
        while game.get_win() is None:
            placement = player.choose_action(game, difficulty)
            if placement is not None:
                game.place(placement)
        return game.history

    @classmethod
    def reproduce(cls, parents: Collection[CombinatorialPlayer, CombinatorialPlayer]):
        parent_a, parent_b = parents
        assert parent_a.nb_chromosomes == parent_b.nb_chromosomes  # Zoophilia is forbidden by God
        nb_chromosomes = parent_a.nb_chromosomes
        child_chromosomes = list(np.random.choice([0, 1], size=nb_chromosomes, replace=True))
        for i, ch_chromo in enumerate(child_chromosomes):
            child_chromosomes[i] = parent_a.chromosomes[i] if ch_chromo == 0 else parent_b.chromosomes[i]
        return [cls(nb_chromosomes, chromosomes=child_chromosomes)]

    def __init__(self, nb_chromosomes, player_turn_id=random.randint(1,2), chromosomes=None):
        super().__init__(player_turn_id)
        self.nb_chromosomes = nb_chromosomes
        if chromosomes is None:
            chromosomes = [CombinatorialPlayer.get_minmax_game_history() for _ in range(nb_chromosomes)]
        self.chromosomes = chromosomes

    def choose_action(self, game: Connect4Game) -> int:
        best_substring = ""
        letter = None
        for gh_i in range(len(game.history)):
            for chromo in self.chromosomes:
                if chromo[-1] != str(game.get_turn()):
                    continue
                substring = game.history[gh_i:-2]
                index = chromo.rfind(substring)  # Search from the end
                # If we found the substring and is longer than the previous best
                if index != -1 and len(substring) > len(best_substring):
                    best_substring = substring
                    letter = chromo[index + len(best_substring)].lower()
        # If nothing was found
        if letter is None or game.history.count(letter.lower()) + game.history.count(letter.upper()) >= 6:
            action = random.randint(0, 6)
        else:
            action = ord(letter) - ord("a")
        return action


if __name__ == '__main__':
    # for h in [CombinatorialPlayer.get_random_hypothetical_game_history() for _ in range(10)]:
    #     print(h)
    #     board = Connect4Game.from_history(h)
    #     for col in board.board:
    #         print(col)
    #     print(board.get_win(), board.history)
    #
    # player = [CombinatorialPlayer(5), CombinatorialPlayer(5)]
    # board = Connect4Game.from_history("dAgDeAfFeBaDdCeBeAaAcDbFb")
    # player[0].choose_action(board)
    # new_player = CombinatorialPlayer.reproduce(player)
    # for p in player:
    #     print(p.chromosomes)
    # print(new_player.chromosomes)

    player_a = CombinatorialPlayer(24)
    player_b = CombinatorialPlayer(24)

    player_c = CombinatorialPlayer.reproduce((player_a, player_b))
    history = "BfFaEdBeAgGaDbFgDdEcFaCaGcFcBcBaGgBdDfCeEe"
    board = Connect4Game.from_history(history)
    player_a.choose_action(board)
    player_b.choose_action(board)
    player_c.choose_action(board)
