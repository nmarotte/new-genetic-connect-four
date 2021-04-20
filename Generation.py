import progressbar
import numpy as np

from Players.NeuralNetworkPlayer import NeuralNetworkPlayer


class Generation:
    def __init__(self, nb_players, nb_generations, nb_games):
        self.nb_players = nb_players
        self.nb_generations = nb_generations
        self.nb_games = nb_games
        self.players = [NeuralNetworkPlayer() for _ in range(self.nb_players)]
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
            survivors = np.random.choice(self.players, size=len(self.players) // 2, replace=False, p=fitness)
            new_gen[0:len(survivors)] = survivors
            for i in np.where(new_gen == 0)[0]:
                parents = np.random.choice(self.players, size=2, replace=False, p=fitness)
                children = NeuralNetworkPlayer.reproduce(parents)
                if i+len(children) < self.nb_players:
                    new_gen[i:i+len(children)] = children
                else:
                    new_gen[i:i+len(children)-1] = children[0]
                    # todo find a better alternative to when we only need
                    #  one more child
            bar.update(generation)

    def fitness(self):
        """
        Compute the fitness of each player of the generation
        :return:
        """
        scores = np.zeros(len(self.players))
        for i, player in enumerate(self.players):
            scores[i] = player.compute_fitness()
        return scores/sum(scores)  # makes the total equals to 1


if __name__ == '__main__':
    gen = Generation(20, 100, 1)