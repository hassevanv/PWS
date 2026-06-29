import random

def choose_move(board, big_board, forced_section, current_player=None):

    # --- STAP 1: BEPAAL DE GROTE SECTIE (Als er een Free Move is) ---
    if forced_section is None:
        # Controleer of het grote centrum (50) nog open is én niet vol zit
        if big_board[50] == 0 and not all(board[50 + s] != 0 for s in range(1, 10)):
            chosen_section = 50
        else:
            # Als 50 niet kan, pakken we alle andere nog beschikbare secties
            available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                                  if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
            chosen_section = random.choice(available_sections)
    else:
        # Als we gedwongen worden naar een sectie, moeten we die volgen
        chosen_section = forced_section

    # --- STAP 2: BEPAAL HET VAKJE BINNEN DE GEKOZEN SECTIE ---
    # Controleer of het centrumvakje (5) binnen deze sectie nog vrij (0) is
    if board[chosen_section + 5] == 0:
        chosen_cell = 5
    else:
        # Als het centrumvakje al bezet is, kies dan random uit de overige vrije vakjes
        available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0]
        chosen_cell = random.choice(available_cells)
    
    return chosen_section, chosen_cell