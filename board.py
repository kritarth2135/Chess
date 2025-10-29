import pieces
import helper

# Length of the square chess grid 
SIZE: int = 8
# Players
EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1

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
            match ch:
                case "K":
                    self.castling_availability[WHITE_KINGSIDE] = True
                case "Q":
                    self.castling_availability[WHITE_QUEENSIDE] = True
                case "k":
                    self.castling_availability[BLACK_KINGSIDE] = True
                case "q":
                    self.castling_availability[BLACK_QUEENSIDE] = True

        piece_placement: list[str] = helper.number_to_Es_in_board_state(board_state.split("/"))
        grid: list[list[pieces.Piece]] = []
        for rank in range(SIZE):
            temp_list: list[pieces.Piece] = []
            for file in range(SIZE):
                piece = piece_placement[rank][file]
                position = (rank, file)
                if piece in ["K", "k"]:
                    piece = pieces.King(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(piece)
                elif piece in ["Q", "q"]:
                    piece = pieces.Queen(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(piece)
                elif piece in ["R", "r"]:
                    piece = pieces.Rook(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(piece)
                elif piece in ["B", "b"]:
                    piece = pieces.Bishop(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(piece)
                elif piece in ["N", "n"]:
                    piece = pieces.Knight(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(piece)
                elif piece in ["P", "pieces"]:
                    piece = pieces.Pawn(WHITE if piece.isupper() else BLACK, position)
                    temp_list.append(piece)
                else:
                    piece = pieces.Empty(EMPTY, position)
                    temp_list.append(piece)
            grid.append(temp_list)
        self.grid = grid

    def display(self) -> None:
        print("+", "----" * SIZE, "+", sep="")
        for rank in range(SIZE):
            print(" | ", end="")
            for file in range(SIZE):
                print(self.grid[rank][file].symbol, end = " | ")
            print()
            print("+", "----" * SIZE, "+", sep="")

    def move(self):
        pass
