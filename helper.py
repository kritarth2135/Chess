from __future__ import annotations
from typing import Any
import re
import os

from constants import *
import errors



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
        
        return f"({chr(ord("A") + self.file)}{SIZE - self.rank})"
    
    def in_straight_direction(self, other: PositionTuple | Any) -> bool:
        """Returns true if both PositionTuple refer to the location in a straight line on grid"""

        return self.rank == other.rank or self.file == other.file
    
    def in_diagonal_direction(self, other: PositionTuple | Any) -> bool:
        """Returns true if both PositionTuple refer to the location in a straight line on grid"""

        return ((self.rank - other.rank) ** 2) == ((self.file - other.file) ** 2)


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


# Helper functions to validate and convert user input to MovementTuple.

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

