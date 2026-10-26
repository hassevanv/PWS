import random
import main



def choose_move(board, big_board, forced_section, current_player, opponent_player):

    CORNERS = (1, 3, 7, 9)
    BIG_CORNERS = (10, 30, 70, 90)
    #BIG_EDGES = (20, 40, 60, 80)
    BOARD = range(1,10)
    BIG_BOARD = range(10,100,10)
    """ THREATS = ((1,2, 3),(1,3, 2),(2,3, 1),(4,5, 6),(4,6, 5),(5,6, 4),(7,8, 9),(7,9, 8),(8,9, 7),
                    (1,4, 7),(1,7, 4),(4,7, 1),(2,5, 8),(2,8, 5),(5,8, 2),(3,6, 9),(3,9, 6),(6,9, 3),
                    (1,5, ),(1,9),(5,9),(3,5),(3,7),(5,7))
    BIG_THREATS = ((10,20),(10,30),(20,30),(40,50),(40,60),(50,60),(70,80),(70,90),(80,90),
                        (10,40),(10,70),(40,70),(20,50),(20,80),(50,80),(30,60),(30,90),(60,90),
                        (10,50),(10,90),(50,90),(30,50),(30,70),(50,70)) """
    THREATS = (((2,3),(4,7),(5,9)), # Alle twee op een rij, gesorteerd op de lege vakjes in de twee op een rij.
               ((1,3),(5,8)),
               ((1,2),(6,9),(5,7)),
               ((5,6),(1,7)),
               ((4,6),(2,8),(1,9),(3,7)),
               ((4,5),(3,9)),
               ((8,9),(1,4),(3,5)),
               ((7,9),(2,5)),
               ((7,8),(3,6),(1,5)))
    BIG_THREATS = (((20,30),(40,70),(50,90)),
                    ((10,30),(50,80)),
                    ((10,20),(60,90),(50,70)),
                    ((50,60),(10,70)),
                    ((40,60),(20,80),(10,90),(30,70)),
                    ((40,50),(30,90)),
                    ((80,90),(10,40),(30,50)),
                    ((70,90),(20,50)),
                    ((70,80),(30,60),(10,50)))


    # Deel 1, voor het grote veld
    if forced_section is None: # als er vrije keuze is
        player_sections = [big for big in BIG_BOARD if big_board[big] == current_player]
        opponent_sections = [big for big in BIG_BOARD if big_board[big]== opponent_player]
        available_sections = [big for big in BIG_BOARD if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
        available_corner_sections = [big for big in BIG_CORNERS if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
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
        # Deel 1, voor het grote veld
    else:
        chosen_section = forced_section

    # Deel 2, voor het kleine veld
    
    player_cells = [cell for cell in BOARD if board[chosen_section + cell] == current_player]
    opponent_cells = [cell for cell in BOARD if board[chosen_section + cell] == opponent_player]
    available_cells = [cell for cell in BOARD if board[chosen_section + cell] == 0]
    available_corner_cells = [cell for cell in CORNERS if board[chosen_section + cell] == 0]
   
    if chosen_cell is None: # Als het vakje nog niet bepaald is
    # 1. Als er twee op een rij is, win.
        if len(player_cells) >=2
            if for cell in THREATS: 
                if board[chosen_section + cell[0]] == board[chosen_section + cell[1]]

        # 2. Als de tegenstander twee op een rij heeft, block.
        elif len(opponent_cells) >= 2: 
            if for cell in THREATS: 
                if board[chosen_section + cell[0]] == board[chosen_section + cell[1]]

        # 3. Als het kan, maak een dubbele dreiging.
        elif false: 
            return 1

        # 4. Als die gemaakt kan worden, blokkeer de dubbele dreiging van de tegenstander.
        elif false: 
            return 1

        # 5. Als het kan, neem het midden.
        elif board[chosen_section + 5] == 0:
            chosen_cell = 5

        # 6. Als het kan, neem een overstaande hoek tegenover de tegenstander.
        elif false: 
            return 1

        # 7. Als het kan, neem een hoek.
        elif available_corner_cells: 
            chosen_cell = random.choice(available_corner_cells)

        # 8. Anders, neem een rand.
        else:
            chosen_cell = random.choice(available_cells)

    return chosen_section, chosen_cell # Return de gekozen sectie en het gekozen vakje