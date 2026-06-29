import random

def choose_move(board, big_board, forced_section):
    """Volledig willekeurige tactiek."""
    if forced_section is None:
        available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                              if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        chosen_section = random.choice(available_sections)
    else:
        chosen_section = forced_section

    available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0]
    chosen_cell = random.choice(available_cells)
    
    return chosen_section, chosen_cell