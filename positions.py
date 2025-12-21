from __future__ import annotations

from constants import *


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
        self.position: tuple[int, int] = position
    
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

    def is_out_of_bounds(self) -> bool:
        """Takes a PositionTuple and returns true if it is out of bounds of the grid."""

        for index in [self.rank, self.file]:
            if index not in range(0, SIZE):
                return True
        return False
    
    def get_relative_position(self, dir: str) -> PositionTuple | None:
        """Takes a PositionTuple and returns a PositionTuple according the direction given or returns None in case of failure."""

        relative_position: PositionTuple = PositionTuple(self.position) + values_to_calculate_relative_direction[dir]
        if self.is_out_of_bounds():
            return None
        return relative_position



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
