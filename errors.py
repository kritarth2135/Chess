class InvalidInput(Exception):
    def __init__(self, message = "Invalid input format."):
        self.message = message
        super().__init__(self.message)

class InvalidMove(Exception):
    def __init__(self, message = "Invalid move."):
        self.message = message
        super().__init__(self.message)

class InvalidFEN(Exception):
    def __init__(self, message = "Invalid FEN string."):
        self.message = message
        super().__init__(self.message)