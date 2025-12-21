from typing import Any

from positions import PositionTuple



# Length of the square chess grid 
SIZE: int = 8

# Players
EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1

# Constants for direction names
UP: str = "up"
DOWN: str = "down"
LEFT: str = "left"
RIGHT: str = "right"
UP_LEFT: str = "up_left"
UP_RIGHT: str = "up_right"
DOWN_LEFT: str = "down_left"
DOWN_RIGHT: str = "down_right"

# Constants for calculating directions
values_to_calculate_relative_direction: dict[str, PositionTuple] = {
    UP: PositionTuple((-1, 0)),
    DOWN: PositionTuple((1, 0)),
    LEFT: PositionTuple((0, -1)),
    RIGHT: PositionTuple((0, 1)),
    UP_LEFT: PositionTuple((-1, -1)),
    UP_RIGHT: PositionTuple((-1, 1)),
    DOWN_LEFT: PositionTuple((1, -1)),
    DOWN_RIGHT: PositionTuple((1, 1))
}

# Constants for group of directions
STRAIGHT_DIRECTIONS: list[str] = [UP, DOWN, LEFT, RIGHT]
DIAGONAL_DIRECTIONS: list[str] = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
ALL_DIRECTIONS: list[str] = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

# Pieces names
KING: str = "King"
QUEEN: str = "Queen"
ROOK: str = "Rook"
BISHOP: str = "Bishop"
KNIGHT: str = "Knight"
PAWN: str = "Pawn"
EMPTY_STR: str = "Empty"

NOTATION: str = "notation"
SYMBOL: str = "symbol"
MATERIAL: str = "material"

symbol_notation_and_material: dict[str, Any] = {
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
            EMPTY_STR: " "   # Unicode U+2001
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
            EMPTY_STR: "E"
        }
    ],
    MATERIAL: {
        KING: float("inf"),
        QUEEN: 9,
        ROOK: 5,
        BISHOP: 3,
        KNIGHT: 3,
        PAWN: 1,
        EMPTY_STR: 0
    }
}

DEFAULT_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"