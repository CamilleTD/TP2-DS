# %% Puissance 4 : Affrontement entre IA 
import math
import random
import copy
import time

# Définition des constantes pour la taille du plateau et la condition de victoire
ROWS = 6
COLUMNS = 12
ALIGN = 4  # Nombre de jetons à aligner pour gagner

# Fonction qui retourne un plateau vide
def initial_state():
    return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

# Fonction d'affichage du plateau dans la console
def print_board(board):
    for row in board:
        print('|' + '|'.join(['.' if c == 0 else ('X' if c == 1 else 'O') for c in row]) + '|')
    print(' ' + ' '.join(map(str, range(COLUMNS))))

# Retourne les colonnes jouables 
def actions(board):
    return [c for c in range(COLUMNS) if board[0][c] == 0]

# Applique un coup sur le plateau et retourne le nouveau plateau
def result(board, col, player):
    new_board = copy.deepcopy(board)  # Crée une copie du plateau
    for row in reversed(range(ROWS)):
        if new_board[row][col] == 0:  # Trouve la première case vide en partant du bas
            new_board[row][col] = player
            return new_board
    return board  # Si la colonne est pleine 

# Teste si l'état du jeu est terminal cf fonction
def is_terminal(board):
    total_tokens = sum(1 for row in board for cell in row if cell != 0)
    return (
       check_win(board, 1) or    # Joueur 1 gagne
       check_win(board, -1) or   # Joueur 2 gagne
       total_tokens >= ROWS * COLUMNS  # match nul
    )

# Vérifie si un joueur donné a gagné
def check_win(board, player):
    # Vérifie toutes les directions : horizontale, verticale et les deux diagonales

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

# Évalue le plateau pour un joueur donné 
def evaluate(board, player):
    opponent = -player
    return score_position(board, player) - score_position(board, opponent)

# Fonction qui attribue un score à une position selon différents critères
def score_position(board, player):
    score = 0
    # Parcourt toutes les positions horizontales, verticales et diagonales

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

# Évalue une fenêtre et retourne un score
def evaluate_window(window, player):
    score = 0
    opp = -player

    # Cas favorables pour le joueur
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    # Cas dangereux (l'adversaire peut gagner)
    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 4

    return score

# Implémentation de l'algorithme Minimax en utilisant la méthode 'élagage alpha-bêta'
def minimax(board, depth, alpha, beta, maximizingPlayer, player, start_time, time_limit=9.5):
    # Si le plateau est terminal ou la profondeur est atteinte ou limite de temps dépassée
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
    best_col = random.choice(valid_locations)  # Choix par défaut

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
                break  # Élagage
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
                break  # Élagage
        return best_col, value

# les deux fonctions demandées
# Fonction appelée par l'IA pour choisir un coup
def IA_Decision(board):
    start = time.time()
    col, _ = minimax(board, depth=4, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, player=1, start_time=start)
    return col

# Fonction utilisée pour vérifier si la partie est finie
def Terminal_Test(board):
    return is_terminal(board)

# Lancer un test IA vs Humain
def play_vs_IA():
    board = initial_state()
    
    # Boucle pour s'assurer que l'utilisateur entre 1 ou 2
    while True:
        choix = input("Tu veux être joueur 1 (1) ou joueur 2 (2) ? ")
        if choix in ['1', '2']:
            human = int(choix)
            break
        else:
            print("Entrée invalide. Merci de taper 1 ou 2.")
    
    # Attribution des symboles en fonction du choix
    if human == 1:
        human = 1
        ia = -1
    else:
        human = -1
        ia = 1

    current = 1  # Le joueur 1 commence

    while not Terminal_Test(board):
        print_board(board)
        if current == human:
            # Tour du joueur humain
            while True:
                try:
                    col = int(input(f"Ton coup (0-{COLUMNS-1}) : "))
                    if col < 0 or col >= COLUMNS:
                        print("Colonne invalide. Choisis une colonne entre 0 et", COLUMNS-1)
                    elif board[0][col] != 0:
                        print("Colonne remplie. Choisis une autre colonne.")
                    else:
                        break
                except ValueError:
                    print("Entrée invalide. Merci d’entrer un nombre.")
        else:
            # Tour de l'IA
            col = IA_Decision(board)
            print(f"L'IA joue : {col}")
            if board[0][col] != 0:
                print(f"L'IA a choisi une colonne pleine ({col}). Elle passe son tour.")
                col = None
        
        if col is not None:
            board = result(board, col, current)
            current *= -1  # Changement de joueur

    # Fin du jeu : afficher le résultat
    print_board(board)
    if check_win(board, 1):
        print("Joueur 1 (X) gagne !")
    elif check_win(board, -1):
        print("Joueur 2 (O) gagne !")
    else:
        print("Match nul.")

# Pour lancer un test
play_vs_IA()
