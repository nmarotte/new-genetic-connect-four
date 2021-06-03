from __future__ import annotations

import random
from typing import Collection

import Players.Player as Player
from game import Connect4Game
from utils import get_random_hypothetical_game_history, get_minmax_game_history


class CombinatorialPlayer(Player.Player):
    def __str__(self):
        return " ".join(self.chromosomes)

    @classmethod
    def with_random_chromosomes(cls, nb_chromosomes):
        chromosomes = [get_random_hypothetical_game_history() for _ in nb_chromosomes]
        return cls(nb_chromosomes, chromosomes=chromosomes)

    @classmethod
    def with_minmax_chromosomes(cls, nb_chromosomes, difficulty: int = 2):
        chromosomes = [get_minmax_game_history(difficulty) for _ in nb_chromosomes]
        return cls(nb_chromosomes, chromosomes=chromosomes)

    @classmethod
    def reproduce(cls, parents: Collection[CombinatorialPlayer, CombinatorialPlayer]):
        parent_a, parent_b = parents
        assert parent_a.nb_chromosomes == parent_b.nb_chromosomes  # Cannot breed if the number of chromosome is different, for obvious reasons
        nb_chromosomes = parent_a.nb_chromosomes
        # gets chromosomes from the parent
        child_chromosomes = random.choices(parent_a.chromosomes, k=nb_chromosomes//2) + random.choices(parent_b.chromosomes, k=nb_chromosomes//2)
        # Mutate some chromosomes at random to introduce maybe some good chromosomes
        for _ in range(nb_chromosomes//4):
            child_chromosomes[random.randrange(0, len(child_chromosomes))] = get_minmax_game_history()
        return [cls(nb_chromosomes, chromosomes=child_chromosomes)]

    def __init__(self, nb_chromosomes, player_turn_id=random.randint(1,2), chromosomes=None):
        super().__init__(player_turn_id)
        self.nb_chromosomes = nb_chromosomes
        if chromosomes is None:
            chromosomes = [get_minmax_game_history() for _ in range(nb_chromosomes)]
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
                # and that it is not the game outcome
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

    player_c = CombinatorialPlayer.reproduce((player_a, player_b))[0]
    history = "BfFaEdBeAgGaDbFgDdEcFaCaGcFcBcBaGgBdDfCeEe"
    board = Connect4Game.from_history(history)
    player_a.choose_action(board)
    player_b.choose_action(board)
    player_c.choose_action(board)
