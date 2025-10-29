from board import Board

STARTING_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

board = Board(STARTING_FEN)
board.display()