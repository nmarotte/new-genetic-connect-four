import progressbar
import numpy as np
import pygame

from Players.CombinatorialPlayer import CombinatorialPlayer
from Players.NeuralNetworkPlayer import NeuralNetworkPlayer, MinMaxPlayer
from game import Connect4Game, SQUARE_SIZE, Connect4Viewer


class Generation:
    def __init__(self, nb_players, nb_generations, nb_games, difficulty=2):
        self.nb_players = nb_players
        self.nb_generations = nb_generations
        self.nb_games = nb_games
        self.difficulty = difficulty
        self.players = [CombinatorialPlayer(24) for _ in range(self.nb_players)]
        self.tournament()

    def tournament(self):
        # Progress bar
        bar = progressbar.ProgressBar(max_value=self.nb_generations)
        bar.start()
        for generation in range(self.nb_generations):
            # compute the fitness of the current generation
            fitness = self.fitness()
            new_gen = np.zeros_like(self.players)  # Empty generation
            # Add 50 % of the previous generation
            for i in range(len(self.players) // 4):
                parents = np.random.choice(self.players, size=2, replace=False, p=fitness)
                children = CombinatorialPlayer.reproduce(parents)
                new_gen[i:i + len(children)] = children
            new_gen[np.where(new_gen == 0)[0][0]] = self.players[np.argmax(fitness)]
            survivors = np.random.choice(self.players, size=len(np.where(new_gen == 0)[0]), replace=False, p=fitness)
            new_gen[np.where(new_gen == 0)[0]] = survivors

            bar.update(generation)

    def tournament_new(self):
        # Progress bar
        bar = progressbar.ProgressBar(max_value=self.nb_players * self.nb_generations)
        bar.start()
        for generation in range(self.nb_players * self.nb_generations):
            player_a, player_b = np.random.choice(self.players, replace=False, size=2)
            winner = player_a.play_against(player_b)
            self.players.remove(player_b if winner == player_a.player_turn_id else player_a)
            self.players.append(CombinatorialPlayer(24))

            bar.update(generation)

    def fitness(self):
        """
        Compute the fitness of each player of the generation
        :return:
        """
        scores = np.array([p.compute_fitness() for p in self.players])
        scores_2 = np.array([10 if p.play_against(p2) == p.player_turn_id else 0 for p, p2 in
                             zip(self.players, np.random.choice(self.players, size=len(self.players)))])
        scores = scores + scores_2
        return scores / sum(scores)  # makes the total equals to 1


if __name__ == '__main__':
    MinMaxPlayer.difficulty = 2
    gen = Generation(20, 100, 1)
    best_player = None
    max_fitness = 0
    for player in gen.players:
        fitness = player.compute_fitness()
        if fitness > max_fitness:
            max_fitness = fitness
            best_player = player
    player = best_player
    print(max_fitness)
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
                    player_a_choice = player.choose_action(game)
                    game.place(player_a_choice)
                else:
                    game.reset_game()
