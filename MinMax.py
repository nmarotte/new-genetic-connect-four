from random import choice

import pygame

from game import Connect4Game, Connect4Viewer, SQUARE_SIZE


class MinimaxPlayer:

    def __init__(self, player_id, board):
        """
        Initialisation du joueur
        """
        self.player = player_id
        self.board = board
        self.last = []

    def checkFull(self, input):
        valid = []
        for i in range(len(input)):
            if input[i][-1] == 0:
                valid.append(i)
        return valid

    def act(self, coup, player, simulate = False):
        i = 0
        while self.board[coup][i] != 0:
            i += 1
        self.board[coup][i] = player
        if simulate:
            self.last.append(coup)

    def undo(self):
        coup = self.last.pop()
        previous = 0
        current = 1
        try:
            while not (self.board[coup][previous] != 0 and self.board[coup][current] == 0):
                previous += 1
                current += 1
            self.board[coup][previous] = 0
        except IndexError:
            self.board[coup][-1] = 0


    def chooseAction(self, profondeur=2, maxi=True):
        """
        Algorithme AI
        """
        if profondeur == 0:
            return (None, 0)
        if maxi:
            meilleurscore = -float('inf')
            player = self.player
        else:
            meilleurscore = float('inf')
            player = 3 - self.player

        meilleurcoup = []
        coups = self.checkFull(self.board)
        for coup in coups:
            self.act(coup, player, simulate=True)
            winners = self.check_win(self.board, coup)  # we suppose that the first time it's going to be empty
            if len(winners) == 0:
                score = self.chooseAction(profondeur - 1, not maxi)[1]
            else:
                winner = winners.pop()
                if winner == self.player:
                    score = 1
                else:
                    score = -1
            self.undo()

            if score > meilleurscore:
                if maxi:
                    if score == 1:
                        return (coup, score)
                    meilleurscore = score
                    meilleurcoup = [(coup, score)]
            elif score < meilleurscore:
                if not maxi:
                    if score == -1:
                        return (coup, score)
                    meilleurscore = score
                    meilleurcoup = [(coup, score)]
            else:
                meilleurcoup.append((coup, score))

        return choice(meilleurcoup)

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

if __name__ == '__main__':
    game = Connect4Game()
    player = MinimaxPlayer(2, game.board)
    game.reset_game()
    view = Connect4Viewer(game=game)
    view.initialize()
    running = True
    while running:
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
                    player_a_choice = player.chooseAction(profondeur=4)
                    print(player_a_choice)
                    game.place(player_a_choice[0])
                else:
                    game.reset_game()