import random
#nog niet af!!!

def choose_move(board, big_board, forced_section, current_player=None, opponent_player=None):

    # --- Fase 1: probeer middenzelfverwijzing te joinken ---
    if forced_section is None:
        # Controleer of het grote centrum (50) nog open is én niet vol zit
        if big_board[50] == 0 and not all(board[50 + s] != 0 for s in range(1, 10)):
            chosen_section = 50
            # Controleer of het centrumvakje (5) binnen deze sectie nog vrij (0) is
            if board[chosen_section + 5] == 0:
              chosen_cell = 5
            else:
                # Als het centrumvakje al bezet is, kies dan random uit de overige vrije vakjes, dit zou nooit zo moeten zijn
                available_cells = [s for s in range(1, 10) if board[chosen_section + s] == 0]
                chosen_cell = random.choice(available_cells)
            return chosen_section, chosen_cell
        else:
            # Als 50 niet kan, pakken we alle andere nog beschikbare secties
            available_sections = [big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                                  if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))]
            chosen_section = random.choice(available_sections)
    else:
        # Als we gedwongen worden naar een sectie, moeten we die volgen
        chosen_section = forced_section



    # --- Fase 2: BEPAAL HET VAKJE BINNEN DE GEKOZEN SECTIE ---
    # Bepaal of groot midden al gewonnen is, terugsturen als niet
    if big_board[50] == 0 and board[chosen_section + 5] == 0 and not all(board[50 + s] != 0 for s in range(1, 10)):
        chosen_cell = 5
    else:
        if not (forced_section is None): #kijk of je kan terugverwijzen naar niet-gewonnen section
            available_cells = [s for s in range(1,10) if (( not board[forced_section//10 + s*10] == 0) and (board[forced_section + s] == 0) and (big_board[s*10] == 0) and (not s == (forced_section//10)) and (not all(board[50 + s] != 0 for s in range(1, 10))))]
            if len(available_cells) > 0:
                chosen_cell = random.choice(available_cells)
            else: # 'terugsturen' naar nog niet gewonnen vakje waarvan de zelfverwijzing reeds bezet is 
                available_cells = [s for s in range(1,10) if ((big_board[s*10] == 0) and (board[s*10 + s] != 0) and (not all(board[s*10 + t] != 0 for t in range(1,10))))]
                if len(available_cells) > 0:
                    chosen_cell = random.choice(available_cells)
                else: # Anders zelfverwijzing(bv. vakje 44)
                    if board[chosen_section + chosen_section//10] == 0:
                        chosen_cell = chosen_section//10 
                    else:
                      # Als de zelfverwijzing al bezet is, kies dan uit de overige vrije vakjes
                        available_cells = [s for s in range(1, 10) if ((board[chosen_section + s] == 0) and (big_board[s*10] == 0))]
                        if len(available_cells) > 0:
                            chosen_cell = random.choice(available_cells)
                        else: 
                            available_cells = [s for s in range (1,10) if (board[chosen_section + s] == 0)]
                            chosen_cell = random.choice(available_cells)
        else: 
            available_cells = [s for s in range(1,10) if ((big_board[s*10] == 0) and (board[s*10 + s] != 0) and (not all(board[s*10 + t] != 0 for t in range(1,10))))]
            if len(available_cells) > 0:
                chosen_cell = random.choice(available_cells)
            else: 
                if board[chosen_section + chosen_section//10] == 0:
                    chosen_cell = chosen_section//10
                else:
                    available_cells = [s for s in range(1,10) if board[chosen_section + s] == 0]
                    chosen_cell = random.choice(available_cells)
    return chosen_section, chosen_cell