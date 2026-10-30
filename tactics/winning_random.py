# hi
import random

# vaststellen hoe een veld gekozen wordt
def choose_move(board, big_board, forced_section, current_player=None, opponent_player=None):
    THREATS = (((2,3),(4,7),(5,9)), # Alle twee op een rij, gesorteerd op de lege vakjes in de twee op een rij.
               ((1,3),(5,8)),
               ((1,2),(6,9),(5,7)),
               ((5,6),(1,7)),
               ((4,6),(2,8),(1,9),(3,7)),
               ((4,5),(3,9)),
               ((8,9),(1,4),(3,5)),
               ((7,9),(2,5)),
               ((7,8),(3,6),(1,5)))
    
    if forced_section is None: # vaststellen van de beschikbare secties als er geen forced_section is
        available_sections = [big for big in range(10,100,10)
                              if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        chosen_section = random.choice(available_sections) # random een sectie kiezen uit de beschikbare secties
    else:
        chosen_section = forced_section # anders is de chosen_section de forced_section

# de meest scuffed als win dan win ooit maar wat ga je er aan doen?! Dit: (zie eronder)

    available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0]
    chosen_cell = 0

    if len(available_cells) >= 2:
        for cell in available_cells:
            for i in THREATS[cell-1]:
                if board[chosen_section + i[0]] == board[chosen_section + i[1]] == current_player:
                    chosen_cell = cell

    if chosen_cell == 0:
        chosen_cell = random.choice(available_cells)
    
    return chosen_section, chosen_cell # returnen van de gekozen sectie en cel