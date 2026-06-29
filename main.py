import os
import time
import importlib
import random
from multiprocessing import Pool, cpu_count

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

# --- ENGINE CONTROLES ---
def check_big_win(big_board):
    for c in BIG_WIN_CONDITIONS:
        if big_board[c[0]] == big_board[c[1]] == big_board[c[2]] != 0:
            return big_board[c[0]]
    return 0

def check_small_win(board, big_field):
    for c in SMALL_WIN_CONDITIONS:
        if board[big_field + c[0]] == board[big_field + c[1]] == board[big_field + c[2]] != 0:
            return board[big_field + c[0]]
            
    if all(board[big_field + s] != 0 for s in range(1, 10)):
        c1 = sum(1 for s in range(1, 10) if board[big_field + s] == 1)
        return 1 if c1 > 4 else 2  
    return 0

# --- SIMULATIE RUNNER ---
def run_single_game(args):
    tactic_1_name, tactic_2_name = args
    
    # Dynamisch de tactieken importeren op de specifieke CPU core
    tactic_1 = importlib.import_module(f"tactics.{tactic_1_name}").choose_move
    tactic_2 = importlib.import_module(f"tactics.{tactic_2_name}").choose_move

    board = {big + small: 0 for big in range(10, 100, 10) for small in range(1, 10)}
    big_board = {big: 0 for big in range(10, 100, 10)}
    current_player = 1
    last_digit = None

    while True:
        forced_section = None
        if last_digit is not None:
            potential_section = last_digit * 10
            section_is_full = all(board[potential_section + s] != 0 for s in range(1, 10))
            if big_board[potential_section] == 0 and not section_is_full:
                forced_section = potential_section
        
        if forced_section is None:
            any_moves_left = any(big_board[b] == 0 and not all(board[b + s] != 0 for s in range(1, 10)) for b in big_board)
            if not any_moves_left:
                return 0

        if current_player == 1:
            chosen_section, a = tactic_1(board, big_board, forced_section)
        else:
            chosen_section, a = tactic_2(board, big_board, forced_section)

        chosen_field = chosen_section + a
        board[chosen_field] = current_player

        if big_board[chosen_section] == 0:
            winner_of_section = check_small_win(board, chosen_section)
            if winner_of_section != 0:
                big_board[chosen_section] = winner_of_section

        overall_winner = check_big_win(big_board)
        if overall_winner != 0:
            return overall_winner

        last_digit = a
        current_player = 2 if current_player == 1 else 1

# --- INTERACTIVE MENU ---
def get_available_tactics():
    tactics_dir = os.path.join(os.path.dirname(__file__), "tactics")
    files = os.listdir(tactics_dir)
    tactics = [f[:-3] for f in files if f.endswith(".py") and f != "__init__.py"]
    return sorted(tactics)

def select_tactic(player_num, tactics_list):
    print(f"\nBeschikbare tactieken voor Speler {player_num}:")
    for idx, name in enumerate(tactics_list, 1):
        print(f" [{idx}] {name}")
    
    while True:
        try:
            keuze = int(input(f"Kies tactiek voor Speler {player_num} (nummer): "))
            if 1 <= keuze <= len(tactics_list):
                return tactics_list[keuze - 1]
        except ValueError:
            pass
        print("Ongeldige keuze, probeer opnieuw.")

def ask_simulation_count():
    while True:
        try:
            aantal = int(input("\nHoeveel potjes wil je simuleren? "))
            if aantal > 0:
                return aantal
        except ValueError:
            pass
        print("Ongeldig aantal, vul een positief heel getal in.")

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    available_tactics = get_available_tactics()
    if not available_tactics:
        print("Fout: Geen tactiek-bestanden gevonden in de map 'tactics/'!")
        exit()

    print("=== ULTIMATE TIC-TAC-TOE SIMULATOR ===")
    tactic_p1 = select_tactic(1, available_tactics)
    tactic_p2 = select_tactic(2, available_tactics)
    
    # Vraag hier naar het aantal simulaties
    aantal_simulaties = ask_simulation_count()

    # Start simulatie
    cores = cpu_count()
    print(f"\n[INFO] Starten van {aantal_simulaties} potjes ({tactic_p1} VS {tactic_p2}) over {cores} cores...")
    
    start_time = time.time()
    stats = {1: 0, 2: 0, 0: 0}
    
    chunk = max(1, aantal_simulaties // (cores * 4))
    game_args = [(tactic_p1, tactic_p2)] * aantal_simulaties

    with Pool(processes=cores) as pool:
        results = pool.map(run_single_game, game_args, chunksize=chunk)
    
    for result in results:
        stats[result] += 1

    elapsed_time = time.time() - start_time
    
    # Print Resultaten
    print("\n" + "="*30)
    print(f"RESULTATEN ({tactic_p1} vs {tactic_p2})")
    print("="*30)
    print(f"Speler 1 ({tactic_p1}) wint: {stats[1]} keer ({stats[1] / aantal_simulaties * 100:.2f}%)")
    print(f"Speler 2 ({tactic_p2}) wint: {stats[2]} keer ({stats[2] / aantal_simulaties * 100:.2f}%)")
    print(f"Gelijkspel: {' '*len(tactic_p2)} {stats[0]} keer ({stats[0] / aantal_simulaties * 100:.2f}%)")
    print("-"*30)
    print(f"Totale rekentijd: {elapsed_time:.4f} seconden")
    print("="*30)