from typing import Any

import constants as const
from positions import PositionTuple, MovementTuple
from pieces import Piece, King, Pawn, Empty, create_piece
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
        captured_pieces: List of captured pieces including empty pieces.
        move_history: List of MovementTuples to track previous moves.
    """
    def __init__(self, fen_string: str) -> None:
        FEN_data: dict[str, Any] | None = fen.fen_parser(fen_string)
        if not FEN_data:
            raise errors.InvalidFEN
        
        self.active_color: int = FEN_data["active_color"]
        self.en_passant_squares: str = FEN_data["en_passant_squares"]
        self.halfmove_count: int = FEN_data["halfmove_count"]
        self.fullmove_count: int = FEN_data["fullmove_count"]

        self.grid = Grid(FEN_data["piece_placement_data"])

        self.castling_availability: dict[str, bool] = {
            const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.QUEEN]: False,
            const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.KING]: False,
            const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.KING]: False,
            const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.QUEEN]: False
        }

        for castling, castling_availability in zip(list(self.castling_availability.keys()), FEN_data["castling_availability"]):
            if int(castling_availability) == 1:
                self.castling_availability[castling] = True
        
        self.captured_pieces: list[Piece] = []
        self.move_history: list[MovementTuple] = []
    
        
    def display(self) -> None:
        """Prints the Chess Board in a Visually Good manner."""

        print(f"{const.DIM}┌───┬───┬───┬───┬───┬───┬───┬───┬───┐{const.RESET}")
        for rank in range(const.GRID_SIZE):
            print(f"{const.DIM}│ {const.GRID_SIZE - rank} │ {const.RESET}", end="")
            for file in range(const.GRID_SIZE):
                print(f"{const.BOLD}{self.grid.array[rank][file].symbol}{const.RESET}", end = f"{const.DIM} │ {const.RESET}")
            print()
            print(f"{const.DIM}├───┼───┼───┼───┼───┼───┼───┼───┼───┤{const.RESET}")
        print(f"{const.DIM}│   │ A │ B │ C │ D │ E │ F │ G │ H │{const.RESET}")
        print(f"{const.DIM}└───┴───┴───┴───┴───┴───┴───┴───┴───┘{const.RESET}")


    def get_legal_moves(self, piece: Piece) -> list[PositionTuple]:
        legal_moves: list[PositionTuple] = []
        position: PositionTuple = piece.position
        
        if piece.can_slide:
            directions: list[str] = piece.directions_to_get_possible_moves

            for direction in directions:
                move: PositionTuple = position.get_relative_position(direction)
                while not move.is_out_of_bounds():
                    if self.grid[move].color != const.EMPTY:
                        if self.grid[move].color != piece.color:
                            legal_moves.append(move)
                        break
                    legal_moves.append(move)
                    move = move.get_relative_position(direction)
        
        elif isinstance(piece, Pawn):
            values: list[PositionTuple] = piece.values_to_calculate_possible_moves
            upper_bound: int = len(values) - 1 if piece.is_moved else len(values)
            for value in values[:upper_bound]:
                move: PositionTuple = position + value
                if not move.is_out_of_bounds():
                    if self.grid[move].color == const.EMPTY:
                        legal_moves.append(move)
            values = piece.values_to_calculate_possible_captures
            for value in values:
                move: PositionTuple = position + value
                if not move.is_out_of_bounds():
                    if self.grid[move].color == (piece.color + 1) % 2:
                        legal_moves.append(move)

        else:
            values: list[PositionTuple] = piece.values_to_calculate_possible_moves

            for value in values:
                move: PositionTuple = position + value
                if not move.is_out_of_bounds():
                    if self.grid[move].color == piece.color:
                        continue
                    legal_moves.append(move)
        
        return legal_moves


    def attacked_by_square(self, attacked_square: PositionTuple, attacked_by_square: PositionTuple) -> bool:
        """Returns True if the attacked_square is attacked by the attacked_by_square."""

        if self.grid[attacked_by_square].color == const.EMPTY:
            return False
        if self.grid[attacked_square].color != self.grid[attacked_by_square].color:
            if isinstance(self.grid[attacked_by_square], Pawn):
                attacked_squares: list[PositionTuple] = []
                for square in self.get_legal_moves(self.grid[attacked_by_square]):
                    if not square.in_straight_direction(attacked_by_square):
                        attacked_squares.append(square)
            else:
                attacked_squares: list[PositionTuple] = self.get_legal_moves(self.grid[attacked_by_square])
            if attacked_square in attacked_squares:
                return True
        return False
    

    def update_is_under_Check(self, king: King) -> None:
        king.is_under_Check = False
        for piece in king.pieces_to_get_possible_attacking_squares():
            for square in self.get_legal_moves(piece):
                if self.attacked_by_square(king.position, square):
                    king.is_under_Check = True
                    return


    def move(self, movement: MovementTuple) -> None:
        """Moves the piece on movement.initial_position to movement.final_position if it is valid."""

        piece_to_move: Piece = self.grid[movement.initial_position]

        if piece_to_move.color == const.EMPTY:
            raise errors.InvalidMove
        if piece_to_move.color != self.active_color:
            raise errors.InvalidTurn
        
        legal_moves: list[PositionTuple] = self.get_legal_moves(piece_to_move)
        
        if movement.final_position not in legal_moves:
            raise errors.InvalidMove

        self.make_move(movement)

        for king_position in self.grid.king_position.values():
            self.update_is_under_Check(self.grid[king_position]) #type: ignore

        active_players_king: King = self.grid[self.grid.king_position[self.active_color]] #type: ignore
        if active_players_king.is_under_Check:
            self.make_move(MovementTuple((movement.final_position, movement.initial_position)))
            raise errors.KingStillUnderCheck
        
        self.active_color = (self.active_color + 1) % 2
        self.halfmove_count += 1
        if self.active_color == const.BLACK:
            self.fullmove_count += 1


    def make_move(self, movement: MovementTuple) -> None:
        self.captured_pieces.append(self.grid[movement.final_position])

        self.grid[movement.final_position] = self.grid[movement.initial_position]
        (
            self.grid[movement.final_position].position,
            self.grid[movement.final_position].is_moved
        ) = movement.final_position, True

        if isinstance(self.grid[movement.final_position], King):
            self.grid.king_position[self.grid[movement.final_position].color] = movement.final_position

        self.grid[movement.initial_position] = create_piece(
            const.symbol_notation_and_material[const.NOTATION][const.EMPTY][const.EMPTY_STR],
            movement.initial_position
        )

        self.move_history.append(movement)
    

    def undo(self) -> None:
        if not self.move_history:
            raise errors.NoMoreUndos
        movement: MovementTuple = self.move_history.pop()

        self.grid[movement.initial_position] = self.grid[movement.final_position]
        self.grid[movement.final_position] = self.captured_pieces.pop()



class Grid:
    """
    Create a GRID_SIZE x GRID_SIZE grid for the Chess Board.

    Args:
        piece_placement: Modified piece placement data from FEN string, where numbe of spaces are replaced with Es.
    
    Attributes:
        grid: A 2D list of Piece showing the state of the Chess Board.
    """
    def __init__(self, piece_placement: list[list[str]]) -> None:
        self.array: list[list[Piece]] = []
        self.king_position: dict[int, PositionTuple] = {}

        for rank in range(const.GRID_SIZE):
            temp_list: list[Piece] = []

            for file in range(const.GRID_SIZE):
                piece_notation = piece_placement[rank][file]
                position = PositionTuple((rank, file))
                
                temp_piece: Piece = create_piece(piece_notation, position)
                if isinstance(temp_piece, King):
                    self.king_position[temp_piece.color] = temp_piece.position
                temp_list.append(temp_piece)

            self.array.append(temp_list)
    

    def __getitem__(self, key: PositionTuple):
        """Returns the item from grid at position key."""

        return self.array[key.rank][key.file]
    

    def __setitem__(self, key: PositionTuple, value: Piece):
        """Sets the key position of the grid to the value."""

        self.array[key.rank][key.file] = value
