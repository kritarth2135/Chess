from typing import Any

import pieces
import helper
import errors

PositionTuple = helper.PositionTuple
MovementTuple = helper.MovementTuple

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
        """Prints the Chess Board in a Visually Good manner."""

        print("+---" * (helper.SIZE + 1), "+", sep="")
        for rank in range(helper.SIZE):
            print(f"| {helper.SIZE - rank} | ", end="")
            for file in range(helper.SIZE):
                print(self.grid.grid[rank][file].symbol, end = " | ")
            print()
            print("+---" * (helper.SIZE + 1), "+", sep="")
        print("|   | A | B | C | D | E | F | G | H |")
        print("+---" * (helper.SIZE + 1), "+", sep="")

    
    def valid_moves_from_possible_moves(self, piece: pieces.Piece) -> list[PositionTuple]:
        """Returns valid moves from possible moves according to current position of the board."""
        
        possible_moves: list[list[PositionTuple]] = piece.get_possible_moves()
        valid_moves: list[PositionTuple] = []
        
        if piece.name == pieces.PAWN:
            # Pawn is handled specially
            possible_moving_squares: list[PositionTuple] = possible_moves[0]
            possible_capturing_squares: list[PositionTuple] = possible_moves [1]

            for move in possible_moving_squares:
                if self.grid[move].name != pieces.EMPTY:
                    break
                valid_moves.append(move)
            
            for move in possible_capturing_squares:
                if self.grid[move].name != pieces.EMPTY and self.grid[move].color != piece.color:
                    valid_moves.append(move)
            
            return valid_moves
        
        else:
            for moves in possible_moves:
                for move in moves:
                    if self.grid[move].name != pieces.EMPTY:
                        if self.grid[move].color != piece.color:
                            valid_moves.append(move)
                        break
                    valid_moves.append(move)
            
            return valid_moves

    
    
    def move(self, movement: MovementTuple) -> None:
        """Moves the piece on movement.initial_position to movement.final_position if it is valid."""

        piece_to_move: pieces.Piece = self.grid[movement.initial_position]
        
        if piece_to_move.color == helper.EMPTY:
            raise errors.InvalidMove
        if piece_to_move.color != self.active_color:
            raise errors.InvalidTurn

        valid_moves: list[PositionTuple] = self.valid_moves_from_possible_moves(piece_to_move)
        
        if movement.final_position not in valid_moves:
            raise errors.InvalidMove

        self.grid[movement.final_position] = piece_to_move
        (
            self.grid[movement.final_position].position,
            self.grid[movement.final_position].is_moved,
            self.active_color
        ) = movement.final_position, True, (self.active_color + 1) % 2
        self.grid[movement.initial_position] = pieces.create_piece(pieces.EMPTY, movement.initial_position)

        piece_moved = self.grid[movement.final_position]
        attacked_squares: list[PositionTuple] = self.valid_moves_from_possible_moves(piece_moved)

        for position_of_king in self.grid.position_of_kings:
            if position_of_king in attacked_squares and self.grid[position_of_king].color != piece_moved.color:
                self.grid[position_of_king].is_under_check = True  # type: ignore
                self.grid[position_of_king].check_given_by = piece_moved.position  # type: ignore


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
        self.position_of_kings: list[PositionTuple] = []

        for rank in range(helper.SIZE):
            temp_list: list[pieces.Piece] = []

            for file in range(helper.SIZE):
                piece_notation = piece_placement[rank][file]
                position = PositionTuple((rank, file))
                
                temp_piece: pieces.Piece = pieces.create_piece(piece_notation, position)
                if temp_piece.name == pieces.KING:
                    self.position_of_kings.append(temp_piece.position)
                temp_list.append(temp_piece)

            self.grid.append(temp_list)
    
    def __getitem__(self, key: PositionTuple):
        """Returns the item from grid at position key."""

        return self.grid[key.rank][key.file]
    
    def __setitem__(self, key: PositionTuple, value: pieces.Piece):
        """Sets the key position of the grid to the value."""

        self.grid[key.rank][key.file] = value
