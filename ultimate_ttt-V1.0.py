import random
import time
from multiprocessing import Pool, cpu_count

# --- INSTELLINGEN ---
AANTAL_SIMULATIES = 10000000  

# --- VASTE WINCOMBINATIES (Globale tuples zijn sneller dan lijsten in functies) ---
BIG_WIN_CONDITIONS = (
    (10, 20, 30), (40, 50, 60), (70, 80, 90),
    (10, 40, 70), (20, 50, 80), (30, 60, 90),
    (10, 50, 90), (30, 50, 70)
)

SMALL_WIN_CONDITIONS = (
    (1, 2, 3), (4, 5, 6), (7, 8, 9),
    (1, 4, 7), (2, 5, 8), (3, 6, 9),
    (1, 5, 9), (3, 5, 7)
)

def player_1_tactic(board, current_section):
    # List comprehensions zijn in Python razendsnel op C-niveau geoptimaliseerd
    available_cells = [s for s in range(1, 10) if board[current_section + s] == 0]
    return random.choice(available_cells)

def player_2_tactic(board, current_section):
    available_cells = [s for s in range(1, 10) if board[current_section + s] == 0]
    return random.choice(available_cells)

def check_big_win(big_board):
    for c in BIG_WIN_CONDITIONS:
        if big_board[c[0]] == big_board[c[1]] == big_board[c[2]] != 0:
            return big_board[c[0]]
    return 0

def check_small_win(board, big_field):
    for c in SMALL_WIN_CONDITIONS:
        if board[big_field + c[0]] == board[big_field + c[1]] == board[big_field + c[2]] != 0:
            return board[big_field + c[0]]
            
    # Snelle check of er nog een 0 in de sectie zit zonder hele lijsten te kopiëren
    if all(board[big_field + s] != 0 for s in range(1, 10)):
        # Tel direct
        c1 = sum(1 for s in range(1, 10) if board[big_field + s] == 1)
        return 1 if c1 > 4 else 2  # Als speler 1 er meer dan 4 heeft (dus 5 of meer), wint 1. Anders 2.
            
    return 0

def run_single_game(_):
    board = {big + small: 0 for big in range(10, 100, 10) for small in range(1, 10)}
    big_board = {big: 0 for big in range(10, 100, 10)}
    current_player = 1
    last_digit = None

    while True:
        if last_digit is None:
            current_section = random.choice((10, 20, 30, 40, 50, 60, 70, 80, 90))
        else:
            current_section = last_digit * 10

        section_is_full = all(board[current_section + s] != 0 for s in range(1, 10))
        
        if big_board[current_section] != 0 or section_is_full:
            available_sections = [
                big for big in (10, 20, 30, 40, 50, 60, 70, 80, 90)
                if big_board[big] == 0 and not all(board[big + s] != 0 for s in range(1, 10))
            ]
            if not available_sections:
                return 0  
            current_section = random.choice(available_sections)

        if current_player == 1:
            a = player_1_tactic(board, current_section)
        else:
            a = player_2_tactic(board, current_section)

        chosen_field = current_section + a
        board[chosen_field] = current_player

        if big_board[current_section] == 0:
            winner_of_section = check_small_win(board, current_section)
            if winner_of_section != 0:
                big_board[current_section] = winner_of_section

        overall_winner = check_big_win(big_board)
        if overall_winner != 0:
            return overall_winner

        last_digit = a
        current_player = 2 if current_player == 1 else 1

if __name__ == '__main__':
    cores = cpu_count()
    print(f"Start... {AANTAL_SIMULATIES} potjes over {cores} cores met chunksize optimalisatie.")
    
    start_time = time.time()
    stats = {1: 0, 2: 0, 0: 0}
    
    # Bepaal een efficiënte chunksize (bijv. 500 potjes per keer per core)
    chunk = max(1, AANTAL_SIMULATIES // (cores * 4))

    with Pool(processes=cores) as pool:
        # chunksize=chunk zorgt dat de CPU veel efficiënter data verdeelt
        results = pool.map(run_single_game, range(AANTAL_SIMULATIES), chunksize=chunk)
    
    for result in results:
        stats[result] += 1

    elapsed_time = time.time() - start_time
    print(f"\nResultaten: S1: {stats[1]} | S2: {stats[2]} | Gelijk: {stats[0]}")
    print(f"Totale rekentijd: {elapsed_time:.4f} seconden")