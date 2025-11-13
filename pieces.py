from typing import Any

import helper
PositionTuple = helper.PositionTuple

# Pieces names
KING: str = "King"
QUEEN: str = "Queen"
ROOK: str = "Rook"
BISHOP: str = "Bishop"
KNIGHT: str = "Knight"
PAWN: str = "Pawn"
EMPTY: str = "Empty"

NOTATION: str = "notation"
SYMBOL: str = "symbol"
MATERIAL: str = "material"

pieces: dict[str, Any] = {
    SYMBOL: [
        {   # White (0)
            KING: "♔",
            QUEEN: "♕",
            ROOK: "♖",
            BISHOP: "♗",
            KNIGHT: "♘",
            PAWN: "♙"
        },
        {   # Black (1)
            KING: "♚",
            QUEEN: "♛",
            ROOK: "♜",
            BISHOP: "♝",
            KNIGHT: "♞",
            PAWN: "♟"
        },
        {   # Empty (-1)
            EMPTY: " "   # Unicode U+2001
        }
    ],
    NOTATION: [
        {   # White (0)
            KING: "K",
            QUEEN: "Q",
            ROOK: "R",
            BISHOP: "B",
            KNIGHT: "N",
            PAWN: "P"
        },
        {   # Black (1)
            KING: "k",
            QUEEN: "q",
            ROOK: "r",
            BISHOP: "b",
            KNIGHT: "n",
            PAWN: "p"
        },
        {   # Empty (-1)
            EMPTY: "E"
        }
    ],
    MATERIAL: {
        KING: float("inf"),
        QUEEN: 9,
        ROOK: 5,
        BISHOP: 3,
        KNIGHT: 3,
        PAWN: 1,
        EMPTY: 0
    }
}

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
            possible_directions += helper.ALL_DIRECTIONS
        elif self.name == ROOK:
            possible_directions += helper.STRAIGHT_DIRECTIONS
        else:
            possible_directions += helper.DIAGONAL_DIRECTIONS
        
        for direction in possible_directions:
            temp_list: list[PositionTuple] = []
            position: PositionTuple | None = self.position
            for _ in range(helper.SIZE):
                relative_postion: PositionTuple | None = helper.get_relative_position(position, direction)
                if relative_postion:
                    temp_list.append(relative_postion)
                    position = relative_postion
            possible_moves_per_direction.append(temp_list)
        
        return possible_moves_per_direction


# Subclasses for each piece type.

class Empty(Piece):
    name: str = EMPTY
    material: int = pieces[MATERIAL][name]
    color: int = helper.EMPTY
    
    def __init__(self, color: int, position: PositionTuple):
        super().__init__(Empty.color, position)
        self.symbol = pieces[SYMBOL][color][Empty.name]

class King(Piece):
    name: str = KING
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][King.name]
        self.is_under_check: bool = False
        self.check_given_by: PositionTuple
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the King according to the rules of Chess.
        
        Returns:
            possible_moves: A list of single possible moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        for direction in helper.ALL_DIRECTIONS:
            relative_postion = helper.get_relative_position(self.position, direction)
            if relative_postion:
                temp_list: list[PositionTuple] = []
                temp_list.append(relative_postion)
                possible_moves.append(temp_list)

        return possible_moves

class Queen(Piece):
    name: str = QUEEN
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Queen.name]

class Rook(Piece):
    name: str = ROOK
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Rook.name]

class Bishop(Piece):
    name: str = BISHOP
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Bishop.name]

class Knight(Piece):
    name: str = KNIGHT
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Knight.name]
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Knight according to the rules of Chess.
        
        Returns:
            possible_moves: A list of single possible moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        # straight moves before knight has to turn
        STRAIGHT_MOVES: int = 2
        
        for dir in helper.STRAIGHT_DIRECTIONS:
            position = self.position
            for _ in range(STRAIGHT_MOVES): 
                if not position:
                    break
                relative_position = helper.get_relative_position(position, dir)
                position = relative_position
            for inner_dir in helper.STRAIGHT_DIRECTIONS:
                if not position:
                    break
                relative_position = helper.get_relative_position(position, inner_dir)
                if relative_position:
                    if not relative_position.on_same_rank_or_file(self.position):
                        temp_list: list[PositionTuple] = []
                        temp_list.append(relative_position)
                        possible_moves.append(temp_list)
        
        return possible_moves

class Pawn(Piece):
    name: str = PAWN
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Pawn.name]
    
    def get_possible_moves(self) -> list[list[PositionTuple]]:
        """
        Find all the possible move of the Pawn according to the rules of Chess.
        
        Returns:
            possible_moves: A list of possible moves and capture moves.
        """
        possible_moves: list[list[PositionTuple]] = []

        possible_no_of_moves: int = 1 if self.is_moved else 2
        direction: str = helper.DOWN if self.color == helper.BLACK else helper.UP
        position = self.position
        moving_squares: list[PositionTuple] = []
        capturing_squares: list[PositionTuple] = []
        
        for i in range(possible_no_of_moves):
            relative_position = helper.get_relative_position(position, direction)
            if relative_position:
                moving_squares.append(relative_position)
                position = relative_position
            if i == 0:
                for dir in [helper.LEFT, helper.RIGHT]:
                    capturing_square: PositionTuple | None = helper.get_relative_position(position, dir)
                    if capturing_square:
                        capturing_squares.append(capturing_square)
    
        possible_moves.append(moving_squares)
        possible_moves.append(capturing_squares)
        return possible_moves


def create_piece(notation: str, position: PositionTuple) -> Piece:
    """Takes the notation and position as argument and creates a Piece according to it."""

    if notation in [pieces[NOTATION][helper.WHITE][KING], pieces[NOTATION][helper.BLACK][KING]]:
        return King(helper.WHITE if notation.isupper() else helper.BLACK, position)
    
    elif notation in [pieces[NOTATION][helper.WHITE][QUEEN], pieces[NOTATION][helper.BLACK][QUEEN]]:
        return Queen(helper.WHITE if notation.isupper() else helper.BLACK, position)
    
    elif notation in [pieces[NOTATION][helper.WHITE][ROOK], pieces[NOTATION][helper.BLACK][ROOK]]:
        return Rook(helper.WHITE if notation.isupper() else helper.BLACK, position)
    
    elif notation in [pieces[NOTATION][helper.WHITE][BISHOP], pieces[NOTATION][helper.BLACK][BISHOP]]:
        return Bishop(helper.WHITE if notation.isupper() else helper.BLACK, position)
    
    elif notation in [pieces[NOTATION][helper.WHITE][KNIGHT], pieces[NOTATION][helper.BLACK][KNIGHT]]:
        return Knight(helper.WHITE if notation.isupper() else helper.BLACK, position)
    
    elif notation in [pieces[NOTATION][helper.WHITE][PAWN], pieces[NOTATION][helper.BLACK][PAWN]]:
        return Pawn(helper.WHITE if notation.isupper() else helper.BLACK, position)
    
    else:
        return Empty(helper.EMPTY, position)