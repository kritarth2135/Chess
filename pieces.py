from constants import *
from positions import PositionTuple


class Piece:
    """
    Create a Piece object.

    Args:
        color: An integer constant representing the color of the Piece created.
        position: A PositionTuple indicating the position at which the piece to create on grid.

    Attributes:
        symbol: Icon used to display the piece in the terminal.
        name: The name of the piece.
        is_moved: Variable that represents if a piece is moved or not.
        color: The color of the piece.
        position: PositionTuple representing the position of the piece on the Board.
    """

    def __init__(self, color: int, position: PositionTuple) -> None:
        self.symbol: str
        self.name: str
        self.is_moved: bool = False
        self.color: int = color
        self.position: PositionTuple = position
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Queen, the Rook and the Bishop according to the rules of Chess.
        
        Returns:
            possible_moves: A list of possible moves grouped by direction.
        """

        
        possible_moves_per_direction: list[list[PositionTuple]] = []
        possible_directions: list[str] = []
        
        if self.name == QUEEN:
            possible_directions += ALL_DIRECTIONS
        elif self.name == ROOK:
            possible_directions += STRAIGHT_DIRECTIONS
        else:
            possible_directions += DIAGONAL_DIRECTIONS
        
        for direction in possible_directions:
            temp_list: list[PositionTuple] = []
            position: PositionTuple | None = self.position
            for _ in range(SIZE):
                relative_postion: PositionTuple | None = position.get_relative_position(direction)
                if relative_postion:
                    temp_list.append(relative_postion)
                    position = relative_postion
            possible_moves_per_direction.append(temp_list)
        
        return possible_moves_per_direction


# Subclasses for each piece type.

class Empty(Piece):
    name: str = EMPTY_STR
    material: int = symbol_notation_and_material[MATERIAL][name]
    color: int = EMPTY
    
    def __init__(self, color: int, position: PositionTuple):
        super().__init__(Empty.color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][Empty.name]

class King(Piece):
    name: str = KING
    material: int = symbol_notation_and_material[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][King.name]
        self.is_under_Check: bool = False
        self.Check_given_by: PositionTuple
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the King according to the rules of Chess.
        
        Returns:
            possible_moves: A list of single possible moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        for direction in ALL_DIRECTIONS:
            relative_postion = self.position.get_relative_position(direction)
            if relative_postion:
                temp_list: list[PositionTuple] = []
                temp_list.append(relative_postion)
                possible_moves.append(temp_list)

        return possible_moves
    
    # def get_possible_attacking_positions(self) -> list[list[PositionTuple]]:
    #     """
    #     Find all the possible positions from where the King can be attacked.

    #     Returns:
    #         possible_attacking_positions: A list of positions grouped by direction
    #     """

    #     possible_attacking_positions: list[list[PositionTuple]] = []
    #     temp_piece_1: Queen = Queen(EMPTY, self.position)
    #     temp_piece_2: Knight = Knight(EMPTY, self.position)
    #     temp_piece_3: Pawn = Pawn(EMPTY, self.position)

    #     possible_attacking_positions += temp_piece_1.get_possible_moves()
    #     possible_attacking_positions += temp_piece_2.get_possible_moves()

    #     # Because for a pawn attacking squares are in 1st index of the returned list
    #     possible_attacking_positions += [temp_piece_3.get_possible_moves()[1]]

    #     return possible_attacking_positions

class Queen(Piece):
    name: str = QUEEN
    material: int = symbol_notation_and_material[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][Queen.name]

class Rook(Piece):
    name: str = ROOK
    material: int = symbol_notation_and_material[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][Rook.name]

class Bishop(Piece):
    name: str = BISHOP
    material: int = symbol_notation_and_material[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][Bishop.name]

class Knight(Piece):
    name: str = KNIGHT
    material: int = symbol_notation_and_material[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][Knight.name]
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Knight according to the rules of Chess.
        
        Returns:
            possible_moves: A list of single possible moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        # straight moves before knight has to turn
        STRAIGHT_MOVES: int = 2
        
        for dir in STRAIGHT_DIRECTIONS:
            position = self.position
            for _ in range(STRAIGHT_MOVES): 
                if not position:
                    break
                relative_position = position.get_relative_position(dir)
                position = relative_position
            for inner_dir in STRAIGHT_DIRECTIONS:
                if not position:
                    break
                relative_position = position.get_relative_position(inner_dir)
                if relative_position:
                    if not relative_position.in_straight_direction(self.position):
                        temp_list: list[PositionTuple] = []
                        temp_list.append(relative_position)
                        possible_moves.append(temp_list)
        
        return possible_moves

class Pawn(Piece):
    name: str = PAWN
    material: int = symbol_notation_and_material[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = symbol_notation_and_material[SYMBOL][color][Pawn.name]
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Pawn according to the rules of Chess.
        
        Returns:
            possible_moves: A list of possible moves and capture moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        possible_no_of_moves: int = 1 if self.is_moved else 2
        direction: str = DOWN if self.color == BLACK else UP
        position = self.position
        moving_squares: list[PositionTuple] = []
        capturing_squares: list[PositionTuple] = []
        
        for i in range(possible_no_of_moves):
            relative_position = position.get_relative_position(direction)
            if relative_position:
                moving_squares.append(relative_position)
                position = relative_position
            if i == 0:
                for dir in [LEFT, RIGHT]:
                    capturing_square: PositionTuple | None = position.get_relative_position(dir)
                    if capturing_square:
                        capturing_squares.append(capturing_square)
    
        possible_moves.append(moving_squares)
        possible_moves.append(capturing_squares)
        return possible_moves


def create_piece(notation: str, position: PositionTuple) -> Piece:
    """Takes the notation and position as argument and creates a Piece according to it."""

    if notation in [symbol_notation_and_material[NOTATION][WHITE][KING], symbol_notation_and_material[NOTATION][BLACK][KING]]:
        return King(WHITE if notation.isupper() else BLACK, position)
    
    elif notation in [symbol_notation_and_material[NOTATION][WHITE][QUEEN], symbol_notation_and_material[NOTATION][BLACK][QUEEN]]:
        return Queen(WHITE if notation.isupper() else BLACK, position)
    
    elif notation in [symbol_notation_and_material[NOTATION][WHITE][ROOK], symbol_notation_and_material[NOTATION][BLACK][ROOK]]:
        return Rook(WHITE if notation.isupper() else BLACK, position)
    
    elif notation in [symbol_notation_and_material[NOTATION][WHITE][BISHOP], symbol_notation_and_material[NOTATION][BLACK][BISHOP]]:
        return Bishop(WHITE if notation.isupper() else BLACK, position)
    
    elif notation in [symbol_notation_and_material[NOTATION][WHITE][KNIGHT], symbol_notation_and_material[NOTATION][BLACK][KNIGHT]]:
        return Knight(WHITE if notation.isupper() else BLACK, position)
    
    elif notation in [symbol_notation_and_material[NOTATION][WHITE][PAWN], symbol_notation_and_material[NOTATION][BLACK][PAWN]]:
        return Pawn(WHITE if notation.isupper() else BLACK, position)
    
    else:
        return Empty(EMPTY, position)