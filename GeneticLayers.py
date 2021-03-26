import numpy as np

loc = 0
scale = 0.5
INPUT_SHAPE = 7 * 6 * 3
OUTPUT_SHAPE = 7
MIN_HIDDEN_LAYERS = 0
MAX_HIDDEN_LAYERS = 10
MIN_SHAPE = 7
MAX_SHAPE = 126

nb_agents_spawned = 0


def new_index():
    global nb_agents_spawned
    nb_agents_spawned += 1
    return nb_agents_spawned


def random_nb_layers():
    return np.random.randint(MIN_HIDDEN_LAYERS, MAX_HIDDEN_LAYERS)


def random_layer_shape():
    return np.random.randint(MIN_SHAPE, MAX_SHAPE)


def random_normal_weights(in_shape, out_shape):
    return np.random.normal(loc, scale, size=(in_shape, out_shape))


def construct_hidden_layers(shapes: list):
    return [random_normal_weights(shapes[i], shapes[i + 1]) for i in range(len(shapes) - 1)]


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
        self.index = index
        self.moves = []

    def get_choice(self, board):
        matrix, column_not_full = transform_board(board)

    def print_layers_dimensions(self):
        print("Agent")
        for i, layer in enumerate(self.layers):
            print(f"Layer {i} : {layer.shape}")


if __name__ == '__main__':
    main_agents = [Agent.spawn_agent() for _ in range(10)]
    for main_agent in main_agents:
        main_agent.print_layers_dimensions()
