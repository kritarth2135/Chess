import pieces
import helper
import errors

class Board:
    """
    Create a Chess Board.

    Args:
        fen_string: FEN string stating the state of the board.
    """
    def __init__(self, fen_string: str):
        piece_placement, chance, castling, en_passant_squares, halfmove_clock, fullmove_count = fen_string.strip().split(" ")
        self.active_color: int = helper.WHITE if chance.lower() == "w" else helper.BLACK
        
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

        modified_piece_placement: list[str] = helper.number_of_spaces_to_Es_in_piece_position(piece_placement.split("/"))
        grid: list[list[pieces.Piece]] = []
        
        self.grid = grid

    def display(self) -> None:
        print("+---" * (helper.SIZE + 1), "+", sep="")
        print("|   | A | B | C | D | E | F | G | H |")
        print("+---" * (helper.SIZE + 1), "+", sep="")
        for rank in range(helper.SIZE):
            print(f"| {helper.SIZE - rank} | ", end="")
            for file in range(helper.SIZE):
                print(self.grid[rank][file].symbol, end = " | ")
            print()
            print("+---" * (helper.SIZE + 1), "+", sep="")

    def move(self, move: helper.MovementTuple) -> None:
        pass

class Grid:
    """
    Create a helper.SIZE by helper.SIZE grid for the Chess Board.

    Args:
        piece_placement: Modified piece placement data from FEN string, where numbe of spaces are replaced with Es.
    """
    def __init__(self, piece_placement: str) -> None:
        self.grid: list[list[pieces.Piece]] = []

        for rank in range(helper.SIZE):
            temp_list: list[pieces.Piece] = []
            for file in range(helper.SIZE):
                piece = piece_placement[rank][file]
                position = helper.PositionTuple((rank, file))
                
                if piece in ["K", "k"]:
                    temp_piece = pieces.King(helper.WHITE if piece.isupper() else helper.BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["Q", "q"]:
                    temp_piece = pieces.Queen(helper.WHITE if piece.isupper() else helper.BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["R", "r"]:
                    temp_piece = pieces.Rook(helper.WHITE if piece.isupper() else helper.BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["B", "b"]:
                    temp_piece = pieces.Bishop(helper.WHITE if piece.isupper() else helper.BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["N", "n"]:
                    temp_piece = pieces.Knight(helper.WHITE if piece.isupper() else helper.BLACK, position)
                    temp_list.append(temp_piece)

                elif piece in ["P", "p"]:
                    temp_piece = pieces.Pawn(helper.WHITE if piece.isupper() else helper.BLACK, position)
                    temp_list.append(temp_piece)

                else:
                    temp_piece = pieces.Empty(helper.EMPTY, position)
                    temp_list.append(temp_piece)

            self.grid.append(temp_list)