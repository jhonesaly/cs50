"""
Tic Tac Toe Player
"""

import math
import copy

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
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

def print_board(board):
    for i, row in enumerate(board):
        # Convert None to an empty space for console display
        display_row = [cell if cell is not None else " " for cell in row]

        # Print the row with vertical separators
        print(f" {display_row[0]} | {display_row[1]} | {display_row[2]} ")

        # Print the horizontal divider line (except after the last row)
        if i < 2:
            print("-----------")


def print_board_list(boards):
    if not boards:
        return

    num_boards = len(boards)

    for row_idx in range(3):
        row_strs = []
        for board in boards:
            display_row = [cell if cell is not None else " " for cell in board[row_idx]]
            row_strs.append(f" {display_row[0]} | {display_row[1]} | {display_row[2]} ")

        # Join corresponding rows of each board with spacing
        print("   ".join(row_strs))

        # Print horizontal dividers for all boards (except after last row)
        if row_idx < 2:
            print("   ".join(["-----------"] * num_boards))

if __name__ == "__main__":
    board_list = []
    board1 = initial_state()
    board2 = copy.deepcopy(board1)
    board_list.append(board1)
    board_list.append(board2)
    print_board_list(board_list)
