import numpy as np

loc = 0
scale = 0.5


def construct_hidden_layers(shapes: list):
    return [np.random.normal(loc, scale, size=(shapes[i], shapes[i + 1])) for i in range(len(shapes) - 1)]


class Agent:
    def __init__(self, shapes: list):
        self.layers = construct_hidden_layers(shapes)

    def print_layers_dimensions(self):
        for i, layer in enumerate(self.layers):
            print(f"Layer {i} : {layer.shape}")


if __name__ == '__main__':
    agent = Agent([10, 3, 10, 15, 1, 18, 7])
    agent.print_layers_dimensions()
