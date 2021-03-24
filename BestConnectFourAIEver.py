import random
import numpy as np

import pygame

from game import Connect4Game, Connect4Viewer, SQUARE_SIZE

nb_neurons_first_layer = np.zeros((6, 7), dtype=np.float64)  # 7 * 6 nb rows * nb columns
nb_neurons_output_layer = np.zeros(7, dtype=np.float64)


def transform_board(board):
    matrix = np.zeros((7, 6, 3), dtype=bool)
    for i, row in enumerate(board):
        for j, case in enumerate(row):
            matrix[i][j][case] = 1

    column_not_full = np.full(7, dtype=bool, fill_value=False)
    for i, row in enumerate(matrix):
        if row[-1][0]:  # if case[1] or case[2]
            column_not_full[i] = True

    return matrix, column_not_full


class TriGiNa:
    def __init__(self):
        self.shape = (7, 7, 6, 3)
        self.connexions = np.random.normal(0, 0.05, self.shape)
        self.score = 0

    def activation(self, x):
        return np.exp(-x)

    def update(self):
        pass

    def train(self, n_games=100):
        for _ in range(n_games):
            self.update()

    def get_choice(self, board=None):
        matrix, column_not_full = transform_board(board)
        a, b = np.reshape(matrix, (1, 7 * 6 * 3)), np.reshape(self.connexions, (7 * 6 * 3, 7))
        result = np.matmul(a, b)[0]
        current_max = -np.Infinity
        position = None
        for i, res in enumerate(result):
            if column_not_full[i]:
                if res > current_max:
                    current_max = res
                    position = i
        return position


if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    tgn = TriGiNa()

    game = Connect4Game()
    game.reset_game()

    # view = Connect4Viewer(game=game)
    # view.initialize()

    # human vs ai
    ai_goes_first = bool(random.randint(0, 1))
    nb_placed = 0

    # running = True
    # while running:
    #     if nb_placed % 2 == ai_goes_first:
    #         if game.get_win() is None:  # if it is not won, ai plays
    #             game.place(random.randint(0, 700) // SQUARE_SIZE)  # This is where the AI chooses its play
    #             nb_placed += 1
    #         else:  # Otherwise, skip turn so that the user can see end screen
    #             nb_placed += 1
    #     else:
    #         for i, event in enumerate(pygame.event.get()):
    #             if event.type == pygame.QUIT:
    #                 running = False
    #             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    #                 if game.get_win() is None:
    #                     placement = game.place(pygame.mouse.get_pos()[0] // SQUARE_SIZE)
    #                     if placement is not None:  # Still player's turn if placement fails
    #                         nb_placed += 1
    #                 else:
    #                     game.reset_game()

    # ai vs ai
    nb_agents = 10
    nb_generation = 1000
    players = [TriGiNa() for _ in range(nb_agents)]

    for g in range(nb_generation):
        for i in range(nb_agents):
            for j in range(i + 1, nb_agents):
                game = Connect4Game()
                game.reset_game()

                winner = game.get_win()

                while winner is None:
                    if nb_placed % 2 == ai_goes_first:
                        game.place(players[i].get_choice(game.board))  # This is where the AI chooses its play
                        nb_placed += 1

                    else:
                        game.place(players[j].get_choice(game.board))  # This is where the AI chooses its play
                        nb_placed += 1

                    winner = game.get_win()

                if winner == 1:
                    players[i].score += 1  # adds 1 to the winner
                elif winner == 2:
                    players[j].score += 1
                game.reset_game()

        best_player = players[0]
        for player in players:
            if player.score > best_player.score:
                best_player = player

        if g != nb_generation-1:
            best_player.score = 0
            players = [TriGiNa() for _ in range(nb_agents-1)] + [best_player]

    for player in players:
        print(player.score)
    pygame.quit()
