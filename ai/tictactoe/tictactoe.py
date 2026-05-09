"""
Tic Tac Toe Player
"""

import math
import copy
import random
import time

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


# New alphabeta function based on minimax, with alpha-beta pruning and depth-based heuristic
def alphabeta(board):
    """
    Returns the optimal action for the current player using alpha-beta pruning.
    Prioritizes faster wins (the lower the depth, the better).
    """
    def ab_rec(board, alpha, beta, maximizing, depth):
        if terminal(board):
            util = utility(board)
            # Heuristic: the sooner you win, the better (depth)
            if util == 1:
                return util * (10 - depth)
            elif util == -1:
                return util * (10 - depth)
            else:
                return 0
        if maximizing:
            value = -float('inf')
            for action in actions(board):
                value = max(value, ab_rec(result(board, action), alpha, beta, False, depth + 1))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for action in actions(board):
                value = min(value, ab_rec(result(board, action), alpha, beta, True, depth + 1))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    if terminal(board):
        return None

    current_player = player(board)
    best_move = None
    if current_player == X:
        best_value = -float('inf')
        for action in actions(board):
            value = ab_rec(result(board, action), -float('inf'), float('inf'), False, 1)
            if value > best_value:
                best_value = value
                best_move = action
    else:
        best_value = float('inf')
        for action in actions(board):
            value = ab_rec(result(board, action), -float('inf'), float('inf'), True, 1)
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


def play_game(ai_func, print_moves=False):
    board = initial_state()
    moves = 0
    while not terminal(board):
        if player(board) == X:
            move = random_move(board)
        else:
            move = ai_func(board)
        board = result(board, move)
        moves += 1
        if print_moves:
            print_board(board)
            print()
    return moves, winner(board)

if __name__ == "__main__":
    num_games = 40
    print("Random (X) vs Minimax (O):")
    minimax_moves = []
    minimax_wins = 0
    start = time.time()
    for _ in range(num_games):
        moves, win = play_game(minimax)
        minimax_moves.append(moves)
        if win == O:
            minimax_wins += 1
    end = time.time()
    minimax_time = end - start
    print(f"Minimax average moves to finish: {sum(minimax_moves)/num_games:.2f}")
    print(f"Minimax wins: {minimax_wins}/{num_games} ({(minimax_wins/num_games)*100:.2f}%)")
    print(f"Total time: {minimax_time:.2f}s\n")

    print("Random (X) vs AlphaBeta (O):")
    alphabeta_moves = []
    alphabeta_wins = 0
    start = time.time()
    for _ in range(num_games):
        moves, win = play_game(alphabeta)
        alphabeta_moves.append(moves)
        if win == O:
            alphabeta_wins += 1
    end = time.time()
    alphabeta_time = end - start
    print(f"AlphaBeta average moves to finish: {sum(alphabeta_moves)/num_games:.2f}")
    print(f"AlphaBeta wins: {alphabeta_wins}/{num_games} ({(alphabeta_wins/num_games)*100:.2f}%)")
    print(f"Total time: {alphabeta_time:.2f}s\n")

    avg_minimax = sum(minimax_moves)/num_games
    avg_alphabeta = sum(alphabeta_moves)/num_games
    if avg_minimax > 0:
        faster_moves_pct = 100 * (avg_minimax - avg_alphabeta) / avg_minimax
        print(f"AlphaBeta is faster by {faster_moves_pct:.2f}% in average moves.")
        if alphabeta_wins > minimax_wins:
            win_diff_pct = 100 * (alphabeta_wins - minimax_wins) / minimax_wins if minimax_wins > 0 else 100.0
            print(f"AlphaBeta wins {win_diff_pct:.2f}% more than Minimax against Random.")
        elif minimax_wins > alphabeta_wins:
            win_diff_pct = 100 * (minimax_wins - alphabeta_wins) / alphabeta_wins if alphabeta_wins > 0 else 100.0
            print(f"Minimax wins {win_diff_pct:.2f}% more than AlphaBeta against Random.")
        else:
            print("AlphaBeta and Minimax have the same win rate against Random.")
    else:
        print("AlphaBeta and Minimax have the same average moves.")

    if minimax_time > 0:
        faster_time_pct = 100 * (minimax_time - alphabeta_time) / minimax_time
        print(f"AlphaBeta is faster by {faster_time_pct:.2f}% in processing time.\n")
    else:
        print("AlphaBeta and Minimax have the same processing time.\n")


    # 20 games: 10 Minimax (X) vs AlphaBeta (O), 10 AlphaBeta (X) vs Minimax (O)
    print("Minimax vs AlphaBeta (alternating who starts):")
    ia_games = 20
    minimax_ia_wins = 0
    alphabeta_ia_wins = 0
    draws = 0
    ia_moves = []
    minimax_time_total = 0.0
    alphabeta_time_total = 0.0
    for i in range(ia_games):
        board = initial_state()
        moves = 0
        # Alternate who is X and who is O
        if i < ia_games // 2:
            # Minimax is X, AlphaBeta is O
            X_func = minimax
            O_func = alphabeta
        else:
            # AlphaBeta is X, Minimax is O
            X_func = alphabeta
            O_func = minimax
        while not terminal(board):
            if player(board) == X:
                t0 = time.time()
                move = X_func(board)
                t1 = time.time()
                if X_func == minimax:
                    minimax_time_total += (t1 - t0)
                else:
                    alphabeta_time_total += (t1 - t0)
            else:
                t0 = time.time()
                move = O_func(board)
                t1 = time.time()
                if O_func == minimax:
                    minimax_time_total += (t1 - t0)
                else:
                    alphabeta_time_total += (t1 - t0)
            board = result(board, move)
            moves += 1
        ia_moves.append(moves)
        win = winner(board)
        # Contabiliza vitórias considerando quem era X e O
        if i < ia_games // 2:
            # Minimax X, AlphaBeta O
            if win == X:
                minimax_ia_wins += 1
            elif win == O:
                alphabeta_ia_wins += 1
            else:
                draws += 1
        else:
            # AlphaBeta X, Minimax O
            if win == X:
                alphabeta_ia_wins += 1
            elif win == O:
                minimax_ia_wins += 1
            else:
                draws += 1
    print(f"Average moves to finish: {sum(ia_moves)/ia_games:.2f}")
    print(f"Minimax wins: {minimax_ia_wins}/{ia_games} ({(minimax_ia_wins/ia_games)*100:.2f}%)")
    print(f"AlphaBeta wins: {alphabeta_ia_wins}/{ia_games} ({(alphabeta_ia_wins/ia_games)*100:.2f}%)")
    print(f"Draws: {draws}/{ia_games} ({(draws/ia_games)*100:.2f}%)")
    print(f"Total Minimax processing time: {minimax_time_total:.2f}s ({(minimax_time_total/(minimax_time_total+alphabeta_time_total)*100 if (minimax_time_total+alphabeta_time_total)>0 else 0):.2f}% of total)")
    print(f"Total AlphaBeta processing time: {alphabeta_time_total:.2f}s ({(alphabeta_time_total/(minimax_time_total+alphabeta_time_total)*100 if (minimax_time_total+alphabeta_time_total)>0 else 0):.2f}% of total)\n")
