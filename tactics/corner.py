import random

def choose_move(board, big_board, forced_section, current_player=None):

    SMALL_CORNERS = (1, 3, 7, 9)
    BIG_CORNERS = (10, 30, 70, 90)

    if forced_section is None: # als er vrije keuze is
        available_big_corners = [big for big in BIG_CORNERS # filter vrije grote hoeken
                                 if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        
        if available_big_corners:
            chosen_section = random.choice(available_big_corners) # random grote hoek kiezen uit de selectie
        else:
            available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90) # vaststellen welke niet-hoeken er nog beschikbaar zijn
                                  if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
            chosen_section = random.choice(available_sections) # random sectie kiezen uit de beschikbare secties
    else:
        chosen_section = forced_section # naar de forced_section gaan als er een is

    available_cells_corners = [s for s in SMALL_CORNERS if board[chosen_section + s] == 0] # vrije lege kleine hoeken vaststellen
    
    if available_cells_corners:
        chosen_cell = random.choice(available_cells_corners) # random vrij hoekje kiezen
    else:
        available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0] # random vrij vakje keizen als er geen hoekjes zijn
        chosen_cell = random.choice(available_cells)
    
    return chosen_section, chosen_cell # return de gekozen sectie en het gekozen vakje