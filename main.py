from board import Board
import helper
import errors
import sys

NEW_GAME_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def main() -> None:
    if len(sys.argv) == 2:
        starting_fen = sys.argv[1]
    else:
        starting_fen = NEW_GAME_FEN
    
    try:
        board = Board(starting_fen)
    except errors.InvalidFEN:
        print("Invalid FEN string passed.")
        exit(1)

    while True:
        helper.clear_screen()
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

if __name__ == "__main__":
    main()
