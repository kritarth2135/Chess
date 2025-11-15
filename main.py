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
                if board.grid[board.grid.king_position[board.active_color]].is_under_Check: # type: ignore
                    print("\033[31mYour King is under Check!\033[0m")
                
                input_str: str = input("Enter the move to play or 'exit' to quit: ")
                if input_str.lower() == "exit":
                    sys.exit()
                board.move(helper.input_str_to_movement_tuple(input_str))
            except errors.InvalidTurn:
                print(f"\033[31mIt is {"White" if board.active_color == helper.WHITE else "Black"}'s turn.\033[0m")
            except Exception as e:
                print(f"\033[31m{e}\033[0m")
            else:
                break

if __name__ == "__main__":
    main()
