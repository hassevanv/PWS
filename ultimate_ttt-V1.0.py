import random

# Initialisatie van het bord
# Grote velden: 10, 20, ..., 90
# Kleine velden per groot veld: 1 t/m 9 (bijv. 11 t/m 19, 21 t/m 29, etc.)
board = {}
for big in range(10, 100, 10):
    for small in range(1, 10):
        board[big + small] = 0

# Status van de grote velden (0 = leeg, 1 = X, 2 = O)
big_board = {big: 0 for big in range(10, 100, 10)}

def check_big_win():
    # Wincombinaties voor de grote velden
    win_conditions = [
        [10, 20, 30], [40, 50, 60], [70, 80, 90], # Horizontaal
        [10, 40, 70], [20, 50, 80], [30, 60, 90], # Verticaal
        [10, 50, 90], [30, 50, 70]                 # Diagonaal
    ]
    for condition in win_conditions:
        if big_board[condition[0]] == big_board[condition[1]] == big_board[condition[2]] != 0:
            return big_board[condition[0]]
    return 0

def check_small_win(big_field):
    # Wincombinaties binnen één groot veld (gebaseerd op het laatste cijfer)
    win_conditions = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9], # Horizontaal
        [1, 4, 7], [2, 5, 8], [3, 6, 9], # Verticaal
        [1, 5, 9], [3, 5, 7]              # Diagonaal
    ]
    for condition in win_conditions:
        pos1 = big_field + condition[0]
        pos2 = big_field + condition[1]
        pos3 = big_field + condition[2]
        if board[pos1] == board[pos2] == board[pos3] != 0:
            return board[pos1]
    return 0

# --- Start van het spel ---
current_player = 1
last_digit = None

print("Start van Ultimate Tic-Tac-Toe!")

while True:
    # Bepaal in welke sectie (groot veld) we moeten spelen
    if last_digit is None:
        # Eerste beurt: kies een volledig willekeurig groot veld
        current_section = random.choice(list(big_board.keys()))
    else:
        current_section = last_digit * 10

    # Logica: "if section-big != 0 place random"
    # Als het grote veld al gewonnen is (of vol/niet beschikbaar), kies een random vrij groot veld
    if big_board[current_section] != 0:
        available_sections = [big for big, status in big_board.items() if status == 0]
        if not available_sections:
            print("Gelijkspel! Geen grote velden meer beschikbaar.")
            break
        current_section = random.choice(available_sections)

    # Logica: "a = random" -> kies een willekeurig klein vakje (1 t/m 9) binnen de sectie
    # We blijven zoeken tot we een leeg vakje vinden in deze sectie
    available_cells = [small for small in range(1, 10) if board[current_section + small] == 0]
    
    if not available_cells:
        # Als de gekozen sectie vol is maar nog niet gewonnen, kies dan een random sectie die wel plek heeft
        available_sections = [big for big in big_board.keys() if any(board[big + s] == 0 for s in range(1, 10))]
        if not available_sections:
            print("Gelijkspel! Het bord is vol.")
            break
        current_section = random.choice(available_sections)
        available_cells = [small for small in range(1, 10) if board[current_section + small] == 0]

    a = random.choice(available_cells)
    chosen_field = current_section + a

    # Logica: "make section 1 (or 2)"
    board[chosen_field] = current_player
    print(self_message := f"Speler {current_player} kiest vakje {chosen_field}")

    # Logica: "If last digit is 1,2,3 or ect. = 1 or 2 make section-big 1 or 2"
    # Controleer of het kleine veld hiermee gewonnen wordt
    if big_board[current_section] == 0:
        winner_of_section = check_small_win(current_section)
        if winner_of_section != 0:
            big_board[current_section] = winner_of_section
            print(f"Sectie {current_section} is gewonnen door Speler {winner_of_section}!")

    # Logica: "if 10,20,30 or 40,50,60 or ect. =1 or =2 print WIN!"
    overall_winner = check_big_win()
    if overall_winner != 0:
        print(f"WIN! Speler {overall_winner} heeft het spel gewonnen!")
        break

    # Bereid de volgende beurt voor: "turn n-1 last digit * 10 + a"
    last_digit = a
    
    # Wissel van speler
    current_player = 2 if current_player == 1 else 1