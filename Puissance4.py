# %% Puissance 4 : Affrontement entre IA 
import math
import random
import copy
import time

ROWS = 6
COLUMNS = 12
ALIGN = 4

def initial_state():
    return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print('|' + '|'.join(['.' if c == 0 else ('X' if c == 1 else 'O') for c in row]) + '|')
    print(' ' + ' '.join(map(str, range(COLUMNS))))

def actions(board):
    return [c for c in range(COLUMNS) if board[0][c] == 0]

def result(board, col, player):
    new_board = copy.deepcopy(board)
    for row in reversed(range(ROWS)):
        if new_board[row][col] == 0:
            new_board[row][col] = player
            return new_board
    return board  # au cas ou la colonne est pleine

def is_terminal(board):
    return check_win(board, 1) or check_win(board, -1) or all(board[0][c] != 0 for c in range(COLUMNS))

def check_win(board, player):
    # Horizontale
    for r in range(ROWS):
        for c in range(COLUMNS - ALIGN + 1):
            if all(board[r][c + i] == player for i in range(ALIGN)):
                return True
    # Verticale
    for r in range(ROWS - ALIGN + 1):
        for c in range(COLUMNS):
            if all(board[r + i][c] == player for i in range(ALIGN)):
                return True
    # Diagonale /
    for r in range(ALIGN - 1, ROWS):
        for c in range(COLUMNS - ALIGN + 1):
            if all(board[r - i][c + i] == player for i in range(ALIGN)):
                return True
    # Diagonale \
    for r in range(ROWS - ALIGN + 1):
        for c in range(COLUMNS - ALIGN + 1):
            if all(board[r + i][c + i] == player for i in range(ALIGN)):
                return True
    return False

def evaluate(board, player):
    opponent = -player
    return score_position(board, player) - score_position(board, opponent)

def score_position(board, player):
    score = 0
    # Score horizontal
    for row in board:
        for c in range(COLUMNS - 3):
            window = row[c:c+4]
            score += evaluate_window(window, player)
    # Score vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window, player)
    # Score diagonale \
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)
    # Score diagonale /
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)
    return score

def evaluate_window(window, player):
    score = 0
    opp = -player
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 4
    return score

def minimax(board, depth, alpha, beta, maximizingPlayer, player, start_time, time_limit=9.5):
    if is_terminal(board) or depth == 0 or (time.time() - start_time > time_limit):
        if check_win(board, player):
            return (None, 100000)
        elif check_win(board, -player):
            return (None, -100000)
        elif is_terminal(board):
            return (None, 0)
        else:
            return (None, evaluate(board, player))
    
    valid_locations = actions(board)
    best_col = random.choice(valid_locations)

    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            child = result(board, col, player)
            _, score = minimax(child, depth-1, alpha, beta, False, player, start_time)
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        for col in valid_locations:
            child = result(board, col, -player)
            _, score = minimax(child, depth-1, alpha, beta, True, player, start_time)
            if score < value:
                value = score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# les deux fonctions demandées
# IA_Decision
def IA_Decision(board):
    start = time.time()
    col, _ = minimax(board, depth=4, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, player=1, start_time=start)
    return col

# Terminal_Test
def Terminal_Test(board):
    return is_terminal(board)

# Lancer un test IA vs Humain
def play_vs_IA():
    board = initial_state()
    human = int(input("Tu veux être joueur 1 (1) ou joueur 2 (-1) ? "))
    ia = -human
    current = 1

    while not Terminal_Test(board):
        print_board(board)
        if current == human:
            col = int(input(f"Ton coup (0-{COLUMNS-1}) : "))
        else:
            col = IA_Decision(board)
            print(f"L'IA joue : {col}")
        board = result(board, col, current)
        current *= -1

    print_board(board)
    if check_win(board, 1):
        print("Joueur 1 (X) gagne !")
    elif check_win(board, -1):
        print("Joueur 2 (O) gagne !")
    else:
        print("Match nul.")

# Pour lancer un test
play_vs_IA()


