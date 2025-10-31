from board import Board
import helper
import errors
import os
import sys

STARTING_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def main() -> None:
    if len(sys.argv) > 1:
        starting_fen = sys.argv[1]
    else:
        starting_fen = STARTING_FEN
    
    board = Board(starting_fen)
    while True:
        clear_screen()
        board.display()
        
        while True:
            try:
                input_str: str = input("Enter the move to play: ")
                board.move(helper.input_str_to_movement_tuple(input_str))
            except errors.InvalidInput:
                print("Format to enter input: \"<starting_square>,<ending_square>\"")
            except errors.InvalidMove:
                print("This move is illegal.")
            else:
                break

def clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    main()
