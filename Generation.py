import progressbar
import numpy as np

from NeuralNetworkPlayer import NeuralNetworkPlayer


class Generation:
    def __init__(self, nb_players, nb_generations, nb_games):
        self.nb_players = nb_players
        self.nb_generations = nb_generations
        self.nb_games = nb_games
        self.players = [NeuralNetworkPlayer() for _ in range(self.nb_players)]
        self.tournament()

    def tournament(self):
        # Progress bar
        bar = progressbar.ProgressBar(maxval=self.nb_generations)
        for generation in range(self.nb_generations):
            # compute the fitness of the current generation
            fitness = self.fitness()
            new_gen = np.zeros_like(self.players)  # Empty generation
            # Add 50 % of the previous generation
            survivors = np.random.choice(self.players, size=len(self.players) // 2, replace=False, p=fitness)
            new_gen[0:len(survivors)] = survivors
            for i in np.where(new_gen == 0)[0]:
                parents = np.random.choice(self.players, size=2, replace=False, p=fitness)
                children = NeuralNetworkPlayer.reproduce(parents)
                new_gen[i:i+len(children)] = children
            bar.next()

    def fitness(self):
        """
        Compute the fitness of each player of the generation by making him play
        10 times against a MinMax player
        :return:
        """
        scores = np.zeros(len(self.players))
        for i, player in enumerate(self.players):
            scores[i] = player.compute_fitness()
        return scores/sum(scores)