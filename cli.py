import sys
import os

from board import Board
import constants as const
import errors
from inputs import input_str_to_movement_tuple
from positions import MovementTuple


def main_cli(starting_fen: str) -> None:
    """Runs the game in CLI interface."""

    try:
        board = Board(starting_fen)
    except errors.InvalidFEN:
        print("Invalid FEN string passed.")
        sys.exit(1)

    while True:
        # clear_screen()
        board.display()

        while True:
            try:
                input_str: str = input("Enter the move to play, 'exit' to quit or 'undo'/'u' to undo: ")
                if input_str.lower() == "exit":
                    sys.exit()
                elif input_str.lower() == "u" or input_str.lower() == "undo":
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
