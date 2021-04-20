import numpy as np

import pygame

from Old.game import Connect4Game, Connect4Viewer, SQUARE_SIZE
from utils import transform_board

nb_neurons_first_layer = np.zeros((6, 7), dtype=np.float64)  # 7 * 6 nb rows * nb columns
nb_neurons_output_layer = np.zeros(7, dtype=np.float64)


# def transform_board(board):
#     matrix = np.zeros((7, 6, 3), dtype=bool)
#     for i, row in enumerate(board):
#         for j, case in enumerate(row):
#             matrix[i][j][case] = 1
#
#     column_not_full = np.full(7, dtype=bool, fill_value=False)
#     for i, row in enumerate(matrix):
#         if row[-1][0]:  # if case[1] or case[2]
#             column_not_full[i] = True
#
#     return matrix, column_not_full


class TriGiNa:
    def __init__(self, oldest_gen):
        self.in_shape = 7*6*3
        self.mid_shape = 10
        self.out_shape = 7

        self.connexions_in_mid = np.random.normal(0, 1, (self.in_shape, self.mid_shape))
        self.connexions_mid_out = np.random.normal(0, 1, (self.mid_shape, self.out_shape))

        self.score = 0
        self.nb_played = 0
        self.index = oldest_gen

    def get_choice(self, board=None):
        matrix, column_not_full = transform_board(board)
        first = np.matmul(np.reshape(matrix, (1, 126)), self.connexions_in_mid)[0]
        out = np.matmul(first, self.connexions_mid_out)
        current_max = -np.Infinity
        position = None
        for i, res in enumerate(out):
            if column_not_full[i]:
                if res > current_max:
                    current_max = res
                    position = i
        return position

    def make_baby(self, agent):
        new_agent = TriGiNa(agent.index)
        new_agent.connexions_in_mid = (self.connexions_in_mid + agent.connexions_in_mid) / 2
        new_agent.connexions_mid_out = (self.connexions_mid_out + agent.connexions_mid_out) / 2
        new_agent.index = min(self.index, agent.index)
        return new_agent

    def __lt__(self, other):
        return self.score/self.nb_played < other.score/other.nb_played

    def __eq__(self, other):
        return self.score/self.nb_played == other.score/other.nb_played

    def __gt__(self, other):
        return self.score/self.nb_played > other.score/other.nb_played


agents_count = 0


def mix_population(players, current_gen):
    nb_agents = len(players)
    new_players = [players[0]]  # keep the best player

    # mix depending on score
    nb_to_mix = (nb_agents-1)//2
    players_weight = np.array([p.score for p in players])
    players_weight = players_weight / sum(players_weight)
    for i in range(nb_to_mix):
        player_a, player_b = np.random.choice(players, size=2, replace=False, p=players_weight)
        new_players.append(player_a.make_baby(player_b))

    while len(new_players) < nb_agents:
        new_players.append(TriGiNa(current_gen))
    return new_players


if __name__ == '__main__':
    np.set_printoptions(suppress=True)

    game = Connect4Game()
    game.reset_game()

    # ai vs ai
    main_nb_agents = 30
    nb_generation = 1000
    main_players = [TriGiNa(agents_count + i) for i in range(main_nb_agents)]
    agents_count += main_nb_agents

    for g in range(nb_generation):
        print(f"generation {g}")
        for i in range(main_nb_agents):
            for j in range(i + 1, main_nb_agents):
                game = Connect4Game()
                game.reset_game()

                winner = game.get_win()

                while winner is None:
                    player_a_choice = main_players[i].get_choice(game.board)
                    game.place(player_a_choice)
                    winner = game.get_win()
                    if winner is not None:
                        break
                    player_b_choice = main_players[j].get_choice(game.board)
                    game.place(player_b_choice)
                    winner = game.get_win()

                if winner == 1:
                    main_players[i].score += 1  # adds 1 to the winner
                elif winner == 2:
                    main_players[j].score += 1

                game.reset_game()
                main_players[i].nb_played += 1
                main_players[j].nb_played += 1

        main_players.sort()

        if g != nb_generation - 1:
            main_players = mix_population(main_players, g)

        else:
            print(main_players[-1].score, main_players[-1].nb_played)
            game = Connect4Game()
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
                            player_a_choice = main_players[-1].get_choice(game.board)
                            game.place(player_a_choice)
                        else:
                            game.reset_game()

    main_players.sort()
    for player in main_players:
        print(f"Player {player.index} got score {player.score/player.nb_played} on {player.nb_played} games")
    pygame.quit()
