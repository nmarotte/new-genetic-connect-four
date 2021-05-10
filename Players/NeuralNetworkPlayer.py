import random

import numpy as np

from Players.MinMaxPlayer import MinMaxPlayer
from Players.Player import Player
from game import Connect4Game

INPUT_LAYER = 126
INTERMEDIATE_LAYERS = (126, 126)
OUTPUT_LAYER = 7


class NeuralNetworkPlayer(Player):
    def __init__(self, player_turn_id=random.randint(1,2), n_input=INPUT_LAYER, n_output=OUTPUT_LAYER,
                 n_intermediate=INTERMEDIATE_LAYERS):
        super().__init__(player_turn_id)
        self.weights = []
        self.activation_function = lambda x: 1 / (1 + np.exp(-x))  # sigmoid
        layers = [n_input]
        if isinstance(n_intermediate, int):
            layers.append(n_intermediate)
        else:
            layers += list(n_intermediate)
        layers.append(n_output)
        for i in range(len(layers) - 1):
            self.weights.append(np.random.uniform(low=-1.0, high=1.0, size=(layers[i], layers[i + 1])))

        self.nb_layers = len(layers) - 1

    def choose_action(self, game: Connect4Game):
        board = game.transform_board()[0]
        # Get the prediction
        prediction = self.forward_pass(board)
        # Remove full column
        prediction = [0 if game.board[i][-1] != 0 else prediction[0][i] for i in range(len(game.board))]
        return np.argmax(prediction)

    def compute_fitness(self):
        """
        The fitness of one player is computed by making him play 10 times against a MinMaxPlayer
        :return:
        """
        player_score = 1  # Since this will be used for probabilities, no one should have a score of 0
        for i in range(10):
            game = Connect4Game()
            opponent = MinMaxPlayer(player_turn_id=3 - game.get_turn())
            winner = self.play_against(opponent, game)
            if winner == 0:  # Tie
                player_score += 50
            elif winner == self.player_turn_id:  # Won
                player_score += 100
        return player_score

    def forward_pass(self, board):
        current_board = board
        for layer in range(self.nb_layers):
            layer_prediction = np.matmul(current_board, self.weights[layer])
            current_board = self.activation_function(layer_prediction)
        return current_board

    @staticmethod
    def reproduce(parents):
        parent_a, parent_b = parents

        children = np.array([NeuralNetworkPlayer(), NeuralNetworkPlayer()])  # Cannot use np.full otherwise same address
        for i in range(len(parent_a.weights)):
            shape = parent_a.weights[i].shape

            chromosomes1 = parent_a.weights[i].flatten()
            split_point = np.random.randint(0, len(chromosomes1))
            chromosomes2 = parent_b.weights[i].flatten()

            new_chromosomes1 = np.array(
                np.concatenate((chromosomes1[:split_point], chromosomes2[split_point:]))).reshape(shape)
            new_chromosomes2 = np.array(
                np.concatenate((chromosomes2[:split_point], chromosomes1[split_point:]))).reshape(shape)
            children[0].weights[i] = new_chromosomes1
            children[1].weights[i] = new_chromosomes2
        return children

    @staticmethod
    def reproduce_new(parents):
        parent_a, parent_b = parents

        children = [NeuralNetworkPlayer(), NeuralNetworkPlayer()]
        for i in range(len(parent_a.weights)):
            shape = parent_a.weights[i].shape

            chromosomes1 = parent_a.weights[i].flatten()
            chromosomes2 = parent_b.weights[i].flatten()
            choice = np.random.randint(0, 1, size=len(chromosomes1))
            new_chromosomes1 = np.where(choice == 0, chromosomes1, chromosomes2)
            new_chromosomes2 = np.where(choice == 1, chromosomes1, chromosomes2)
            children[0].weights[i] = new_chromosomes1
            children[1].weights[i] = new_chromosomes2
        return children
