from __future__ import annotations
from typing import Any
import re

import errors

"""Constants used."""

# Length of the square chess grid 
SIZE: int = 8

# Players
EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1

"""Helper Classess."""

class PositionTuple:
    """
    Create a PositionTuple.

    Args:
        position: Tuple of the form (rank, file) where rank and file are the indexes of the grid.
    """

    def __init__(self, position: tuple[int, int]) -> None:
        self.rank: int = position[0]
        self.file: int = position[1]
        self.position = position
    
    def __add__(self, other: PositionTuple) -> PositionTuple:
        """Return the addition of two PositionTuples."""

        rank = self.rank + other.rank
        file = self.file + other.file
        return PositionTuple((rank, file))
    
    def __eq__(self, other: PositionTuple | Any) -> bool:
        """Returns true if both PositionTuples refer to the same location."""

        return self.rank == other.rank and self.file == other.file
    
    def on_same_rank_or_file(self, other: PositionTuple | Any) -> bool:
        """Returns true if both PositionTuples refer to the location on same rank OR same file."""

        return self.rank == other.rank or self.file == other.file
    
    def display(self) -> None:
        """Print the PositionTuple in a readable format"""
        
        print(f"({self.rank}, {self.file})")
        
class MovementTuple:
    """
    Create a MovementTuple.

    Args:
        movement: Tuple of the form (initial_position, final_position) where both are of type PositionTuple.
    """

    def __init__(self, movement: tuple[PositionTuple, PositionTuple]) -> None:
        self.initial_position: PositionTuple = movement[0]
        self.final_position: PositionTuple = movement[1]
        self.movement = movement

    def display(self) -> None:
        """Prints the MovementTuple in a readable format."""

        print("[")
        self.initial_position.display()
        self.final_position.display()
        print("]")

"""Helper Functions to get position in a particular direction."""

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
    UP: PositionTuple((-1, 0)), DOWN: PositionTuple((1, 0)),
    LEFT: PositionTuple((0, -1)), RIGHT: PositionTuple((0, 1)),
    UP_LEFT: PositionTuple((-1, -1)), UP_RIGHT: PositionTuple((-1, 1)),
    DOWN_LEFT: PositionTuple((1, -1)), DOWN_RIGHT: PositionTuple((1, 1))
}

# Constants for group of directions
STRAIGHT_DIR: list[str] = [UP, DOWN, LEFT, RIGHT]
DIAGONAL_DIR: list[str] = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
ALL_DIR: list[str] = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

def get_relative_position(position: PositionTuple, dir: str) -> PositionTuple | None:
    """Takes a PositionTuple and returns a PositionTuple according the direction given or returns None in case of failure."""

    if not position:
        return None
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

"""Helper functions to validate and convert user input to PositionTuple."""

def alg_notation_to_position_tuple(alg_notation: str) -> PositionTuple:
    """Takes algorithmic notation in str and returns a PositionTuple according to it."""

    position: list[int] = []
    for i in range(len(alg_notation)):
        position.append((ord(alg_notation[i]) - ord("a")) if i == 0 else (SIZE - int(alg_notation[i])))
    return PositionTuple(tuple(reversed(position)))

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
    
    return MovementTuple(tuple(movement_list))

def number_of_spaces_to_Es_in_piece_position(piece_position: list[str]) -> list[str]:
    """Converts the part of FEN string which indicates the position of all pieces and replaces the number of spaces with 'E's"""
    
    new_piece_position: list[str] = []
    for rank in piece_position:
        temp_str: str = ""
        for i in range(len(rank)):
            if rank[i].isdigit():
                temp_str += "E" * int(rank[i])
            else:
                temp_str += rank[i]
        new_piece_position.append(temp_str)
    return new_piece_position
