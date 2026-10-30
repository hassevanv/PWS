import random
import copy

def win(board, current_player, opponent_player, chosen_section, available_cells, giveAll):
    # Kiest cell die 2 op een rij afmaakt
    # Als die cell niet bestaat return 0
    # Geeft de eerste optie of een lijst (ligt aan giveAll True/False)
    THREATS = (((2,3),(4,7),(5,9)), # Alle twee op een rij, gesorteerd op de lege vakjes in de twee op een rij.
               ((1,3),(5,8)),
               ((1,2),(6,9),(5,7)),
               ((5,6),(1,7)),
               ((4,6),(2,8),(1,9),(3,7)),
               ((4,5),(3,9)),
               ((8,9),(1,4),(3,5)),
               ((7,9),(2,5)),
               ((7,8),(3,6),(1,5)))
    chosen_cells = []

    if available_cells[0] % 10 == 0: # Als die een section moet kiezen
        for cell in available_cells:
            cell = int(cell/10)
            for i in THREATS[cell-1]:
                if board[chosen_section + i[0] * 10] == board[chosen_section + i[1]* 10] == current_player:
                    if giveAll:
                        chosen_cells.append(cell)
                    else:
                        return cell
    else:                           # Als die een cell moet kiezen
        for cell in available_cells:
            for i in THREATS[cell-1]:
                if board[chosen_section + i[0]] == board[chosen_section + i[1]] == current_player:
                    if giveAll:
                        chosen_cells.append(cell)
                    else:
                        return cell
    if giveAll:
        return chosen_cells
    else: 
        return 0

def doubleThreat(board, current_player, opponent_player, chosen_section, available_cells):
    old_board = copy.deepcopy(board)
    #print(old_board)

    for cell in available_cells:
        board[chosen_section + cell] = current_player
        threats = win(board, current_player, opponent_player, chosen_section, available_cells, True)
        #print("nieuw ", old_board)
        if len(threats) >= 2:
            return cell
        board = copy.deepcopy(old_board)

    return 0

def check(board, current_player, opponent_player, chosen_section, available_cells):
    # Past regels 2 t/m 8 to van de tactic
    CORNERS = (1, 3, 7, 9)
    mult = 1

    if chosen_section == 0:
        mult = 10

    # 5. Als het kan, neem het midden.
    #elif 50 in available_cells or 5 in available_cells :
    #    return 5

    # 6. Als het kan, neem een overstaande hoek tegenover de tegenstander. 
    for cell in CORNERS:
        if board[chosen_section + cell*mult] == 0 and board[chosen_section + (10-cell)*mult] == opponent_player:  # Overstaande hoeken bij elkaar opgeteld zijn gelijk aan 10
            return cell

    # 7. Als het kan, neem een hoek.
    available_corner_cells = [cell for cell in CORNERS if cell*mult in available_cells]
    if available_corner_cells:
        return random.choice(available_corner_cells)

    # 8. Anders, neem een rand.
    elif available_cells[0]%10 == 0:        # Controleer of het in section of cell is, zodat er altijd een getal tussen de 1 en de 9 als output is.
        return int(random.choice(available_cells)/10)
    else:
        return random.choice(available_cells)

def choose_move(board, big_board, forced_section, current_player, opponent_player):
    BOARD = range(1,10)
    BIG_BOARD = range(10,100, 10)
    THREATS = (((2,3),(4,7),(5,9)), # Alle twee op een rij, gesorteerd op de lege vakjes in de twee op een rij.
               ((1,3),(5,8)),
               ((1,2),(6,9),(5,7)),
               ((5,6),(1,7)),
               ((4,6),(2,8),(1,9),(3,7)),
               ((4,5),(3,9)),
               ((8,9),(1,4),(3,5)),
               ((7,9),(2,5)),
               ((7,8),(3,6),(1,5)))


    # Deel 1, voor het grote veld
    if forced_section is None: # als er vrije keuze is
        opponent_sections = []
        available_sections = []
        for big in BIG_BOARD:
            if big_board[big] == opponent_player:
                opponent_sections.append(big)
            if big_board[big] == 0:
                available_sections.append(big)
        #opponent_sections = [big for big in BIG_BOARD if big_board[big]== opponent_player]
        #available_sections = [big for big in BIG_BOARD if big_board[big] == 0 and not all(board[big + s] != 0 for s in BOARD)]
        chosen_section = 0

        # 1.
        if len(opponent_sections) + len(available_sections) <= 8: # Tenminste twee player vakjes is blijkbaar niet nodig voor winst
            chosen_section = win(big_board, current_player, opponent_player, 0, available_sections, False) * 10
        # 2.
        if len(opponent_sections) >= 2 and chosen_section == 0:
            chosen_section = win(big_board, opponent_player, current_player, 0, available_sections, False) * 10
        # 3. Als het kan, maak een dubbele dreiging.
        if len(opponent_sections) + len(available_sections) <= 8: # Tenminste twee player vakjes is blijkbaar niet nodig voor winst
            chosen_section = doubleThreat(big_board, current_player, opponent_player, 0, available_sections)
        # 4. Als die gemaakt kan worden, blokkeer de dubbele dreiging van de tegenstander.
        if len(opponent_sections) >= 2 and chosen_section == 0:
            chosen_section = doubleThreat(big_board, opponent_player, current_player, 0, available_sections) # blijkbaar niet geactiveerd voor winst als speler 1
        # 5-8.  blijkbaar niet geactiveerd voordat 1-4 een keer geactiveerd is als speler 1 zijnde
        if chosen_section == 0:
            chosen_section = check(big_board, current_player, opponent_player, 0, available_sections) * 10 # blijkbaar overbodig voor winst als speler 1
    else:
        chosen_section = forced_section

    # Deel 2, voor het kleine veld
    opponent_cells = []
    available_cells = []
    for cell in BOARD:
        if board[chosen_section + cell] == opponent_player:
            opponent_cells.append(cell)
        if board[chosen_section + cell] == 0:
            available_cells.append(cell)
    #opponent_cells = [cell for cell in BOARD if board[chosen_section + cell] == opponent_player]
    #available_cells = [cell for cell in BOARD if board[chosen_section + cell] == 0]
    chosen_cell = 0
    if len(available_cells) == 1:
        chosen_cell = available_cells[0]

    # 1. Als je twee op een rij hebt, win.
    if len(opponent_cells) + len(available_cells) >= 8:
        chosen_cell = win(board, current_player, opponent_player, chosen_section, available_cells, False)
    
    # 2. Als de tegenstander twee op een rij heeft, block.
    if len(opponent_cells) >= 2 and chosen_cell == 0: 
        chosen_cell = win(board, opponent_player, current_player, chosen_section, available_cells, False)

    #3.
    if len(opponent_cells) + len(available_cells) >= 8 and chosen_cell == 0:
        chosen_cell = doubleThreat(board, current_player, opponent_player, chosen_section, available_cells)
    
    #4.
    if len(opponent_cells) >= 2 and chosen_cell == 0: 
        chosen_cell = doubleThreat(board, opponent_player, current_player, chosen_section, available_cells)
    #5-8. blijkbaar niet geactiveerd voordat 1-4 een keer geactiveerd is als speler 1 zijnde
    if chosen_cell == 0: 
        chosen_cell = check(board, current_player, opponent_player, chosen_section, available_cells)

    return int(chosen_section), int(chosen_cell) # Return de gekozen sectie en het gekozen vakje