from __future__ import annotations
from typing import Any
import re
import os

import errors


# Constants used.

# Length of the square chess grid 
SIZE: int = 8

# Players
EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1


# Helper Classess.

class PositionTuple:
    """
    Create a PositionTuple.

    Args:
        position: Tuple of the form (rank, file) where rank and file are the indexes of the grid.

    Attributes:
        rank: Index of the rank from top of the grid.
        file: Index of the file from left of the grid.
    """

    def __init__(self, position: tuple[int, int]) -> None:
        self.rank: int = position[0]
        self.file: int = position[1]
    
    def __add__(self, other: PositionTuple) -> PositionTuple:
        """Return the addition of two PositionTuples."""

        rank = self.rank + other.rank
        file = self.file + other.file
        return PositionTuple((rank, file))
    
    def __eq__(self, other: PositionTuple | Any) -> bool:
        """Returns true if both PositionTuples refer to the same location."""

        return self.rank == other.rank and self.file == other.file
    
    def __str__(self) -> str:
        """Returns the PositionTuple in a readable format"""
        
        return f"({self.rank}, {self.file})"
    
    def on_same_rank_or_file(self, other: PositionTuple | Any) -> bool:
        """Returns true if both PositionTuples refer to the location on same rank OR same file."""

        return self.rank == other.rank or self.file == other.file


class MovementTuple:
    """
    Create a MovementTuple.

    Args:
        movement: Tuple of the form (initial_position, final_position) where both are of type PositionTuple.
    
    Attributes:
        initial_position: PositionTuple indicating the initial position of the move.
        final_position: PositionTuple indicating the final position of the move.
    """

    def __init__(self, movement: tuple[PositionTuple, PositionTuple]) -> None:
        self.initial_position: PositionTuple = movement[0]
        self.final_position: PositionTuple = movement[1]

    def __str__(self) -> str:
        """Prints the MovementTuple in a readable format."""

        return f"[{self.initial_position}, {self.final_position}]"


# Helper Functions to get position in a particular direction.

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


def get_relative_position(position: PositionTuple, dir: str) -> PositionTuple | None:
    """Takes a PositionTuple and returns a PositionTuple according the direction given or returns None in case of failure."""

    relative_position = position + values_to_calculate_relative_direction[dir]
    if is_out_of_bounds(relative_position):
        return None
    return relative_position


def is_out_of_bounds(position: PositionTuple) -> bool:
    """Takes a PositionTuple and returns true if it is out of bounds of the grid."""

    for index in [position.rank, position.file]:
        if index not in range(0, SIZE):
            return True
    return False


# Helper functions to validate and convert user input to PositionTuple.

def alg_notation_to_position_tuple(alg_notation: str) -> PositionTuple:
    """Takes algorithmic notation in str and returns a PositionTuple according to it."""

    position: list[int] = []
    for i in range(len(alg_notation)):
        position.append((ord(alg_notation[i]) - ord("a")) if i == 0 else (SIZE - int(alg_notation[i])))
    return PositionTuple(tuple(reversed(position))) # type: ignore


def input_str_validator(input_str: str) -> bool:
    """Takes the input string and returns true if it is of the form '<starting_square>,<ending_square>'."""
    
    input_regex = "([a-h][0-8]),([a-h][0-8])"
    return bool(re.fullmatch(input_regex, input_str))


def input_str_to_movement_tuple(input_str: str) -> MovementTuple:
    """Takes the input string and returns a MovementTuple according to it."""

    input_str = input_str.lower()
    if not input_str_validator(input_str):
        raise errors.InvalidInput
    
    input_list = input_str.split(",")
    movement_list: list[PositionTuple] = []

    for string in input_list:
        movement_list.append(alg_notation_to_position_tuple(string))
    
    return MovementTuple(tuple(movement_list)) # type: ignore


def clear_screen() -> None:
    """Clears the screen of the terminal."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# All functions related to FEN parsing.

def fen_parser(fen_string: str) -> dict[str, Any] | None:
    """Takes a FEN string and scrapes all information from it and returns a dictionary of all data."""
    modified_FEN: str = FEN_to_modified_FEN(fen_string)
    if not modified_FEN_string_validator(modified_FEN):
        return None
    
    FEN_data: dict[str, Any] = {}
    (
        piece_placement_data,
        active_color,
        castling_availability,
        en_passant_squares,
        halfmove_count,
        fullmove_count
    ) = modified_FEN.split(" ")
    
    FEN_data["piece_placement_data"] = piece_placement_data.split("/")
    FEN_data["active_color"] = WHITE if active_color == "w" else BLACK
    FEN_data["castling_availability"] = list(castling_availability)
    FEN_data["en_passant_squares"] = en_passant_squares
    FEN_data["halfmove_count"] = int(halfmove_count)
    FEN_data["fullmove_count"] = int(fullmove_count)

    return FEN_data


def modified_FEN_string_validator(modified_FEN: str) -> bool:
    '''Takes modified FEN as input and returns True if it is valid.'''

    modified_FEN_regex: str = r"([kqrbnpKQRBNPE]{8}\/){7}[kqrbnpKQRBNPE]{8}\s[wb]\s[01]{4}\s(.*)"
    return bool(re.fullmatch(modified_FEN_regex, modified_FEN))


def FEN_to_modified_FEN(fen_string: str) -> str:
    """Converts the FEN string into a more usable format by making it fixed length."""
    piece_placement_data, active_color, castling_availability, en_passant_squares, halfmove_count, fullmove_count = fen_string.strip().split(" ")

    modified_piece_placement_data: str = "/".join(modified_piece_placement(piece_placement_data.split("/")))
    updated_castling_availability: str = modified_castling_availability(list(castling_availability))

    return " ".join([modified_piece_placement_data, active_color, updated_castling_availability, en_passant_squares, halfmove_count, fullmove_count])


def modified_piece_placement(piece_placement: list[str]) -> list[str]:
    """Converts the part of FEN string which indicates the position of all pieces and replaces the number of spaces with 'E's"""
    
    new_piece_placement: list[str] = []
    for rank in piece_placement:
        temp_str: str = ""
        for i in range(len(rank)):
            if rank[i].isdigit():
                temp_str += "E" * int(rank[i])
            else:
                temp_str += rank[i]
        new_piece_placement.append(temp_str)
    
    return new_piece_placement


def modified_castling_availability(castling_availability: list[str]):
    """Converts castling availability into a series of 0s and 1s in the sequence shown in valid_castling_sides"""

    from pieces import pieces, NOTATION, KING, QUEEN

    valid_castling_sides: list[str] = [
        pieces[NOTATION][WHITE][KING],
        pieces[NOTATION][WHITE][QUEEN],
        pieces[NOTATION][BLACK][KING],
        pieces[NOTATION][BLACK][QUEEN],
    ]

    modified_castling_availability: str = ""
    for side in valid_castling_sides:
        if side in castling_availability:
            modified_castling_availability += "1"
        else:
            modified_castling_availability += "0"
    
    return modified_castling_availability
