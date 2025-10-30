import helper
from typing import Any

SIZE: int = helper.SIZE

symbols: list[dict[str, str]] = [
    {   # White (0)
        "K": "♔", "Q": "♕",
        "R": "♖", "B": "♗",
        "N": "♘", "P": "♙"
    },
    {   # Black (1)
        "K": "♚", "Q": "♛",
        "R": "♜", "B": "♝",
        "N": "♞", "P": "♟"
    },
    {   # Empty (-1)
        "E": " "   # Unicode U+2001
    }
]

pieces: dict[str, dict[str, Any]] = {
    "E": {"material": 0, "name": "Empty"},
    "K": {"material": float("inf"), "name": "King"},
    "Q": {"material": 9, "name": "Queen"},
    "R": {"material": 5, "name": "Rook"},
    "B": {"material": 3, "name": "Bishop"},
    "N": {"material": 3, "name": "Knight"},
    "P": {"material": 1, "name": "Pawn"},
}

class Piece:
    def __init__(self, color: int, position: tuple[int, int]):
        self.symbol: str
        self.name: str
        self.color: int = color
        self.is_moved: bool = False
        self.position: helper.PositionTuple = helper.PositionTuple(position)
    
    def valid_moves(self) -> list[helper.PositionTuple]:
        valid_moves: list[helper.PositionTuple] = []
        
        if self.name in ["Q", "R", "B"]:
            valid_dir: str = ""
            if self.name == "Q":
                valid_dir += helper.ALL
            elif self.name == "R":
                valid_dir += helper.STRAIGHT
            else:
                valid_dir += helper.DIAGONAL
            
            for dir in helper.RELATIVE_POSITIONS[valid_dir]:
                position: helper.PositionTuple = self.position
                for _ in range(SIZE):
                    relative_postion: helper.PositionTuple = helper.get_relative_position(position, dir)
                    if relative_postion:
                        valid_moves.append(relative_postion)
                        position = relative_postion
                        
            return valid_moves
        
        elif self.name == "K":
            for dir in helper.RELATIVE_POSITIONS[helper.ALL]:
                relative_postion: helper.PositionTuple = helper.get_relative_position(self.position, dir)
                if relative_postion:
                    valid_moves.append(relative_postion)

            return valid_moves
        
        elif self.name == "N":
            # straight moves before knight has to turn
            STRAIGHT_MOVES: int = 2
            for dir in helper.RELATIVE_POSITIONS[helper.STRAIGHT]:
                position: helper.PositionTuple = self.position
                for _ in range(STRAIGHT_MOVES):
                    relative_position: helper.PositionTuple = helper.get_relative_position(position, dir)
                    position = relative_position
                for inner_dir in helper.RELATIVE_POSITIONS[helper.STRAIGHT]:
                    relative_position = helper.get_relative_position(position, inner_dir)
                    if relative_position:
                        if not relative_position.on_same_rank_or_file(self.position):
                            valid_moves.append(relative_position)
            
            return valid_moves
        
        elif self.name == "P":
            VALID_NO_OF_MOVES: int = 1 if self.is_moved else 2
            DIR: str = "down" if self.color else "up"
            position: helper.PositionTuple = self.position
            for _ in range(VALID_NO_OF_MOVES):
                relative_position: helper.PositionTuple = helper.get_relative_position(position, DIR)
                if relative_position:
                    valid_moves.append(relative_position)
                    position = relative_position
        
        return valid_moves

class Empty(Piece):
    name: str = "E"
    material: int = pieces[name]["material"]
    
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Empty.name]

class King(Piece):
    name: str = "K"
    material: int = pieces[name]["material"]

    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][King.name]

class Queen(Piece):
    name: str = "Q"
    material: int = pieces[name]["material"]

    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Queen.name]

class Rook(Piece):
    name: str = "R"
    material: int = pieces[name]["material"]

    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Rook.name]

class Bishop(Piece):
    name: str = "B"
    material: int = pieces[name]["material"]

    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Bishop.name]

class Knight(Piece):
    name: str = "N"
    material: int = pieces[name]["material"]

    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Knight.name]

class Pawn(Piece):
    name: str = "P"
    material: int = pieces[name]["material"]

    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Pawn.name]
