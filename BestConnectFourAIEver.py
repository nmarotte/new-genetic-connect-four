import random
import numpy as np

import pygame

from game import Connect4Game, Connect4Viewer, SQUARE_SIZE

nb_neurons_first_layer = np.zeros((6, 7), dtype=np.float64)  # 7 * 6 nb rows * nb columns
nb_neurons_output_layer = np.zeros(7, dtype=np.float64)


class TriGiNa:
    def __init__(self):
        self.shape = (7, 7, 6)
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
        board = np.array(board)
        print(board.shape, self.connexions[0].shape)
        res = np.unravel_index(np.argmax(self.connexions, axis=None), self.shape)[0]
        return res


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
    players = [TriGiNa() for _ in range(nb_agents)]

    for i in range(10):
        for j in range(i + 1, 10):
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

            if winner != 0:
                players[game.get_win() - 1].score += 1  # adds 1 to the winner
            game.reset_game()

    pygame.quit()
