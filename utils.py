import numpy as np
from functools import wraps
from time import perf_counter

from Constants import *


def transform_board(board):
    matrix = np.zeros((7, 6, 3), dtype=bool)
    column_not_full = np.full(7, dtype=bool, fill_value=False)
    for i, row in enumerate(board):
        for j, case in enumerate(row):
            matrix[i][j][case] = 1
            if j == len(row) - 1 and case == 0:
                column_not_full[i] = True

    # TODO if genetic layers accepted: change matrix variable to be by default (1,126)
    return matrix, column_not_full


def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end_ = perf_counter() - start
            print(f"Total execution time for function {func.__name__}: {end_} s")

    return _time_it


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def activation_function(x):
    return sigmoid(x)


nb_agents_spawned = 0


def new_index():
    global nb_agents_spawned
    nb_agents_spawned += 1
    return nb_agents_spawned


def random_nb_layers():
    return np.random.randint(MIN_HIDDEN_LAYERS, MAX_HIDDEN_LAYERS + 1)  # exclusive upper bound


def random_layer_shape():
    return np.random.randint(MIN_SHAPE, MAX_SHAPE + 1)  # exclusive upper bound


def random_normal_weights(in_shape, out_shape):
    return np.random.normal(norm_loc, norm_scale, size=(in_shape, out_shape))


def random_exponential_weights(in_shape, out_shape):
    return np.random.exponential(exp_scale, size=(in_shape, out_shape))


def construct_hidden_layers(shapes: list):
    return [random_normal_weights(shapes[i], shapes[i + 1]) for i in range(len(shapes) - 1)]
