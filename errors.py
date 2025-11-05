class InvalidFEN(Exception):
    def __init__(self):
        super().__init__("Invalid FEN string.")

class InvalidInput(Exception):
    def __init__(self):
        super().__init__("Invalid input format.")

class InvalidMove(Exception):
    def __init__(self):
        super().__init__("Illegal move.")

class InvalidTurn(Exception):
    def __init__(self):
        super().__init__("Invalid turn.")