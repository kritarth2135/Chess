import pieces
import helper
import errors
import random

SIZE: int = helper.SIZE
EMPTY: int = helper.EMPTY
WHITE: int = helper.WHITE
BLACK: int = helper.BLACK

# Casling availability indexes
WHITE_KINGSIDE: int = 0
WHITE_QUEENSIDE: int = 1
BLACK_KINGSIDE: int = 2
BLACK_QUEENSIDE: int = 3

class Board:
    def __init__(self, fen_string: str):
        board_state, chance, castling, en_passant_squares, halfmove_clock, fullmove_count = fen_string.strip().split(" ")
        self.active_color: int = WHITE if chance.lower() == "w" else BLACK
        
        self.en_passant_squares = en_passant_squares
        self.halfmove_clock = halfmove_clock
        self.fullmove_count = fullmove_count
        
        self.castling_availability: list[bool] = [False, False, False, False]
        for ch in castling:
            if ch == "K":
                self.castling_availability[WHITE_KINGSIDE] = True
            
            elif ch == "Q":
                self.castling_availability[WHITE_QUEENSIDE] = True
            
            elif ch == "k":
                self.castling_availability[BLACK_KINGSIDE] = True

            elif ch == "q":
                self.castling_availability[BLACK_QUEENSIDE] = True

        piece_placement: list[str] = helper.number_of_spaces_to_Es_in_piece_position(board_state.split("/"))
        grid: list[list[pieces.Piece]] = []
        for rank in range(SIZE):
            temp_list: list[pieces.Piece] = []
            for file in range(SIZE):
                piece = piece_placement[rank][file]
                position = helper.PositionTuple((rank, file))
                
                if piece in ["K", "k"]:
                    temp_piece = pieces.King(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["Q", "q"]:
                    temp_piece = pieces.Queen(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["R", "r"]:
                    temp_piece = pieces.Rook(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["B", "b"]:
                    temp_piece = pieces.Bishop(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["N", "n"]:
                    temp_piece = pieces.Knight(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["P", "p"]:
                    temp_piece = pieces.Pawn(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(temp_piece)

                else:
                    temp_piece = pieces.Empty(EMPTY, position)
                    temp_list.append(temp_piece)

            grid.append(temp_list)
        self.grid = grid

    def display(self) -> None:
        print("+---" * (SIZE + 1), "+", sep="")
        print("|   | A | B | C | D | E | F | G | H |")
        print("+---" * (SIZE + 1), "+", sep="")
        for rank in range(SIZE):
            print(f"| {SIZE - rank} | ", end="")
            for file in range(SIZE):
                print(self.grid[rank][file].symbol, end = " | ")
            print()
            print("+---" * (SIZE + 1), "+", sep="")

    def move(self, move: helper.MovementTuple) -> None:
        pass
