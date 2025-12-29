import sys
import os

import constants as const
from board import Board
from inputs import input_str_to_movement_tuple
import errors



def main() -> None:
    if len(sys.argv) == 2:
        starting_fen = sys.argv[1]
    else:
        starting_fen = const.DEFAULT_FEN
    
    try:
        board = Board(starting_fen)
    except errors.InvalidFEN:
        print("Invalid FEN string passed.")
        exit(1)

    while True:
        clear_screen()
        board.display()

        while True:
            try:
                if board.grid[board.grid.king_position[board.active_color]].is_under_Check: #type: ignore
                    print(f"{const.RED}Your king is under Check!{const.RESET}")
                input_str: str = input("Enter the move to play or 'exit' to quit: ")
                if input_str.lower() == "exit":
                    sys.exit()
                board.move(input_str_to_movement_tuple(input_str))
            except errors.CustomException as e:
                print(f"{const.RED}{e}{const.RESET}")
            else:
                break


def clear_screen() -> None:
    """Clears the screen of the terminal."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    main()
