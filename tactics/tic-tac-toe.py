import random
import main



def choose_move(board, big_board, forced_section,current_player,opponent_player):

    SMALL_CORNERS = (1, 3, 7, 9)
    BIG_CORNERS = (10, 30, 70, 90)
    BOARD = range(1,10)

    # Deel 1, voor het grote veld
    if forced_section is None: # Als er vrije keuze is
        available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                              if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        chosen_section = random.choice(available_sections) # random een sectie kiezen uit de beschikbare secties
    else:
        chosen_section = forced_section # naar de forced_section gaan als er een is

    # Deel 2, kleine veld
    player_cells_corners = [s for s in BOARD if board[chosen_section + s] == current_player] # Board[chosen_section + s] == current_player] # genomen vakjes
    opponent_cells = [s for s in BOARD if board[chosen_section + s] == opponent_player]
    #surrounding_corners = ((3,7),(1,3),(1,9),(1,7),(0,0),(3,9),(1,9),(7,9),(3,7)) # Lijst met omliggende hoeken ingedeeld als [0] is vakje 1 [1] is vakje 2 [2] is vakje 3 etc. (vakje 5 heeft gen surrounding corners)

    # place holder random
    available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0] # vaststellen van de beschikbare cellen in de gekozen sectie
    chosen_cell = random.choice(available_cells) # random een cel kiezen uit de beschikbare cellen

    """ if (board[chosen_section + c] == current_player for c in SMALL_CORNERS):
        # Als de speler een hoekje heeft kies dan een hoekje ernaast (met de laagste index)
        
        for i in player_cells_corners: # Vind een omliggend hoekje naast eigen hoekje, begint met de laagste index
            if surrounding_corners[i-1][0] in available_cells_corners: 
                chosen_cell = surrounding_corners[i-1][0]
            elif surrounding_corners[i-1][1] in available_cells_corners:
                chosen_cell = surrounding_corners[i-1][1]
            if chosen_cell: 
                break

        if not chosen_cell: # Als de tegenstander de omliggende hoekjes heeft:
            if available_cells_corners:
                chosen_cell = random.choice(available_cells_corners) # Random vrij hoekje kiezen
            else:
                available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0] # Random vrij vakje keizen als er geen hoekjes zijn
                chosen_cell = random.choice(available_cells)
    elif available_cells_corners:
        chosen_cell = random.choice(available_cells_corners) # Random vrij hoekje kiezen
    else:
        available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0] # Random vrij vakje keizen als er geen hoekjes zijn
        chosen_cell = random.choice(available_cells) """

    return chosen_section, chosen_cell # Return de gekozen sectie en het gekozen vakje