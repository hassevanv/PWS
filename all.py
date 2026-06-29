import time
import main

def select_simulation_tactics(position_name, full_list):
    print(f"\nWelke tactieken moeten meedoen als {position_name}?")
    print(" [0] ALLES (Volledige lijst)")
    for idx, name in enumerate(full_list, 1):
        print(f" [{idx}] {name}")
        
    while True:
        try:
            keuze = input(f"Kies nummers (bijv. '1' of '1,3' of '0' voor alles): ").strip()
            if keuze == '0' or keuze == '':
                return full_list
                
            # Splits invoer op komma's voor het geval je er meerdere kiest
            gekozen_indices = [int(x.strip()) for x in keuze.split(',')]
            valid_selection = []
            
            for idx in gekozen_indices:
                if 1 <= idx <= len(full_list):
                    valid_selection.append(full_list[idx - 1])
                    
            if valid_selection:
                return valid_selection
        except ValueError:
            pass
        print("Ongeldige keuze. Voer '0' in voor alles, of nummers gescheiden door een komma (bijv: 1,3).")

if __name__ == '__main__':
    # 1. Haal alle beschikbare tactieken op uit de config van main.py
    all_tactics = main.get_available_tactics()
    if not all_tactics:
        print("Geen tactieken gevonden om een simulatie mee te starten!")
        exit()
        
    print("=== ULTIMATE TIC-TAC-TOE simulatie (CUSTOMIZED) ===")
    
    # Selecteer de filters voor Speler 1 en Speler 2
    s1_tactics = select_simulation_tactics("Speler 1 (S1)", all_tactics)
    s2_tactics = select_simulation_tactics("Speler 2 (S2)", all_tactics)
    
    aantal_per_simulatie = main.ask_simulation_count()
    start_simulatie = time.time()
    
    # Matrix om de resultaten in op te slaan (dynamisch op basis van selectie)
    resultaten = {t1: {t2: {1: 0, 2: 0, 0: 0} for t2 in s2_tactics} for t1 in s1_tactics}

    # 2. Run de geselecteerde combinaties
    for t1 in s1_tactics:
        for t2 in s2_tactics:
            print(f"\n[SIMULATIE] {t1} (S1) VS {t2} (S2) starten...")
            
            cores = main.cpu_count()
            chunk = max(1, aantal_per_simulatie // (cores * 4))
            game_args = range(aantal_per_simulatie)

            with main.Pool(processes=cores, initializer=main.init_worker, initargs=(t1, t2)) as pool:
                match_results = pool.map(main.run_single_game, game_args, chunksize=chunk)
            
            # Resultaten tellen
            for r in match_results:
                resultaten[t1][t2][r] += 1

    # printen van de resultaten
    print("\n" + "="*80)
    print("EINDRESULTATEN simulatie (Winst S1% / Winst S2% / Gelijk%)")
    print("="*80)
    
    header = f"{'S1 ╲ S2':<12}"
    for t2 in s2_tactics:
        header += f"│ {t2:<18}"
    print(header)
    print("─"*12 + "┼" + "────────────────────┼"*len(s2_tactics))

    for t1 in s1_tactics:
        row = f"{t1:<12}"
        for t2 in s2_tactics:
            res = resultaten[t1][t2]
            w1 = (res[1] / aantal_per_simulatie) * 100
            w2 = (res[2] / aantal_per_simulatie) * 100
            d  = (res[0] / aantal_per_simulatie) * 100
            row += f"│ {w1:>4.2f}% / {w2:>4.2f}% / {d:>3.2f}% "
        print(row)
        
    print("="*80)
    print(f"simulatie succesvol afgerond in {time.time() - start_simulatie:.2f} seconden!")
    print("="*80)