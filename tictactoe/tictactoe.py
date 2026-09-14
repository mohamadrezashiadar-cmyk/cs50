"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] != EMPTY:
        raise Exception("Invalid action: cell is already occupied")

    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []

    # Rows and columns
    for i in range(3):
        lines.append([board[i][0], board[i][1], board[i][2]])
        lines.append([board[0][i], board[1][i], board[2][i]])

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] is not EMPTY and line[0] == line[1] == line[2]:
            return line[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    return all(cell != EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def max_value(board, alpha, beta):
    """
    Helper for minimax: returns the maximum utility achievable from
    this board state, assuming optimal play by both sides.
    """
    if terminal(board):
        return utility(board), None

    value = -math.inf
    best_action = None

    for action in actions(board):
        min_val, _ = min_value(result(board, action), alpha, beta)
        if min_val > value:
            value = min_val
            best_action = action
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return value, best_action


def min_value(board, alpha, beta):
    """
    Helper for minimax: returns the minimum utility achievable from
    this board state, assuming optimal play by both sides.
    """
    if terminal(board):
        return utility(board), None

    value = math.inf
    best_action = None

    for action in actions(board):
        max_val, _ = max_value(result(board, action), alpha, beta)
        if max_val < value:
            value = max_val
            best_action = action
        beta = min(beta, value)
        if alpha >= beta:
            break

    return value, best_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        _, action = max_value(board, -math.inf, math.inf)
    else:
        _, action = min_value(board, -math.inf, math.inf)

    return action
