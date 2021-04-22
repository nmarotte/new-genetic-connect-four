import random

import pygame

from Players.Player import Player
import numpy as np

from game import Connect4Game, Connect4Viewer, SQUARE_SIZE


class MinMaxPlayer(Player):
    difficulty = 2

    def __init__(self, player_turn_id=None):
        super().__init__(player_turn_id)

    def check_win(self, board, pos):
        """
        Checks for win/draw from newly added disc
        :param pos: position from which to check the win
        :return: player number if a win occurs, 0 if a draw occurs, None otherwise
        """
        rows = 6
        cols = 7

        i = 0
        while i < 6 and board[pos][i] != 0:
            i += 1

        c = pos
        r = i - 1
        player = board[c][r]

        min_col = max(c - 3, 0)
        max_col = min(c + 3, cols - 1)
        min_row = max(r - 3, 0)
        max_row = min(r + 3, rows - 1)

        # Horizontal check
        count = 0
        for ci in range(min_col, max_col + 1):
            if board[ci][r] == player:
                count += 1
            else:
                count = 0
            if count == 4:
                won = player
                return [won]

        # Vertical check
        count = 0
        for ri in range(min_row, max_row + 1):
            if board[c][ri] == player:
                count += 1
            else:
                count = 0
            if count == 4:
                won = player
                return [won]

        count1 = 0
        count2 = 0
        # Diagonal check
        for i in range(-3, 4):
            # bottom-left -> top-right
            if 0 <= c + i < cols and 0 <= r + i < rows:
                if board[c + i][r + i] == player:
                    count1 += 1
                else:
                    count1 = 0
                if count1 == 4:
                    won = player
                    return [won]
            # bottom-right -> top-let
            if 0 <= c + i < cols and 0 <= r - i < rows:
                if board[c + i][r - i] == player:
                    count2 += 1
                else:
                    count2 = 0
                if count2 == 4:
                    won = player
                    return [won]

        # Draw check
        if sum([x.count(0) for x in board]) == 0:
            won = 0
            return [1, 2]

        won = []
        return won

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
            last_token_dropped_index = game.board[move].index(0) - 1  # Element if column is not full
        except ValueError:
            last_token_dropped_index = len(game.board[move]) - 1  # Last element if column is full
        game.board[move][last_token_dropped_index] = 0

    def choose_action(self, game):
        """
        Algorithme AI
        """
        return self.min_max_search(game)[0]

    def min_max_search(self, game, depth=None, maxi=True) -> tuple[int, int]:
        # Default depth
        if depth is None:
            depth = MinMaxPlayer.difficulty
        if depth == 0:
            return None, 0
        best_score = -float('inf') if maxi else float('inf')
        player_id = self.player_turn_id if maxi else 1 if self.player_turn_id == 2 else 2  # current player if max, else opposite

        best_move = []
        moves_possible = game.get_possible_moves()

        for move in moves_possible:
            pos = move, game.board[move].index(0) - 1
            self.drop_token(game, move, player_id, log_moves=True)  # Puts token
            winners = self.check_win(game.board, move)  # we suppose that the first time it's going to be empty
            if len(winners) == 0:  # No winner yet
                score = self.min_max_search(game, depth - 1, not maxi)[1]  # Recursive
            else:
                score = 1 if winners.pop() == self.player_turn_id else -1  # todo behavior for draw is same as losing

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


if __name__ == '__main__':
    game = Connect4Game()
    game.reset_game()
    view = Connect4Viewer(game=game)
    view.initialize()
    running = True
    while running:
        player = MinMaxPlayer(3 - game.get_turn())
        for i, event in enumerate(pygame.event.get()):
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if game.get_win() is None:
                    placement = game.place(pygame.mouse.get_pos()[0] // SQUARE_SIZE)
                    if placement is None:  # Still player's turn if placement fails
                        continue
                    if game.get_win() is not None:
                        game.reset_game()
                    player_a_choice = player.choose_action(game)
                    game.place(player_a_choice)
                else:
                    game.reset_game()
