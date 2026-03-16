import argparse

import constants as const
from cli import main_cli
from gui import main_gui

class Args:
    def __init__(self) -> None:
        self.cli: bool
        self.fen: str

parser = argparse.ArgumentParser(
    prog="main.py"
)
args = Args()
parser.add_argument("fen",nargs="?", default=const.DEFAULT_FEN)
parser.add_argument("-c", "--cli", action="store_true", help="Add this flag to run this program in cli.")
parser.parse_args(namespace=args)


def main():
    if args.cli:
        main_cli(args.fen)
    else:
        main_gui(args.fen)


if __name__ == "__main__":
    main()