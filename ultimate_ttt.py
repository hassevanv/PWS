import random
import time

class UltimateTicTacToe:
    def __init__(self):
        # 9 kleine borden van elk 9 vakjes
        self.big_board = [[" " for _ in range(9)] for _ in range(9)]
        # De status van de 9 grote vakken (wie heeft het kleine bord gewonnen?)
        self.meta_board = [" " for _ in range(9)]
        # Welk bord de volgende speler MOET spelen (-1 betekent vrije keuze)
        self.next_small_board = -1
        self.turn = "X"

    def check_winner(self, board):
        win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for qc in win_conditions:
            if board[qc[0]] == board[qc[1]] == board[qc[2]] != " " and board[qc[0]] != "D":
                return board[qc[0]]
        if " " not in board:
            return "D" # Draw / Gelijkspel
        return None

    def get_legal_moves(self):
        moves = []
        if self.next_small_board != -1 and self.meta_board[self.next_small_board] == " ":
            active_boards = [self.next_small_board]
        else:
            active_boards = [i for i, x in enumerate(self.meta_board) if x == " "]

        for b_idx in active_boards:
            for s_idx in range(9):
                if self.big_board[b_idx][s_idx] == " ":
                    moves.append((b_idx, s_idx))
        return moves

    def play_move(self, board_idx, slot_idx):
        self.big_board[board_idx][slot_idx] = self.turn
        winner = self.check_winner(self.big_board[board_idx])
        if winner:
            self.meta_board[board_idx] = winner
        
        if self.meta_board[slot_idx] == " ":
            self.next_small_board = slot_idx
        else:
            self.next_small_board = -1
            
        self.turn = "O" if self.turn == "X" else "X"

def simuleer_spel():
    game = UltimateTicTacToe()
    while True:
        moves = game.get_legal_moves()
        if not moves: break
        
        move = random.choice(moves)
        game.play_move(move[0], move[1])
        
        res = game.check_winner(game.meta_board)
        if res: return res
    return "Gelijkspel"

def simulate_games(n):
    """Deze functie wordt aangeroepen door de web-interface"""
    stats = {"X": 0, "O": 0, "Draw": 0}
    for _ in range(n):
        winnaar = simuleer_spel()
        if winnaar == "X":
            stats["X"] += 1
        elif winnaar == "O":
            stats["O"] += 1
        else:
            stats["Draw"] += 1
    return stats

if __name__ == "__main__":
    # Dit draait alleen als je het bestand direct opent met 'python3 ultimate_ttt.py'
    aantal = 5000
    start = time.time()
    res = simulate_games(aantal)
    duur = time.time() - start
    print(f"Klaar! X: {res['X']} | O: {res['O']} | Draw: {res['Draw']} ({aantal/duur:.0f} p/s)")