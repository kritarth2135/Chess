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
    """

    def __init__(self, color: int, position: PositionTuple) -> None:
        self.symbol: str
        self.name: str
        self.is_moved: bool = False
        self.color: int = color
        self.position: PositionTuple = position
        # self._attacked_squares: list[list[PositionTuple]]
    

    # @property
    # def attacked_squares(self):
    #     return self._attacked_squares
    
    # @attacked_squares.setter
    # def attacked_squares(self):
    #     self._attacked_squares = self.get_possible_moves()

    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Queen, the Rook and the Bishop according to the rules of Chess.
        
        Returns:
            possible_moves: A list of possible moves grouped by direction.
        """
        possible_moves_per_direction: list[list[PositionTuple]] = []
        possible_directions: list[str] = []
        
        if self.name == const.QUEEN:
            possible_directions += const.ALL_DIRECTIONS
        elif self.name == const.ROOK:
            possible_directions += const.STRAIGHT_DIRECTIONS
        else:
            possible_directions += const.DIAGONAL_DIRECTIONS
        
        for direction in possible_directions:
            temp_list: list[PositionTuple] = []
            position: PositionTuple = self.position
            for _ in range(const.SIZE):
                relative_position: PositionTuple = position.get_relative_position(direction)
                if relative_position.is_out_of_bounds():
                    continue
                temp_list.append(relative_position)
                position = relative_position
            possible_moves_per_direction.append(temp_list)
        
        return possible_moves_per_direction



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

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][King.name]
        self.is_under_Check: bool = False
        self.Check_given_by: PositionTuple
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the King according to the rules of Chess.
        
        Returns:
            possible_moves: A list of single possible moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        for direction in const.ALL_DIRECTIONS:
            relative_position = self.position.get_relative_position(direction)
            if relative_position.is_out_of_bounds():
                continue
            temp_list: list[PositionTuple] = []
            temp_list.append(relative_position)
            possible_moves.append(temp_list)

        return possible_moves
    
    def pieces_to_get_possible_attacking_squares(self) -> list[Piece]:
        """
        Returns pieces which can be used to get all possible attacking squares.
        
        Returns:
            pieces_to_get_possible_attacking_squares: A list of all possible attacking squares grouped by direction.
        """
        pieces_to_get_possible_attacking_squares: list[Piece] = []

        for piece in [
            const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.QUEEN],
            const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.KNIGHT],
            const.symbol_notation_and_material[const.NOTATION][const.WHITE][const.PAWN]
        ]:
            pieces_to_get_possible_attacking_squares.append(create_piece(piece, self.position))
        
        return pieces_to_get_possible_attacking_squares


class Queen(Piece):
    name: str = const.QUEEN
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Queen.name]


class Rook(Piece):
    name: str = const.ROOK
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Rook.name]


class Bishop(Piece):
    name: str = const.BISHOP
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Bishop.name]


class Knight(Piece):
    name: str = const.KNIGHT
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Knight.name]
    

    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Knight according to the rules of Chess.
        
        Returns:
            possible_moves: A list of single possible moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        # straight moves before knight has to turn
        STRAIGHT_MOVES: int = 2
        
        for dir in const.STRAIGHT_DIRECTIONS:
            position = self.position
            for _ in range(STRAIGHT_MOVES): 
                if position.is_out_of_bounds():
                    break
                relative_position = position.get_relative_position(dir)
                position = relative_position
            for inner_dir in const.STRAIGHT_DIRECTIONS:
                if position.is_out_of_bounds():
                    break
                relative_position = position.get_relative_position(inner_dir)
                if relative_position.is_out_of_bounds():
                    continue
                if not relative_position.in_straight_direction(self.position):
                    temp_list: list[PositionTuple] = []
                    temp_list.append(relative_position)
                    possible_moves.append(temp_list)
        
        return possible_moves


class Pawn(Piece):
    name: str = const.PAWN
    material: int = const.symbol_notation_and_material[const.MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = const.symbol_notation_and_material[const.SYMBOL][color][Pawn.name]
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Pawn according to the rules of Chess.
        
        Returns:
            possible_moves: A list of possible moves (at index 0) and capture moves (at index 1).
        """
        possible_moves: list[list[PositionTuple]] = []

        possible_no_of_moves: int = 1 if self.is_moved else 2
        direction: str = const.DOWN if self.color == const.BLACK else const.UP
        position = self.position
        moving_squares: list[PositionTuple] = []
        capturing_squares: list[PositionTuple] = []
        
        for i in range(possible_no_of_moves):
            relative_position = position.get_relative_position(direction)
            if relative_position.is_out_of_bounds():
                continue
            moving_squares.append(relative_position)
            position = relative_position
            if i == 0:
                for dir in [const.LEFT, const.RIGHT]:
                    capturing_square: PositionTuple | None = position.get_relative_position(dir)
                    if capturing_square:
                        capturing_squares.append(capturing_square)
    
        possible_moves.append(moving_squares)
        possible_moves.append(capturing_squares)
        return possible_moves


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