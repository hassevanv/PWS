import os
import time
import importlib
import random
from multiprocessing import Pool, cpu_count

# Vaststellen welke velden nodig zijn voor winst
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

# Vaststellen wanneer er sprake is van winst
def check_big_win(big_board):
    for c in BIG_WIN_CONDITIONS:
        if big_board[c[0]] == big_board[c[1]] == big_board[c[2]] != 0: # Als drie velden op rij een gelijke waarde !=0 hebben is er sprake van winst
            return big_board[c[0]]
    return 0

def check_small_win(board, big_field):
    for c in SMALL_WIN_CONDITIONS:
        if board[big_field + c[0]] == board[big_field + c[1]] == board[big_field + c[2]] != 0: # Als drie velden op rij een gelijke waarde !=0 hebben is er sprake van winst
            return board[big_field + c[0]]
            
    if all(board[big_field + s] != 0 for s in range(1, 10)): # Als alle velden gevuld zijn, is de winst in het kleine veld voor degene met de meeste velden (>4)
        c1 = sum(1 for s in range(1, 10) if board[big_field + s] == 1)
        return 1 if c1 > 4 else 2  
    return 0

# runnen van een spel
def run_single_game(args):
    tactic_1_name, tactic_2_name = args
    
    # tactieken importeren vanuit de map "tactics"
    tactic_1 = importlib.import_module(f"tactics.{tactic_1_name}").choose_move # importeren van de tactiek van speler 1
    tactic_2 = importlib.import_module(f"tactics.{tactic_2_name}").choose_move # importeren van de tactiek van speler 2

    # bord en big_board vaststellen
    board = {big + small: 0 for big in range(10, 100, 10) for small in range(1, 10)} 
    big_board = {big: 0 for big in range(10, 100, 10)}
    current_player = 1 # speler 1 begint
    last_digit = None # er is nog geen last_digit

    while True:
        forced_section = None
        if last_digit is not None: # als er een last_digit is:
            potential_section = last_digit * 10 # is de section last_digit * 10, mits:
            section_is_full = all(board[potential_section + s] != 0 for s in range(1, 10)) # vaststellen of de section vol is
            if big_board[potential_section] == 0 and not section_is_full: # de section niet vol is of gewonnen is
                forced_section = potential_section
        
        if forced_section is None:
            any_moves_left = any(big_board[b] == 0 and board[b + s] == 0 for b in big_board for s in range(1, 10)) # vaststellen of er nog zetten mogelijk zijn
            if not any_moves_left: 
                    return 0 # als er geen zetten meer mogelijk zijn, is het gelijkspel

        if current_player == 1: # als speler 1 aan de beurt is
            chosen_section, a = tactic_1(board, big_board, forced_section) # haal het grote veld en de 'a' op uit de tactiek van speler 1
        else: # anders is speler 2 aan de beurt
            chosen_section, a = tactic_2(board, big_board, forced_section) # haal het grote veld en de 'a' op uit de tactiek van speler 2

        chosen_field = chosen_section + a # vaststellen van het gekozen veld
        board[chosen_field] = current_player # het gekozen veld invullen met de waarde van de speler

        if big_board[chosen_section] == 0: # als het grote veld nog niet gewonnen is (tegen bugs)
            winner_of_section = check_small_win(board, chosen_section) # vaststellen of er een winnaar is in het kleine veld
            if winner_of_section != 0: # als er een winnaar is in het kleine veld, invullen van de waarde van de winnaar in het grote veld
                big_board[chosen_section] = winner_of_section

        overall_winner = check_big_win(big_board) # vaststellen of er een winnaar is in het grote veld
        if overall_winner != 0: # als er een winnaar is in het grote veld, return de waarde van de winnaar
            return overall_winner

        last_digit = a # vaststellen van de last_digit voor de volgende ronde
        current_player = 2 if current_player == 1 else 1 # wisselen van speler

# vragen vooraf genereren
def get_available_tactics(): # ophalen van de beschikbare tactieken in de map "tactics"
    tactics_dir = os.path.join(os.path.dirname(__file__), "tactics")
    files = os.listdir(tactics_dir)
    tactics = [f[:-3] for f in files if f.endswith(".py") and f != "__init__.py"]
    return sorted(tactics)

