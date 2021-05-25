import random

from Players.Player import Player
from game import Connect4Game


class CombinatorialPlayer(Player):
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

    def __init__(self, nb_chromosomes, chromosomes=None):
        super().__init__()
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
        print(f"{best_substring=}, {self.chromosomes[0]=}, {game.history=}, to play : {self.chromosomes[0][best_index+len(best_substring)]}")
        print(best_substring, self.chromosomes[0], game.history, best_index)


if __name__ == '__main__':
    # for h in [CombinatorialPlayer.get_random_hypothetical_game_history() for _ in range(10)]:
    #     print(h)
    #     board = Connect4Game.from_history(h)
    #     for col in board.board:
    #         print(col)
    #     print(board.get_win(), board.history)

    player = CombinatorialPlayer(1)
    board = Connect4Game.from_history("dAgDeAfFeBaDdCeBeAaAcDbFb")
    player.choose_action(board)
