from typing import Any

import pieces
import helper
import errors

class Board:
    """
    Create a Chess Board.

    Args:
        fen_string: FEN string stating the state of the board.
    
    Attributes:
        grid: A Grid object representing the state of the board.
        active_color: The color whose turn is right now.
        castling_availability: A dictionary of bools for all four possible castles.
        en_passant_squares: A string containing all the squares on which a pawn can move to make an en passant capture.
        halfmove_count: The number of halfmoves.
        fullmove_count: The number of fullmoves.
    """

    def __init__(self, fen_string: str) -> None:
        FEN_data: dict[str, Any] | None = helper.fen_parser(fen_string)
        if not FEN_data:
            raise errors.InvalidFEN
        
        self.active_color: int = FEN_data["active_color"]
        self.en_passant_squares: str = FEN_data["en_passant_squares"]
        self.halfmove_clock: int = FEN_data["halfmove_count"]
        self.fullmove_count: int = FEN_data["fullmove_count"]

        self.grid = Grid(FEN_data["piece_placement_data"])

        self.castling_availability: dict[str, bool] = {
            pieces.pieces[pieces.NOTATION][helper.WHITE][pieces.KING]: False,
            pieces.pieces[pieces.NOTATION][helper.WHITE][pieces.QUEEN]: False,
            pieces.pieces[pieces.NOTATION][helper.BLACK][pieces.KING]: False,
            pieces.pieces[pieces.NOTATION][helper.BLACK][pieces.QUEEN]: False
        }

        for castling, castling_availability in zip(list(self.castling_availability.keys()), FEN_data["castling_availability"]):
            if int(castling_availability) == 1:
                self.castling_availability[castling] = True
        
    def display(self) -> None:
        print("+---" * (helper.SIZE + 1), "+", sep="")
        print("|   | A | B | C | D | E | F | G | H |")
        print("+---" * (helper.SIZE + 1), "+", sep="")
        for rank in range(helper.SIZE):
            print(f"| {helper.SIZE - rank} | ", end="")
            for file in range(helper.SIZE):
                print(self.grid.grid[rank][file].symbol, end = " | ")
            print()
            print("+---" * (helper.SIZE + 1), "+", sep="")
        print()

    def move(self, movement: helper.MovementTuple) -> None:
        piece_moved: pieces.Piece = self.grid[movement.initial_position]
        if piece_moved.color != self.active_color:
            raise errors.InvalidTurn

        valid_moves: list[list[helper.PositionTuple]] = piece_moved.get_valid_moves()
        
        if piece_moved.name == pieces.PAWN:
            # Pawn is handled specially
            moving_squares: list[helper.PositionTuple] = valid_moves[0]
            capturing_squares: list[helper.PositionTuple] = valid_moves [1]

            if self.grid[movement.final_position].name == pieces.EMPTY:
                if movement.final_position not in moving_squares:
                    raise errors.InvalidMove
            else:
                if movement.final_position not in capturing_squares:
                    raise errors.InvalidMove
        
        else:
            if not any(movement.final_position in moves for moves in valid_moves):
                raise errors.InvalidMove
                
            for moves in valid_moves:
                for i in range(len(moves)):
                    if moves[i] == movement.final_position:
                        for j in range(i):
                            if self.grid[moves[j]].name != pieces.EMPTY:
                                raise errors.InvalidMove
        
        self.grid[movement.final_position] = piece_moved
        (
            self.grid[movement.final_position].position,
            self.grid[movement.final_position].is_moved,
            self.active_color
        ) = movement.final_position, True, (self.active_color + 1) % 2
        self.grid[movement.initial_position] = pieces.create_piece(pieces.EMPTY, movement.initial_position)


class Grid:
    """
    Create a helper.SIZE by helper.SIZE grid for the Chess Board.

    Args:
        piece_placement: Modified piece placement data from FEN string, where numbe of spaces are replaced with Es.
    
    Attributes:
        grid: A 2D list of Piece showing the state of the Chess Board.
    """

    def __init__(self, piece_placement: list[list[str]]) -> None:
        self.grid: list[list[pieces.Piece]] = []

        for rank in range(helper.SIZE):
            temp_list: list[pieces.Piece] = []

            for file in range(helper.SIZE):
                piece_notation = piece_placement[rank][file]
                position = helper.PositionTuple((rank, file))
                
                temp_piece: pieces.Piece = pieces.create_piece(piece_notation, position)
                temp_list.append(temp_piece)

            self.grid.append(temp_list)
    
    def __getitem__(self, key: helper.PositionTuple):
        """Returns the item from grid at position key."""

        return self.grid[key.rank][key.file]
    
    def __setitem__(self, key: helper.PositionTuple, value: pieces.Piece):
        """Sets the key position of the grid to the value."""

        self.grid[key.rank][key.file] = value
