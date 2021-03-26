import numpy as np


def transform_board(board):
    matrix = np.zeros((7, 6, 3), dtype=bool)
    column_not_full = np.full(7, dtype=bool, fill_value=False)
    for i, row in enumerate(board):
        for j, case in enumerate(row):
            matrix[i][j][case] = 1
            if j == len(row) - 1 and case == 0:
                column_not_full[i] = True

    return matrix, column_not_full
