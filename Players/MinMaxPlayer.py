import random

from Players.Player import Player
import numpy as np

from game import Connect4Game


class MinMaxPlayer(Player):
    def __init__(self, player_turn_id=None):
        super().__init__(player_turn_id)

    def drop_token(self, game: Connect4Game, column_number, player_id, log_moves):
        """
        Make the player drop his token into the given column
        :param game:
        :param player_id:
        :param column_number:
        :param log_moves:
        :return: None
        """
        for i, token in enumerate(game.board[column_number]):
            if token == 0:
                game.board[column_number][i] = player_id
                break  # Exits

        if log_moves:
            self.last_moves.append(column_number)

    def undo_drop_token(self, game: Connect4Game):
        move = self.last_moves.pop()
        try:
            last_token_dropped_index = game.board[move].index(0)  # Element if column is not full
        except ValueError:
            last_token_dropped_index = len(game.board[move]) - 1  # Last element if column is full
        game.board[move][last_token_dropped_index] = 0

    def choose_action(self, game):
        """
        Algorithme AI
        """
        return self.min_max_search(game)[0]

    def min_max_search(self, game, depth=2, maxi=True) -> tuple[int, int]:
        if depth == 0:
            return -1, 0
        best_score = -float('inf') if maxi else float('inf')
        player_id = self.player_turn_id if maxi else 1 if self.player_turn_id == 2 else 2  # current player if max, else opposite

        best_move = []
        moves_possible = game.get_possible_moves()
        for move in moves_possible:
            self.drop_token(game, move, player_id, log_moves=True)  # Puts token
            try:
                pos = move, game.board[move].index(0)
            except ValueError:  # Happens when no 0 in the column
                pos = move, -1
            winner = game.check_win(pos)  # we suppose that the first time it's going to be empty
            if winner is None:  # No winner yet
                score = self.min_max_search(game, depth - 1, not maxi)[1]  # Recursive
            else:
                score = 1 if winner == self.player_turn_id else -1  # todo behavior for draw is same as losing

            self.undo_drop_token(game)  # Remove token

            if score > best_score:
                if maxi:
                    if score == 1:
                        return move, score
                    best_score = score
                    best_move = [(move, score)]
            elif score < best_score:
                if not maxi:
                    if score == -1:
                        return move, score
                    best_score = score
                    best_move = [(move, score)]
            else:
                best_move.append((move, score))

        return random.choice(best_move)
