from __future__ import annotations

import random
from typing import Collection

import numpy as np

from Players.Player import Player
from game import Connect4Game


class CombinatorialPlayer(Player):
    def __str__(self):
        return " ".join(self.chromosomes)

    @staticmethod
    def get_random_hypothetical_game_history():
        lower_turn = bool(random.getrandbits(1))
        history = ""
        for _ in range(6 * 7):
            available = "abcdefg"
            for c in available:
                if history.count(c) + history.count(c.upper()) >= 6:
                    available = available.replace(c, "")
            column = random.choice(available)
            history += column if lower_turn else column.upper()
            lower_turn = not lower_turn
        return history

    @classmethod
    def reproduce(cls, parents: Collection[CombinatorialPlayer, CombinatorialPlayer]):
        parent_a, parent_b = parents
        assert parent_a.nb_chromosomes == parent_b.nb_chromosomes  # Zoophilia is forbidden by God
        nb_chromosomes = parent_a.nb_chromosomes
        child_chromosomes = list(np.random.choice([0, 1], size=nb_chromosomes, replace=True))
        for i, ch_chromo in enumerate(child_chromosomes):
            child_chromosomes[i] = parent_a.chromosomes[i] if ch_chromo == 0 else parent_b.chromosomes[i]
        return cls(nb_chromosomes, child_chromosomes)

    def __init__(self, nb_chromosomes, chromosomes=None):
        super().__init__()
        self.nb_chromosomes = nb_chromosomes
        if chromosomes is None:
            chromosomes = [CombinatorialPlayer.get_random_hypothetical_game_history() for _ in range(nb_chromosomes)]
        self.chromosomes = chromosomes

    def choose_action(self, game: Connect4Game) -> int:
        best_substring = ""
        best_index = -1
        for gh_i in range(len(game.history)):
            for chromo in self.chromosomes:
                substring = game.history[gh_i:]
                index = chromo.rfind(substring)  # Search from the end
                # If we found the substring and is longer than the previous best
                if index != -1 and len(substring) > len(best_substring):
                    best_substring = substring
                    best_index = index
        return ord(self.chromosomes[0][best_index+len(best_substring)].lower()) - ord("a")


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
    print(player_a, player_b, player_c, sep='\n')
