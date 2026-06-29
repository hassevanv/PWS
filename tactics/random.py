import random

# vaststellen hoe een veld gekozen wordt
def choose_move(board, big_board, forced_section,current_player):
    if forced_section is None: # vaststellen van de beschikbare secties als er geen forced_section is
        available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                              if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        chosen_section = random.choice(available_sections) # random een sectie kiezen uit de beschikbare secties
    else:
        chosen_section = forced_section # anders is de chosen_section de forced_section

    available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0] # vaststellen van de beschikbare cellen in de gekozen sectie
    chosen_cell = random.choice(available_cells) # random een cel kiezen uit de beschikbare cellen
    
    return chosen_section, chosen_cell # returnen van de gekozen sectie en cel