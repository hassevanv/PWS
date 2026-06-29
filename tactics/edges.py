import random

def choose_move(board, big_board, forced_section):

    SMALL_EDGES = (2, 4, 6, 8)
    BIG_EDGES = (20, 40, 60, 80)

    if forced_section is None: # als er vrije keuze is
        available_big_edges = [big for big in BIG_EDGES # filter vrije grote randvakken
                                if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        
        if available_big_edges:
            chosen_section = random.choice(available_big_edges) # random groot randvak kiezen uit de selectie
        else:
            available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90) # vaststellen welke niet-randvakken er nog beschikbaar zijn
                                  if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
            chosen_section = random.choice(available_sections) # random sectie kiezen uit de beschikbare secties
    else:
        chosen_section = forced_section # naar de forced_section gaan als er een is

    available_cells_edges = [s for s in SMALL_EDGES if board[chosen_section + s] == 0] # vrije lege kleine randvakjes vaststellen
    
    if available_cells_edges:
        chosen_cell = random.choice(available_cells_edges) # random vrij randvakje kiezen
    else:
        available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0] # random vrij vakje keizen als er geen randvakjes zijn
        chosen_cell = random.choice(available_cells)
    
    return chosen_section, chosen_cell # return de gekozen sectie en het gekozen vakje