from __future__ import annotations
import re
from typing import Any
import errors

# Length of the square chess grid 
SIZE: int = 8
# Players
EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1

class PositionTuple:
    # These are rank and file index, not actual rank and file
    def __init__(self, position: tuple[int, int]):
        self.rank = position[0]
        self.file = position[1]
        self.position = position
    
    def __add__(self, other: PositionTuple):
        rank = self.rank + other.rank
        file = self.file + other.file
        return PositionTuple((rank, file))
    
    def __eq__(self, other: PositionTuple | Any) -> bool:
        return self.rank == other.rank and self.file == other.file
    
    def on_same_rank_or_file(self, other: PositionTuple | Any) -> bool:
        return self.rank == other.rank or self.file == other.file
    
    def display(self) -> None:
        print(f"({self.rank}, {self.file})")
        
class MovementTuple:
    def __init__(self, movement: tuple[PositionTuple, PositionTuple]):
        self.initial = movement[0]
        self.final = movement[1]
        self.movement = movement

    def display(self) -> None:
        print(f"(({self.initial.rank}, {self.initial.file}), ({self.final.rank}, {self.final.file}))")

# Values to add to current position_tuple to find relative position_tuple
DIRECTIONS: dict[str, PositionTuple] = {
    # Values to calculate ranks are reversed because grid is indexed from top to bottom
    "up": PositionTuple((-1, 0)), "down": PositionTuple((1, 0)),
    "left": PositionTuple((0, -1)), "right": PositionTuple((0, 1)),
    "up_left": PositionTuple((-1, -1)), "up_right": PositionTuple((-1, 1)),
    "down_left": PositionTuple((1, -1)), "down_right": PositionTuple((1, 1))
}
RELATIVE_POSITIONS: dict[str, list[str]] = {
    "all": ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"],
    "straight": ["up", "down", "left", "right"],
    "diagonal": ["up_left", "up_right", "down_left", "down_right"]
}
ALL: str = "all"
STRAIGHT: str = "straight"
DIAGONAL: str = "diagonal"

def get_relative_position(position: PositionTuple, dir: str) -> PositionTuple | None:
    if not position:
        return None
    relative_position = position + DIRECTIONS[dir]
    if is_out_of_bounds(relative_position):
        return None
    return relative_position

def is_out_of_bounds(position: PositionTuple) -> bool:
    for index in [position.rank, position.file]:
        if index not in range(0, SIZE):
            return True
    return False

def alg_notation_to_position_tuple(alg_notation: str) -> PositionTuple:
    position: list[int] = []
    for i in range(len(alg_notation)):
        position.append((ord(alg_notation[i]) - ord("a")) if i == 0 else (SIZE - int(alg_notation[i])))
    return PositionTuple(tuple(reversed(position)))

def input_str_validator(input_str: str) -> bool:
    # Input regex
    regex_pattern = "([a-h][0-8]),([a-h][0-8])"
    # Input format: <start_square>,<end_square>
    
    return bool(re.fullmatch(regex_pattern, input_str))

def input_str_to_movement_tuple(input_str: str) -> MovementTuple:
    input_str = input_str.lower()
    if not input_str_validator(input_str):
        raise errors.InvalidInput
    
    input_list = input_str.split(",")
    movement_list: list[PositionTuple] = []

    for string in input_list:
        movement_list.append(alg_notation_to_position_tuple(string))
    
    return MovementTuple(tuple(movement_list))

def number_to_Es_in_board_state(board_state: list[str]) -> list[str]:
    new_board_state: list[str] = []
    for rank in board_state:
        temp_str: str = ""
        for i in range(len(rank)):
            if rank[i].isdigit():
                temp_str += "E" * int(rank[i])
            else:
                temp_str += rank[i]
        new_board_state.append(temp_str)
    return new_board_state
