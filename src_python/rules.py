import constants as const
from positions import PositionTuple


class Rules:
    SLIDERS: list[str] = [const.QUEEN, const.ROOK, const.BISHOP]
    NON_SLIDERS: list[str] = [const.KING, const.KNIGHT, const.PAWN]

    MOVING_DIRECTIONS: dict[str, str] = {
        const.QUEEN: const.ALL_DIRECTIONS,
        const.ROOK: const.STRAIGHT_DIRECTIONS,
        cosnt.BISHOP: const.DIAGONAL_DIRECTIONS
    }

    MOVING_OFFSETS: dict[str, list[PositionTuple]] = {
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

    ATTACKING_OFFSETS: dict[str, list[PositionTuple]] = {
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


