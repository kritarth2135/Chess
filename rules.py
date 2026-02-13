import constants as const
from positions import PositionTuple


class Rules:
    pass


class MovementRules(Rules):
    sliders: list[str] = [const.QUEEN, const.ROOK, const.BISHOP]
    non_sliders: list[str] = [const.KING, const.KNIGHT, const.PAWN]

    moving_directions: dict[str, str] = {
        const.QUEEN: const.ALL_DIRECTIONS,
        const.ROOK: const.STRAIGHT_DIRECTIONS,
        cosnt.BISHOP: const.DIAGONAL_DIRECTIONS
    }

    moving_offsets: dict[str, list[PositionTuple]] = {
        const.KING: [
            PositionTuple((1, 0)),
            PositionTuple((-1, 0)),
            PositionTuple((0, 1)),
            PositionTuple((0, -1)),
            PositionTuple((1, 1)),
            PositionTuple((1, -1)),
            PositionTuple((-1, 1)),
            PositionTuple((-1, -1)),
        ],
        const.KNIGHT: [
            PositionTuple((2, 1)),
            PositionTuple((2, -1)),
            PositionTuple((-2, 1)),
            PositionTuple((-2, -1)),
            PositionTuple((1, 2)),
            PositionTuple((1, -2)),
            PositionTuple((-1, 2)),
            PositionTuple((-1, -2))
        ],
        const.PAWN: [
            PositionTuple((1, 0)),
            PositionTuple((2, 0))
        ]
    }


class AttackRules(Rules):
    sliders: list[str] = [const.QUEEN, const.ROOK, const.BISHOP]
    non_sliders: list[str] = [const.KING, const.KNIGHT, const.PAWN]

    attacking_directions: dict[str, str] = {
        const.QUEEN: const.ALL_DIRECTIONS,
        const.ROOK: const.STRAIGHT_DIRECTIONS,
        cosnt.BISHOP: const.DIAGONAL_DIRECTIONS
    }

    attacking_offsets: dict[str, list[PositionTuple]] = {
        const.KING: [
            PositionTuple((1, 0)),
            PositionTuple((-1, 0)),
            PositionTuple((0, 1)),
            PositionTuple((0, -1)),
            PositionTuple((1, 1)),
            PositionTuple((1, -1)),
            PositionTuple((-1, 1)),
            PositionTuple((-1, -1)),
        ],
        const.KNIGHT: [
            PositionTuple((2, 1)),
            PositionTuple((2, -1)),
            PositionTuple((-2, 1)),
            PositionTuple((-2, -1)),
            PositionTuple((1, 2)),
            PositionTuple((1, -2)),
            PositionTuple((-1, 2)),
            PositionTuple((-1, -2))
        ],
        const.PAWN: [
            PositionTuple((1, 1)),
            PositionTuple((1, -1))
        ]
    }
