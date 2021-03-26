import time

import numpy as np

from game import Connect4Game
from utils import *


class Agent:

    @classmethod
    def spawn_agent(cls):
        nb_layers = random_nb_layers()
        shapes = [INPUT_SHAPE]
        shapes += [random_layer_shape() for _ in range(nb_layers)]
        shapes += [OUTPUT_SHAPE]
        return cls(shapes, new_index())

    @classmethod
    def mix_agents(cls, agents: list):
        pass

    def __init__(self, shapes: list, index: int):
        self.layers = construct_hidden_layers(shapes)
        self.shapes = shapes
        self.index = index
        self.moves = []  # TODO will store what path was taken from the argmax neuron

    @measure
    def get_choice(self, board):
        # flatten the matrix and get if column is full
        matrix, column_not_full = transform_board(board)
        matrix = np.reshape(matrix, (1, self.shapes[0]))
        transmission = np.matmul(matrix, self.layers[0])
        for i in range(1, len(self.layers)):
            transmission = activation_function(np.matmul(transmission, self.layers[i]))
        transmission = activation_function(np.multiply(column_not_full, transmission))
        return np.argmax(transmission)

    def print_layers_dimensions(self):
        print("Agent")
        for i, layer in enumerate(self.layers):
            print(f"Layer {i} : {layer.shape}")


if __name__ == '__main__':
    main_agents = [Agent.spawn_agent() for _ in range(10)]
    for main_agent in main_agents:
        print(main_agent.index)
    game = Connect4Game()
    game.reset_game()
    print(main_agents[0].get_choice(game.board))
