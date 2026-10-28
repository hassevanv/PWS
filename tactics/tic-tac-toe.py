import random
import main

def threat(board, current_player, opponent_player, available_cells):
    # Kiest cell die 2 op een rij afmaakt
    # Als die cell niet bestaat return 0
    
    BOARD = range(1,10)
    BIG_BOARD = range(10,100,10)
    THREATS = (((2,3),(4,7),(5,9)), # Alle twee op een rij, gesorteerd op de lege vakjes in de twee op een rij.
               ((1,3),(5,8)),
               ((1,2),(6,9),(5,7)),
               ((5,6),(1,7)),
               ((4,6),(2,8),(1,9),(3,7)),
               ((4,5),(3,9)),
               ((8,9),(1,4),(3,5)),
               ((7,9),(2,5)),
               ((7,8),(3,6),(1,5)))



    return chosen_cell

def check(board, current_player, opponent_player, chosen_section, available_cells):
    # Past regels 2 t/m 8 to van de tactic
    BOARD = range(1,10)
    CORNERS = (1, 3, 7, 9)
    mult = 1

    if chosen_section == 0:
        mult = 10

    # 3. Als het kan, maak een dubbele dreiging.
    if False: 
        return 1

    # 4. Als die gemaakt kan worden, blokkeer de dubbele dreiging van de tegenstander.
    elif False: 
        return 1

    # 5. Als het kan, neem het midden.
    elif available_cells == 50 or available_cells == 5:
        return 5

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
        return random.choice(available_cells)/10
    else:
        return random.choice(available_cells)

    return error

def choose_move(board, big_board, forced_section, current_player, opponent_player):

    CORNERS = (1, 3, 7, 9)
    BOARD = range(10,100, 10)
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
        player_sections = [big for big in BOARD if big_board[big] == current_player]
        opponent_sections = [big for big in BOARD if big_board[big]== opponent_player]
        available_sections = [big for big in BOARD if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        available_corner_sections = [big for big in CORNERS if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]

        # 1.
        chosen_section = threat(board, current_player, opponent_player, available_sections)
        # 2.
        if chosen_section == 0:
            chosen_section = threat(board, opponent_player, current_player, available_sections)
        # 3-8.
        if chosen_section == 0:
            chosen_section = check(board, current_player, opponent_player, 0, available_sections)*10
        #available_edge_sections = [big for big in BIG_EDGES if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]

        # 1. Als er twee op een rij is in minimaal 1 kleiner veld, kies dan het voordeligste veld.
        # Geeft de locatie van winnende vakjes in een list van de vorm [[1e win section, 1e win cell], [2e win section, 2e win cell], etc.] of nee toch 2 lists 1 voor cells en 1 voor sections
        big_possibilities = []
        possibilities = []
        for big in available_sections: 
            player_cells = [cell for cell in BOARD if board[BIG_BOARD + cell] == current_player]
            available_cells = [cell for cell in BOARD if board[BIG_BOARD + cell] == 0]
            winning = False

            if len(player_cells) >= 2: # als de speler meer dan 2 vakjes in een veld heeft (anders boeit het toch niet)
                for cell in available_cells:
                    for i in THREATS[cell]:
                        if board[big + i[0]] == board[big + i[1]] == current_player:
                            possibilities.append(cell)
                            big_possibilities.append(big/10)
                            winning = True
                            break # alleen 1 win combi per sectie
                    if winning:
                        break

        if len(possibilities) == 0:
             # 2. Als de tegenstander twee op een rij heeft, block.
            if false: 
                return 1

            # 3. Als het kan, maak een dubbele dreiging.
            elif false: 
                return 1

            # 4. Als die gemaakt kan worden, blokkeer de dubbele dreiging van de tegenstander.
            elif false: 
                return 1

            # 5. Als het kan, neem het midden.
            elif board[50] == 0:
                chosen_section = 50

            # 6. Als het kan, neem een overstaande hoek tegenover de tegenstander.
            elif false: 
                return 1

            # 7. Als het kan, neem een hoek.
            elif available_corner_sections: 
                chosen_section = random.choice(available_corner_sections)

            # 8. Anders, neem een rand.
            else:
                chosen_section = random.choice(available_sections)

        if len(possibilities) == 1:
            chosen_section = big_possibilities[0]
            chosen_cell = possibilities[0]
            return chosen_section, chosen_cell

        else:
            # 1.
            if len(player_sections) >= 2:
                j = -1
                for big in big_possibilities:
                    j += 1
                    for i in THREATS:
                        if big_board[i[0] * 10] == big_board[i[1] * 10] == current_player:
                            chosen_section = big * 10
                            chosen_cell = possibilities[j]
                            return chosen_section, chosen_cell
                            
            else:
                # 2. Als de tegenstander twee op een rij heeft, block.
                if false: 
                    return 1

                # 3. Als het kan, maak een dubbele dreiging.
                elif false: 
                    return 1

                # 4. Als die gemaakt kan worden, blokkeer de dubbele dreiging van de tegenstander.
                elif false: 
                    return 1

                # 5. Als het kan, neem het midden.
                elif board[50] == 0:
                    chosen_section = 50

                # 6. Als het kan, neem een overstaande hoek tegenover de tegenstander.
                elif false: 
                    return 1

                # 7. Als het kan, neem een hoek.
                elif available_corner_sections:

                    chosen_section = random.choice()

                # 8. Anders, neem een rand.
                else:
                    chosen_section = random.choice(big_possibilities)
    else:
        chosen_section = forced_section

    # Deel 2, voor het kleine veld
    opponent_cells = [cell for cell in BOARD if board[chosen_section + cell] == opponent_player]
    available_cells = [cell for cell in BOARD if board[chosen_section + cell] == 0]
    
    if len(available_cells) == 1:
        return chosen_section, available_cells[0]

    # 1. Als je twee op een rij hebt, win.
    if len(opponent_cells) + len(available_cells) >= 8:
        chosen_cell = threat(board, current_player, opponent_player)
    
    # 2. Als de tegenstander twee op een rij heeft, block.
    elif len(opponent_cells) >= 2 and chosen_cell == 0: 
        chosen_cell = threat(board, opponent_player, current_player)
    else:
        chosen_cell = check(board, current_player, opponent_player, chosen_section, available_cells)

    return chosen_section, chosen_cell # Return de gekozen sectie en het gekozen vakje