import sys
import os

import constants as const
from board import Board
from inputs import input_str_to_movement_tuple
import errors



def main_cli(starting_fen: str) -> None:
    try:
        board = Board(starting_fen)
    except errors.InvalidFEN:
        print("Invalid FEN string passed.")
        sys.exit(1)

    while True:
        # clear_screen()
        board.display()

        if board.grid[board.grid.king_position[board.active_color]].is_under_Check: #type: ignore
            print(f"{const.RED}Your king is under Check!{const.RESET}")

        while True:
            try:
                input_str: str = input("Enter the move to play, 'exit' to quit or 'undo' to undo: ")
                if input_str.lower() == "exit":
                    sys.exit()
                elif input_str.lower() == "undo":
                    board.undo()
                else:
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
    main_cli(const.DEFAULT_FEN)
