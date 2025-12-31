import constants as const
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
        can_slide: It indicates that if a piece can move in a sliding fashion (Queen, Rook, Bishop) or not (King, Knight, Pawn).
    """

    def __init__(self, color: int, position: PositionTuple) -> None:
        self.symbol: str
        self.name: str
        self.is_moved: bool = False
        self.color: int = color
        self.position: PositionTuple = position
        self.can_slide: bool
        self.directions_to_get_possible_moves: list[str]
        self.values_to_calculate_possible_moves: list[PositionTuple]


class Empty(Piece):
    name: str = const.EMPTY_STR
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    color: int = const.EMPTY

    
    def __init__(self, color: int, position: PositionTuple):
        super().__init__(Empty.color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Empty.name]


class King(Piece):
    name: str = const.KING
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    can_slide: bool = False
    values_to_calculate_possible_moves: list[PositionTuple] = [
        PositionTuple((1, 0)),
        PositionTuple((-1, 0)),
        PositionTuple((0, 1)),
        PositionTuple((0, -1)),
        PositionTuple((1, 1)),
        PositionTuple((1, -1)),
        PositionTuple((-1, 1)),
        PositionTuple((-1, -1)),
    ]

    
    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][King.name]
        self.is_under_Check: bool = False
        self.Check_given_by: PositionTuple
   
    
    def pieces_to_get_possible_attacking_squares(self) -> list[Piece]:
        """
        Returns pieces which can be used to get all possible attacking squares.
        
        Returns:
            pieces_to_get_possible_attacking_squares: A list of all possible attacking squares grouped by direction.
        """
        pieces_to_get_possible_attacking_squares: list[Piece] = []

        for piece in [
            const.symbol_notation_and_material[const.NOTATION][self.color][const.QUEEN],
            const.symbol_notation_and_material[const.NOTATION][self.color][const.KNIGHT],
            const.symbol_notation_and_material[const.NOTATION][self.color][const.PAWN]
        ]:
            pieces_to_get_possible_attacking_squares.append(create_piece(piece, self.position))
        
        return pieces_to_get_possible_attacking_squares


class Queen(Piece):
    name: str = const.QUEEN
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    can_slide: bool = True
    directions_to_get_possible_moves: list[str] = const.ALL_DIRECTIONS


    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Queen.name]


class Rook(Piece):
    name: str = const.ROOK
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    can_slide: bool = True
    directions_to_get_possible_moves: list[str] = const.STRAIGHT_DIRECTIONS


    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Rook.name]


class Bishop(Piece):
    name: str = const.BISHOP
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    can_slide: bool = True
    directions_to_get_possible_moves: list[str] = const.DIAGONAL_DIRECTIONS


    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Bishop.name]


class Knight(Piece):
    name: str = const.KNIGHT
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    can_slide: bool = False
    values_to_calculate_possible_moves: list[PositionTuple] = [
        PositionTuple((2, 1)),
        PositionTuple((2, -1)),
        PositionTuple((-2, 1)),
        PositionTuple((-2, -1)),
        PositionTuple((1, 2)),
        PositionTuple((1, -2)),
        PositionTuple((-1, 2)),
        PositionTuple((-1, -2))
    ]


    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Knight.name]

class Pawn(Piece):
    name: str = const.PAWN
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]
    can_slide: bool = False


    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Pawn.name]
        self.values_to_calculate_possible_moves: list[PositionTuple] = [
            PositionTuple((-1, 0)),
            PositionTuple((-2, 0))
        ] if color == const.WHITE else [
            PositionTuple((1, 0)),
            PositionTuple((2, 0))
        ]
        self.values_to_calculate_possible_captures: list[PositionTuple] = [
            PositionTuple((-1, 1)),
            PositionTuple((-1, -1))
        ] if color == const.WHITE else [
            PositionTuple((1, 1)),
            PositionTuple((1, -1))
        ]

def create_piece(notation: str, position: PositionTuple) -> Piece:
    """Takes the notation and position as argument and creates a Piece according to it."""

    if notation in [
        const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.KING],
        const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.KING]
        ]:
        return King(const.WHITE if notation.isupper() else const.BLACK, position)
    
    elif notation in [
        const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.QUEEN],
        const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.QUEEN]
        ]:
        return Queen(const.WHITE if notation.isupper() else const.BLACK, position)
    
    elif notation in [
        const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.ROOK],
        const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.ROOK]
        ]:
        return Rook(const.WHITE if notation.isupper() else const.BLACK, position)
    
    elif notation in [
        const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.BISHOP],
        const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.BISHOP]
        ]:
        return Bishop(const.WHITE if notation.isupper() else const.BLACK, position)
    
    elif notation in [
        const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.KNIGHT],
        const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.KNIGHT]
        ]:
        return Knight(const.WHITE if notation.isupper() else const.BLACK, position)
    
    elif notation in [
        const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.PAWN],
        const.symbol_notation_and_material[const.NOTATION][const.BLACK][const.PAWN]
        ]:
        return Pawn(const.WHITE if notation.isupper() else const.BLACK, position)
    
    else:
        return Empty(const.EMPTY, position)
