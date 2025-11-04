from typing import Any

import helper

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

    def __init__(self, color: int, position: helper.PositionTuple) -> None:
        self.symbol: str
        self.name: str
        self.is_moved: bool = False
        self.color: int = color
        self.position: helper.PositionTuple = position
    
    def get_valid_moves(self) -> list[list[helper.PositionTuple]] | list[helper.PositionTuple]:
        """
        Find all the valid move of the piece according to the rules of Chess.
        
        Returns:
            valid_moves: A list of valid moves grouped by direction in case of Queen, Rook, Bishop and
                         a combined list of all valid moves in case of all other pieces
        """

        if self.name in [QUEEN, ROOK, BISHOP]:
            valid_moves_per_direction: list[list[helper.PositionTuple]] = []
            temp_list: list[helper.PositionTuple] = []
            valid_directions: list[str] = []
            
            if self.name == QUEEN:
                valid_directions += helper.ALL_DIRECTIONS
            elif self.name == ROOK:
                valid_directions += helper.STRAIGHT_DIRECTIONS
            else:
                valid_directions += helper.DIAGONAL_DIRECTIONS
            
            for direction in valid_directions:
                position: helper.PositionTuple | None = self.position
                for _ in range(helper.SIZE):
                    relative_postion: helper.PositionTuple | None = helper.get_relative_position(position, direction)
                    if relative_postion:
                        temp_list.append(relative_postion)
                        position = relative_postion
                valid_moves_per_direction.append(temp_list)
                        
            return valid_moves_per_direction
        
        else:
            valid_moves: list[helper.PositionTuple] = []

            if self.name == KING:
                for direction in helper.ALL_DIRECTIONS:
                    relative_postion = helper.get_relative_position(self.position, direction)
                    if relative_postion:
                        valid_moves.append(relative_postion)

                return valid_moves
            
            elif self.name == KNIGHT:
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
                                valid_moves.append(relative_position)
                
                return valid_moves
            
            elif self.name == PAWN:
                valid_no_of_moves: int = 1 if self.is_moved else 2
                direction: str = helper.DOWN if self.color == helper.BLACK else helper.UP
                position = self.position
                
                for _ in range(valid_no_of_moves):
                    relative_position = helper.get_relative_position(position, direction)
                    if relative_position:
                        valid_moves.append(relative_position)
                        position = relative_position
            
                return valid_moves
            
            return valid_moves

"""Subclasses for each piece type."""

class Empty(Piece):
    name: str = EMPTY
    material: int = pieces[MATERIAL][name]
    color: int = helper.EMPTY
    
    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(Empty.color, position)
        self.symbol = pieces[SYMBOL][color][Empty.name]

class King(Piece):
    name: str = KING
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][King.name]

class Queen(Piece):
    name: str = QUEEN
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Queen.name]

class Rook(Piece):
    name: str = ROOK
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Rook.name]

class Bishop(Piece):
    name: str = BISHOP
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Bishop.name]

class Knight(Piece):
    name: str = KNIGHT
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Knight.name]

class Pawn(Piece):
    name: str = PAWN
    material: int = pieces[MATERIAL][name]

    def __init__(self, color: int, position: helper.PositionTuple):
        super().__init__(color, position)
        self.symbol = pieces[SYMBOL][color][Pawn.name]
