import numpy as np

loc = 0
scale = 0.5


def construct_hidden_layers(neuron_count_per_layer: list):
    res = []
    for i in range(len(neuron_count_per_layer)-1):
        layer = np.random.normal(loc, scale, size=(neuron_count_per_layer[i], neuron_count_per_layer[i+1]))
        res.append(layer)
    return res


class Agent:
    def __init__(self, neuron_count_per_layer: list):
        self.in_layer = np.random.normal(loc, scale, size=(126, neuron_count_per_layer[0]))
        self.out_layer = np.random.normal(loc, scale, size=(neuron_count_per_layer[-1], 0))
        self.hidden_layers = construct_hidden_layers(neuron_count_per_layer)

    def print_layers_dimensions(self):
        print(f"Input layer : {self.in_layer.shape}")
        for i, layer in enumerate(self.hidden_layers):
            print(f"Hidden layer {i} : {layer.shape}")
        print(f"Output layer : {self.out_layer.shape}")


if __name__ == '__main__':
    agent = Agent([10,15,13,7])
    agent.print_layers_dimensions()