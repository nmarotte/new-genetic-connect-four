import numpy as np

INPUT_LAYER = 126
OUTPUT_LAYER = 7
INTERMEDIATE_LAYERS = (126, 126)


class NeuralNetwork:
    def __init__(self, n_input=INPUT_LAYER, n_output=OUTPUT_LAYER, n_intermediate=INTERMEDIATE_LAYERS):
        self.weights = []
        layers = [n_input]
        if isinstance(n_intermediate, int):
            layers.append(n_intermediate)
        else:
            layers += list(n_intermediate)
        layers.append(n_output)
        for i in range(len(layers) - 1):
            self.weights.append(np.random.uniform(low=-1.0, high=1.0, size=(layers[i], layers[i + 1])))

        self.nb_layers = len(layers) - 1

    def forwardPass(self, input):
        current_input = input
        for layer in range(self.nb_layers):
            layer_prediction = np.matmul(current_input, self.weights[layer])
            current_input = self.sigmoid(layer_prediction)
        return current_input

    def sigmoid(self, input):
        return 1 / (1 + np.exp(-input))

    def setWeights(self, index, values):
        self.weights[index] = values

    def backpropagation(self):
        pass


class NeuralNetworkPlayer:

    def __init__(self, neural_network = NeuralNetwork()):
        self.neural_network = neural_network
        self.score = 0

    def chooseAction(self, input):
        board = self.transform_board(input)[0]
        prediction = self.neural_network.forwardPass(board)
        prediction = self.checkFull(input, prediction)
        return np.argmax(prediction)

    def addScore(self, value):
        self.score += value

    def resetScore(self):
        self.score = 0

    def getScore(self):
        return self.score

    def checkFull(self, input, prediction):
        for i in range(len(input)):
            if input[i][-1] != 0:
                prediction[0][i] = 0
        return prediction

    def transform_board(self, board):
        matrix = np.zeros((7, 6, 3), dtype=bool)
        column_not_full = np.full(7, dtype=bool, fill_value=False)
        for i, row in enumerate(board):
            for j, case in enumerate(row):
                matrix[i][j][case] = 1
                if j == len(row) - 1 and case == 0:
                    column_not_full[i] = True

        # TODO if genetic layers accepted: change matrix variable to be by default (1,126)
        return np.reshape(matrix, (1, 126)), column_not_full
