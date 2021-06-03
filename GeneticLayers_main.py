from pprint import pprint

import GeneticFunctions
from utils import *


class Agent:
    learning_rate = 0.001

    @classmethod
    def spawn_agent(cls):
        nb_layers = random_nb_layers()
        shapes = [INPUT_SHAPE]
        shapes += [random_layer_shape() for _ in range(nb_layers)]
        shapes += [OUTPUT_SHAPE]
        return cls(shapes, new_index())

    @classmethod
    def mix_agents(cls, agents: list):
        return cls(GeneticFunctions.mix_shapes(agents), new_index())

    def __init__(self, shapes: list, index: int):
        self.layers = construct_hidden_layers(shapes)
        self.shapes = shapes
        self.index = index
        self.moves = []

        self.score = 0
        self.nb_played = 0
        self.moves_of_game = 0

    def __str__(self):
        return f"Agent {self.index} played {self.nb_played} times and won {self.score} times " \
               f"({round(100 * self.score / self.nb_played)}%). Shapes = {self.shapes}"

    def backpropagation(self):
        for i in range(len(self.moves) - 1, -1, -1):
            choice_path = self.moves[i]
            for j in range(len(choice_path) - 1, -1, -1):
                move = choice_path[j]
                delta = move - self.layers[j]
                self.layers[j] += delta * Agent.learning_rate

    def get_choice(self, board, show=False):
        # flatten the matrix and get if column is full
        X, column_not_full = transform_board(board)
        X = np.reshape(X, (1, self.shapes[0]))[0]
        if show:
            print(self.layers[0])
        P = activation_function(np.matmul(X, self.layers[0]))
        choice_path = []
        for i in range(1, len(self.layers)):
            choice_path.append(np.zeros_like(P))
            choice_path[-1][np.argmax(choice_path[-1])] = 1
            P = activation_function(np.matmul(P, self.layers[i]))
        P = np.where(column_not_full, P, 0)
        choice_path.append(np.zeros_like(P))
        choice_path[-1] = np.where(column_not_full, choice_path[-1], 0)
        choice_path[-1][np.argmax(choice_path[-1])] = 1
        self.moves.append(choice_path)
        if show:
            print(P)
        self.moves_of_game += 1
        return np.argmax(P)

    def print_layers_dimensions(self):
        print("Agent")
        for i, layer in enumerate(self.layers):
            print(f"Layer {i} : {layer.shape}")

    @classmethod
    def spawn_agents(cls, n: int):
        return [Agent.spawn_agent() for _ in range(n)]


if __name__ == '__main__':
    nb_agents = 10
    nb_generations = 10
    print(f"Population of {nb_agents} agents over {nb_generations} generations with {MIN_HIDDEN_LAYERS} to "
          f"{MAX_HIDDEN_LAYERS} layers of {MIN_SHAPE} to {MAX_SHAPE} neurons each")
    for g in range(nb_generations):
        print(f"Generation {g}")
        main_agents = Agent.spawn_agents(nb_agents)
        sorted_main_agents = GeneticFunctions.generation_tournament(main_agents)
        print(f"Best agent of generation : {main_agents[0]}")

    GeneticFunctions.play_human(main_agents[0])

"""
[[0.96130386 0.97995674 0.67847989 0.25086593 0.22262141 0.01571971
  0.13218699 0.80409218 0.4328295  0.99613116 0.38902272 0.48958583
  0.7218514  0.00643753 0.92256629 0.76380222 0.54021552 0.15611889
  0.51857252 0.80991296 0.07765295 0.97772937 0.17846834 0.76733324
  0.83033305 0.9448455  0.50332792 0.34849674 0.84285387 0.28887956
  0.60616082 0.74470905 0.31204136 0.0137449  0.35567099 0.08378544
  0.95914705 0.1578767  0.04047591 0.45544277 0.0825991  0.19558838
  0.47100401 0.4127067  0.99169361 0.93284896 0.87155157 0.17146086
  0.81671396 0.47873407 0.34233391 0.26611677 0.99614638 0.99996048
  0.41643889 0.28580913 0.95551138 0.05919173 0.13183377 0.77439268
  0.00998787 0.06337673 0.87468657 0.6382208  0.07549732 0.02591249
  0.88526476 0.35642603 0.02600139 0.98598893 0.99615541 0.13521672
  0.56570181 0.43052001]]


"""
