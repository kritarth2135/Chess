class InvalidFEN(Exception):
    def __init__(self, message: str = "Invalid FEN string."):
        self.message = message
        super().__init__(self.message)

class InvalidInput(Exception):
    def __init__(self, message: str = "Invalid input format."):
        self.message = message
        super().__init__(self.message)

class InvalidMove(Exception):
    def __init__(self, message: str = "Invalid move."):
        self.message = message
        super().__init__(self.message)

class InvalidTurn(Exception):
    def __init__(self, message: str = "Invalid turn."):
        self.message = message
        super().__init__(self.message)