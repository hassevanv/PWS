import random

def choose_move(board, big_board, forced_section, current_player=None, opponent_player=None):

    SMALL_CORNERS = (1, 3, 7, 9)
    BIG_CORNERS = (10, 30, 70, 90)
    SMALL_EDGES = (2, 4, 6, 8)
    BIG_EDGES = (20, 40, 60, 80)

    # --- STAP 1: BEPAAL DE GROTE SECTIE ---

    if forced_section is None:

        # Eerst centrum proberen
        if (
            big_board[50] == 0
            and not all(board[50 + s] != 0 for s in range(1, 10))
        ):
            chosen_section = 50

        else:
            # Daarna random grote hoek
            available_big_corners = [
                big for big in BIG_CORNERS
                if big_board[big] == 0
                and not all(board[big + s] != 0 for s in range(1, 10))
            ]

            if available_big_corners:
                chosen_section = random.choice(available_big_corners)

            else:
                # Daarna random grote rand
                available_big_edges = [
                    big for big in BIG_EDGES
                    if big_board[big] == 0
                    and not all(board[big + s] != 0 for s in range(1, 10))
                ]

                if available_big_edges:
                    chosen_section = random.choice(available_big_edges)

                else:
                    # Als laatste: iedere beschikbare sectie
                    available_sections = [
                        big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                        if big_board[big] == 0
                        and not all(board[big + s] != 0 for s in range(1, 10))
                    ]

                    if not available_sections:
                        return None

                    chosen_section = random.choice(available_sections)

    else:
        # Forced section moet altijd gevolgd worden
        chosen_section = forced_section

    # --- STAP 2: KIES HET VAKJE BINNEN DE SECTIE ---

    # Eerst centrum
    if board[chosen_section + 5] == 0:
        chosen_cell = 5

    else:
        # Daarna kleine hoek
        available_cells_corners = [
            s for s in SMALL_CORNERS
            if board[chosen_section + s] == 0
        ]

        if available_cells_corners:
            chosen_cell = random.choice(available_cells_corners)

        else:
            # Daarna kleine rand
            available_cells_edges = [
                s for s in SMALL_EDGES
                if board[chosen_section + s] == 0
            ]

            if available_cells_edges:
                chosen_cell = random.choice(available_cells_edges)

            else:
                # Geen zet mogelijk in deze sectie
                return None

    return chosen_section, chosen_cell