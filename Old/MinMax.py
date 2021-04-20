from random import choice


def check_full(board: list[list[int]]) -> list:
    """
    Checks for each column in the board if the column is full or not
    :param board: list of columns containing a number
    :return: list containing all the indices of which the column is not full
    """
    return [i for i, column in enumerate(board) if column[-1] == 0]
    # for i, column in enumerate(board):
    #     if column[-1] == 0:
    #         valid.append(i)
    # return valid


def check_win(board, pos):
    """
    Checks for win/draw from newly added disc
    :param board: the board in which we check
    :param pos: position from which to check the win
    :return: player number if a win occurs, 0 if a draw occurs, None otherwise
    """
    rows = 6
    cols = 7

    i = 0
    while i < 6 and board[pos][i] != 0:
        i += 1

    c = pos
    r = i - 1
    player = board[c][r]

    min_col = max(c - 3, 0)
    max_col = min(c + 3, cols - 1)
    min_row = max(r - 3, 0)
    max_row = min(r + 3, rows - 1)

    # Horizontal check
    count = 0
    for ci in range(min_col, max_col + 1):
        if board[ci][r] == player:
            count += 1
        else:
            count = 0
        if count == 4:
            won = player
            return [won]

    # Vertical check
    count = 0
    for ri in range(min_row, max_row + 1):
        if board[c][ri] == player:
            count += 1
        else:
            count = 0
        if count == 4:
            won = player
            return [won]

    count1 = 0
    count2 = 0
    # Diagonal check
    for i in range(-3, 4):
        # bottom-left -> top-right
        if 0 <= c + i < cols and 0 <= r + i < rows:
            if board[c + i][r + i] == player:
                count1 += 1
            else:
                count1 = 0
            if count1 == 4:
                won = player
                return [won]
        # bottom-right -> top-let
        if 0 <= c + i < cols and 0 <= r - i < rows:
            if board[c + i][r - i] == player:
                count2 += 1
            else:
                count2 = 0
            if count2 == 4:
                won = player
                return [won]

    # Draw check
    if sum([x.count(0) for x in board]) == 0:
        return [1, 2]

    return []


class MinimaxPlayer:
    def __init__(self, player_id, board):
        self.player_id = player_id
        self.board = board
        self.last_moves = []

    def drop_token(self, column_number, player_id, log_moves=False):
        """
        Make the player drop his token into the given column
        :param player_id:
        :param column_number:
        :param log_moves:
        :return: None
        """
        for i, token in enumerate(self.board[column_number]):
            if token == 0:
                self.board[column_number][i] = player_id
                break  # Exits

        # i = 0
        # while self.board[coup][i] != 0:
        #     i += 1
        # self.board[coup][i] = player
        if log_moves:
            self.last_moves.append(column_number)

    def undo_drop_token(self):
        coup = self.last_moves.pop()
        try:
            last_token_dropped_index = self.board[coup].index(0)  # Element if column is not full
        except ValueError:
            last_token_dropped_index = len(self.board[coup])-1  # Last element if column is full
        self.board[coup][last_token_dropped_index] = 0

        # previous = 0
        # current = 1
        # try:
        #     while self.board[coup][previous] == 0 or self.board[coup][current] != 0:
        #         previous += 1
        #         current += 1
        #     self.board[coup][previous] = 0
        # except IndexError:
        #     self.board[coup][-1] = 0

    def chooseAction(self, profondeur=2, maxi=True):
        """
        Algorithme AI
        """
        if profondeur == 0:
            return None, 0
        best_score = -float('inf') if maxi else float('inf')
        player_id = self.player_id if maxi else 1 if self.player_id == 2 else 2  # current player if max, else opposite

        best_move = []
        moves_possible = check_full(self.board)
        for move in moves_possible:
            self.drop_token(move, player_id, log_moves=True)  # Puts token
            winners = check_win(self.board, move)  # we suppose that the first time it's going to be empty
            if len(winners) == 0:  # No winner
                score = self.chooseAction(profondeur - 1, not maxi)[1]  # Recursive
            else:
                winner = winners.pop()
                if winner == self.player_id:
                    score = 1
                else:
                    score = -1
            self.undo_drop_token()  # Remove token

            if score > best_score:
                if maxi:
                    if score == 1:
                        return move, score
                    best_score = score
                    best_move = [(move, score)]
            elif score < best_score:
                if not maxi:
                    if score == -1:
                        return move, score
                    best_score = score
                    best_move = [(move, score)]
            else:
                best_move.append((move, score))

        return choice(best_move)
