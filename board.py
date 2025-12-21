from typing import Any

from constants import *
from positions import PositionTuple, MovementTuple
from pieces import Piece, create_piece
import errors
import fen

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
        FEN_data: dict[str, Any] | None = fen.fen_parser(fen_string)
        if not FEN_data:
            raise errors.InvalidFEN
        
        self.active_color: int = FEN_data["active_color"]
        self.en_passant_squares: str = FEN_data["en_passant_squares"]
        self.halfmove_clock: int = FEN_data["halfmove_count"]
        self.fullmove_count: int = FEN_data["fullmove_count"]

        self.grid = Grid(FEN_data["piece_placement_data"])

        self.castling_availability: dict[str, bool] = {
            symbol_notation_and_material[NOTATION][WHITE][KING]: False,
            symbol_notation_and_material[NOTATION][WHITE][QUEEN]: False,
            symbol_notation_and_material[NOTATION][BLACK][KING]: False,
            symbol_notation_and_material[NOTATION][BLACK][QUEEN]: False
        }

        for castling, castling_availability in zip(list(self.castling_availability.keys()), FEN_data["castling_availability"]):
            if int(castling_availability) == 1:
                self.castling_availability[castling] = True
    
        
    def display(self) -> None:
        """Prints the Chess Board in a Visually Good manner."""

        print("+---" * (SIZE + 1), "+", sep="")
        for rank in range(SIZE):
            print(f"| {SIZE - rank} | ", end="")
            for file in range(SIZE):
                print(self.grid.grid[rank][file].symbol, end = " | ")
            print()
            print("+---" * (SIZE + 1), "+", sep="")
        print("|   | A | B | C | D | E | F | G | H |")
        print("+---" * (SIZE + 1), "+", sep="")

    
    def valid_moves_from_possible_moves(self, piece: Piece) -> list[PositionTuple]:
        """Returns valid moves from possible moves according to current position of the board."""
        
        possible_moves: list[list[PositionTuple]] = piece.get_possible_moves()
        valid_moves: list[PositionTuple] = []
        
        if piece.name == PAWN:
            # Pawn is handled specially
            possible_moving_squares: list[PositionTuple] = possible_moves[0]
            possible_capturing_squares: list[PositionTuple] = possible_moves [1]

            for move in possible_moving_squares:
                if self.grid[move].name != EMPTY_STR:
                    break
                valid_moves.append(move)
            
            for move in possible_capturing_squares:
                if self.grid[move].name != EMPTY_STR and self.grid[move].color != piece.color:
                    valid_moves.append(move)
            
            return valid_moves
        
        else:
            for moves in possible_moves:
                for move in moves:
                    if self.grid[move].name != EMPTY_STR:
                        if self.grid[move].color != piece.color:
                            valid_moves.append(move)
                        break
                    valid_moves.append(move)
            
            return valid_moves


    # def is_king_under_check(self, color: int) -> bool:
    #     for piece in symbol_notation_and_material[NOTATION][WHITE]:
    #         temp_piece: Piece = create_piece(piece, self.grid.king_position[color])
    #         attacked_by_squares: list[list[PositionTuple]] = temp_piece.get_possible_moves()

    #     return False
    
    
    def move(self, movement: MovementTuple) -> None:
        """Moves the piece on movement.initial_position to movement.final_position if it is valid."""

        piece_to_move: Piece = self.grid[movement.initial_position]
        
        if piece_to_move.color == EMPTY:
            raise errors.InvalidMove
        if piece_to_move.color != self.active_color:
            raise errors.InvalidTurn
        
        if self.grid[self.grid.king_position[self.active_color]].is_under_Check: # type: ignore
            print("\033[31mYour King is under Check!\033[0m")

        valid_moves: list[PositionTuple] = self.valid_moves_from_possible_moves(piece_to_move)
        
        if movement.final_position not in valid_moves:
            raise errors.InvalidMove

        self.grid[movement.final_position] = piece_to_move
        (
            self.grid[movement.final_position].position,
            self.grid[movement.final_position].is_moved,
            self.active_color
        ) = movement.final_position, True, (self.active_color + 1) % 2
        self.grid[movement.initial_position] = create_piece(symbol_notation_and_material[NOTATION][EMPTY][EMPTY_STR], movement.initial_position)


class Grid:
    """
    Create a SIZE x SIZE grid for the Chess Board.

    Args:
        piece_placement: Modified piece placement data from FEN string, where numbe of spaces are replaced with Es.
    
    Attributes:
        grid: A 2D list of Piece showing the state of the Chess Board.
    """

    def __init__(self, piece_placement: list[list[str]]) -> None:
        self.grid: list[list[Piece]] = []
        self.king_position: dict[int, PositionTuple] = {}

        for rank in range(SIZE):
            temp_list: list[Piece] = []

            for file in range(SIZE):
                piece_notation = piece_placement[rank][file]
                position = PositionTuple((rank, file))
                
                temp_piece: Piece = create_piece(piece_notation, position)
                if temp_piece.name == KING:
                    self.king_position[temp_piece.color] = temp_piece.position
                temp_list.append(temp_piece)

            self.grid.append(temp_list)
    
    def __getitem__(self, key: PositionTuple):
        """Returns the item from grid at position key."""

        return self.grid[key.rank][key.file]
    
    def __setitem__(self, key: PositionTuple, value: Piece):
        """Sets the key position of the grid to the value."""

        self.grid[key.rank][key.file] = value