def select_tactic(player_num, tactics_list): # printen van de beschikbare tactieken  
    print(f"\nBeschikbare tactieken voor Speler {player_num}:")
    for idx, name in enumerate(tactics_list, 1):
        print(f" [{idx}] {name}")
    
    while True: # vragen om een geldige keuze van de speler
        try:
            keuze = int(input(f"Kies tactiek voor Speler {player_num} (nummer): "))
            if 1 <= keuze <= len(tactics_list):
                return tactics_list[keuze - 1]
        except ValueError:
            pass
        print("Ongeldige keuze, probeer opnieuw.")

def ask_simulation_count(): # vragen om het aantal simulaties dat de gebruiker wil uitvoeren
    while True:
        try:
            aantal = int(input("\nHoeveel potjes wil je simuleren? "))
            if aantal > 0:
                return aantal
        except ValueError:
            pass
        print("Ongeldig aantal, vul een positief heel getal in.")

# tactieken importeren vanuit de map "tactics"
if __name__ == '__main__':
    available_tactics = get_available_tactics()
    if not available_tactics:
        print("Fout: Geen tactiek-bestanden gevonden in de map 'tactics/'!")
        exit()

    print("=== ULTIMATE TIC-TAC-TOE SIMULATOR ===") # tactieken inlezen
    tactic_p1 = select_tactic(1, available_tactics) # tactiek van speler 1 inlezen
    tactic_p2 = select_tactic(2, available_tactics) # tactiek van speler 2 inlezen
    
    aantal_simulaties = ask_simulation_count() # aantal simulaties inlezen

    # simulaties uitvoeren over alle CPU's
    cores = cpu_count()
    print(f"\n[INFO] Starten van {aantal_simulaties} potjes ({tactic_p1} VS {tactic_p2}) over {cores} cores...")
    
    start_time = time.time() # tijd bijhouden van de simulaties
    stats = {1: 0, 2: 0, 0: 0} # winst bijhouden, alle waarden beginnen op 0
    
    chunk = max(1, aantal_simulaties // (cores * 4)) # bepalen van de chunk size voor multiprocessing, zodat de taken gelijkmatig verdeeld worden over de cores
    game_args = [(tactic_p1, tactic_p2)] * aantal_simulaties # alle simulaties gelijk stellen, zodat elke simulatie dezelfde tactieken gebruikt

    # Multiprocessing Pool gebruiken om de simulaties parallel uit te voeren
    with Pool(processes=cores) as pool:
        results = pool.map(run_single_game, game_args, chunksize=chunk)
    
    # resultaten bijhouden van de simulaties
    for result in results:
        stats[result] += 1

    elapsed_time = time.time() - start_time # gebruikte tijd vaststellen
    
    # Printen van de resultaten
    print("\n" + "="*30) # lijn voor overzichtelijkheid
    print(f"RESULTATEN ({tactic_p1} vs {tactic_p2})") # tactieken
    print("="*30) # lijn voor overzichtelijkheid
    print(f"Totaal aantal simulaties: {aantal_simulaties}") # aantal simulaties
    print("-"*30) # lijn voor overzichtelijkheid
    print(f"Speler 1 ({tactic_p1}) wint: {stats[1]} keer ({stats[1] / aantal_simulaties * 100:.2f}%)") # hoeveelheid winst voor speler 1
    print(f"Speler 2 ({tactic_p2}) wint: {stats[2]} keer ({stats[2] / aantal_simulaties * 100:.2f}%)") # hoeveelheid winst voor speler 2
    print(f"Gelijkspel: {' '*len(tactic_p2)} {stats[0]} keer ({stats[0] / aantal_simulaties * 100:.2f}%)") # hoeveelheid gelijkspel
    print("-"*30) # lijn voor overzichtelijkheid
    print(f"Totale rekentijd: {elapsed_time:.4f} seconden") # totale rekentijd
    print("="*30) # lijn voor overzichtelijkheid