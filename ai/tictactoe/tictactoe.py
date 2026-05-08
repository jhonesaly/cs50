"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    num_x = 0
    num_o = 0

    for i in board:
        for j in i:
            if j == X:
                num_x += 1
            elif j == O:
                num_o += 1
    
    if num_x <= num_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if val == EMPTY:
                possible_actions.add((r, c))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_result = copy.deepcopy(board)
    board_result[action[0]][action[1]] = player(board)
    return board_result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Monta `list_x` e `list_o` coletando coordenadas (linha, coluna) de cada símbolo
    list_x = {(r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == X}
    list_o = {(r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == O}

    winning_combinations = [
        # horizontally
        {(0, 0), (0, 1), (0, 2)},
        {(1, 0), (1, 1), (1, 2)},
        {(2, 0), (2, 1), (2, 2)},
        # vertically
        {(0, 0), (1, 0), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 2), (1, 2), (2, 2)},
        # diagonally
        {(0, 0), (1, 1), (2, 2)},
        {(0, 2), (1, 1), (2, 0)}
    ]

    for combination in winning_combinations:
        if combination.issubset(list_x):
            return X
        if combination.issubset(list_o):
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is already over, there is no move to make
    if terminal(board):
        return None

    current_player = player(board)
    best_move = None

    # The AI explores each possible action to find the one with the best value
    if current_player == X:
        best_value = -float('inf')
        for action in actions(board):
            # X wants to maximize the value returned by get_value
            value = get_value(result(board, action))
            if value > best_value:
                best_value = value
                best_move = action
    else:
        best_value = float('inf')
        for action in actions(board):
            # O wants to minimize the value returned by get_value
            value = get_value(result(board, action))
            if value < best_value:
                best_value = value
                best_move = action

    return best_move


def get_value(board):
    """
    Recursively calculates the utility value of a given board state.
    """
    # Base case: if the game is over, return the score (1, 0, or -1)
    if terminal(board):
        return utility(board)

    curr_player = player(board)
    
    if curr_player == X:
        v = -float('inf')
        for action in actions(board):
            # X plays and seeks the maximum possible outcome
            v = max(v, get_value(result(board, action)))
        return v
    else:
        v = float('inf')
        for action in actions(board):
            # O plays and seeks the minimum possible outcome
            v = min(v, get_value(result(board, action)))
        return v


def random_move(board):
    """
    Returns a random action for the current player on the board.
    """
    possible_actions = actions(board)
    return random.choice(list(possible_actions))


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
    board = initial_state()

    while terminal(board) == False:
        print_board(board)
        print(f"Player {player(board)}'s turn.")
        if player(board) == X:
            player_move = input("Enter your move as 'row,col': ")
            row, col = map(int, player_move.split(','))
            board = result(board, (row, col))
        else:
            ai_move = minimax(board)
            board = result(board, ai_move)
    print("Game over.")
    print_board(board)
    print(f"Winner: {winner(board)}")
