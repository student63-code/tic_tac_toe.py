#!/usr/bin/env python3
"""
Enhanced Tic Tac Toe Game with Colorful UI
Console version showing player markers on the left side with improved UX.
"""

import os
import random

# ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(player1, player2):
    """Print the game header with player markers."""
    print("\n" + "=" * 50)
    print(f"    {CYAN}TIC TAC TOE{RESET}  -  {YELLOW}{player1} (X) vs {player2} (O){RESET}")
    print("=" * 50 + "\n")

def create_board():
    """Create an empty Tic Tac Toe board."""
    return [' '] * 9

def print_board(board, current_player, player1, player2):
    """Print the Tic Tac Toe board with player markers."""
    # Show current player marker
    player_marker = f"{player1}: {GREEN}X{RESET}" if current_player == 'X' else f"{player2}: {BLUE}O{RESET}"
    print(f"\n{MAGENTA}Current Turn: {player_marker}{RESET}\n")
    
    # Board with coordinates
    print("    1       2       3")
    print("  ┌───────┬───────┬───────┐")
    for row in range(3):
        row_cells = []
        for col in range(3):
            cell_value = board[row * 3 + col]
            if cell_value == 'X':
                row_cells.append(f"   {GREEN}{cell_value}{RESET}   ")
            elif cell_value == 'O':
                row_cells.append(f"   {BLUE}{cell_value}{RESET}   ")
            else:
                row_cells.append("       ")
        print(f"{row+1} │" + "│".join(row_cells) + "│")
        if row < 2:
            print("  ├───────┼───────┼───────┤")
    print("  └───────┴───────┴───────┘\n")

def is_winner(board, player):
    """Check if the specified player has won."""
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in wins)

def is_board_full(board):
    """Check if the board is full."""
    return all(cell != ' ' for cell in board)

def get_player_move(board, player_name, mark):
    """Get player move with improved validation."""
    while True:
        try:
            move = input(f"{player_name}'s turn ({mark}) - Enter move (row,col): ").strip()
            if move.lower() in ('q', 'quit', 'exit'):
                print("Exiting game. Goodbye!")
                exit(0)
                
            row_str, col_str = move.split(',')
            row = int(row_str) - 1
            col = int(col_str) - 1
            
            if row not in range(3) or col not in range(3):
                print(f"{RED}Invalid input. Rows and columns must be 1-3.{RESET}")
                continue
                
            idx = row * 3 + col
            if board[idx] != ' ':
                print(f"{RED}That cell is taken. Try again.{RESET}")
                continue
                
            return idx
        except ValueError:
            print(f"{RED}Invalid format. Use 'row,col' (e.g., '1,2'){RESET}")
            continue

def get_ai_move(board):
    """Get AI move with basic intelligence."""
    # First check for winning moves
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if is_winner(board, 'O'):
                board[i] = ' '
                return i
            board[i] = ' '
    
    # Then block opponent winning moves
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if is_winner(board, 'X'):
                board[i] = ' '
                return i
            board[i] = ' '
    
    # Try to take center
    if board[4] == ' ':
        return 4
        
    # Try to take corners
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for i in corners:
        if board[i] == ' ':
            return i
            
    # Take any remaining space
    available = [i for i in range(9) if board[i] == ' ']
    return random.choice(available)

def play_game(player1, player2, is_ai=False):
    """Main game loop."""
    board = create_board()
    current_player = 'X'
    scores = {player1: 0, player2: 0}
    game_history = []

    while True:
        clear_console()
        print_header(player1, player2)
        print_board(board, current_player, player1, player2)

        # Get move
        if current_player == 'X':
            move = get_player_move(board, player1, 'X')
        else:
            move = get_ai_move(board) if is_ai else get_player_move(board, player2, 'O')
        
        board[move] = current_player
        game_history.append((current_player, move))
        
        # Check win/tie conditions
        if is_winner(board, current_player):
            clear_console()
            print_header(player1, player2)
            print_board(board, current_player, player1, player2)
            winner = player1 if current_player == 'X' else player2
            print(f"{GREEN}🎉 {winner} ({current_player}) wins! 🎉{RESET}\n")
            scores[winner] += 1
            break
            
        if is_board_full(board):
            clear_console()
            print_header(player1, player2)
            print_board(board, current_player, player1, player2)
            print(f"{YELLOW}⚠️  It's a tie! ⚠️{RESET}\n")
            break
            
        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'

    print(f"{MAGENTA}Match Score:{RESET}")
    print(f"  {player1} (X): {scores[player1]}")
    print(f"  {player2} (O): {scores[player2]}\n")
    
    replay = input("Play again? (y/n): ").lower()
    if replay == 'y':
        play_game(player1, player2, is_ai)
    else:
        print("\nThanks for playing!")
        print("Final Scores:")
        print(f"  {player1}: {scores[player1]}")
        print(f"  {player2}: {scores[player2]}")
        exit()

def main():
    """Game setup and entry point."""
    clear_console()
    print(f"{CYAN}🔥 TIC TAC TOE 🔥{RESET}")
    print("=" * 50 + "\n")
    
    mode = input("Choose mode:\n1. Two Players\n2. Play vs AI\nSelect (1-2): ").strip()
    
    if mode == '1':
        player1 = input("Player 1 name (X): ").strip() or "Player 1"
        player2 = input("Player 2 name (O): ").strip() or "Player 2"
        play_game(player1, player2)
    elif mode == '2':
        player1 = input("Your name (X): ").strip() or "Player"
        player2 = "Computer"
        play_game(player1, player2, True)
    else:
        print(f"{RED}Invalid choice. Exiting.{RESET}")
        exit()

if __name__ == "__main__":
    main()
