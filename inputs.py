import re

import constants as const
from positions import PositionTuple, MovementTuple
import errors



def input_str_to_movement_tuple(input_str: str) -> MovementTuple:
    """Takes the input string and returns a MovementTuple according to it."""

    input_str = input_str.lower()
    if not input_str_validator(input_str):
        raise errors.InvalidInput
    
    input_list = input_str.split(" ")
    movement_list: list[PositionTuple] = []

    for string in input_list:
        movement_list.append(alg_notation_to_position_tuple(string))
    
    return MovementTuple(tuple(movement_list)) # type: ignore


def alg_notation_to_position_tuple(alg_notation: str) -> PositionTuple:
    """Takes algorithmic notation in str and returns a PositionTuple according to it."""

    position: list[int] = []
    for i in range(len(alg_notation)):
        position.append((ord(alg_notation[i]) - ord("a")) if i == 0 else (const.GRID_SIZE - int(alg_notation[i])))
    return PositionTuple(tuple(reversed(position))) # type: ignore


def input_str_validator(input_str: str) -> bool:
    """Takes the input string and returns true if it is of the form '<starting_square><any_separator><ending_square>'."""
    
    input_regex = r"([a-h][1-8])[ ]([a-h][1-8])"
    return bool(re.fullmatch(input_regex, input_str))

