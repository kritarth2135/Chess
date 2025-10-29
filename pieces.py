import helper as h

symbols: list[dict[str: str]] = [
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

pieces: dict[str: dict] = {
    "E": {"material": 0, "name": "Empty"},
    "K": {"material": float("inf"), "name": "King"},
    "Q": {"material": 9, "name": "Queen"},
    "R": {"material": 5, "name": "Rook"},
    "B": {"material": 3, "name": "Bishop"},
    "N": {"material": 3, "name": "Knight"},
    "P": {"material": 1, "name": "Pawn"},
}

class Piece:
    def __init__(self, color: int, position: tuple[int]):
        self.color: int = color
        self.is_moved: bool = False
        self.position: h.PositionTuple = h.PositionTuple(position)

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
    
    def valid_moves(self) -> list[h.PositionTuple]:
        pass

class Queen(Piece):
    name: str = "Q"
    material: int = pieces[name]["material"]
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Queen.name]
    
    def valid_moves(self) -> list[h.PositionTuple]:
        pass

class Rook(Piece):
    name: str = "R"
    material: int = pieces[name]["material"]
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Rook.name]
    
    def valid_moves(self) -> list[h.PositionTuple]:
        pass

class Bishop(Piece):
    name: str = "B"
    material: int = pieces[name]["material"]
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Bishop.name]
    
    def valid_moves(self) -> list[h.PositionTuple]:
        pass

class Knight(Piece):
    name: str = "N"
    material: int = pieces[name]["material"]
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Knight.name]

    def valid_moves(self) -> list[h.PositionTuple]:
        pass

class Pawn(Piece):
    name: str = "P"
    material: int = pieces[name]["material"]
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = symbols[color][Pawn.name]
    
    def valid_moves(self) -> list[h.PositionTuple]:
        pass