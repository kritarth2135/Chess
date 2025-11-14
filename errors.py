class InvalidFEN(Exception):
    def __init__(self):
        super().__init__("Invalid FEN string!")

class InvalidInput(Exception):
    def __init__(self):
        super().__init__(
            "Invalid Input format.\n"
            "Format to enter input: \"<starting_square>,<ending_square>\""
        )

class InvalidMove(Exception):
    def __init__(self):
        super().__init__("Illegal move!")

class KingStillUnderCheck(Exception):
    def __init__(self):
        super().__init__("Your King is still under Check!")

class InvalidTurn(Exception):
    def __init__(self):
        super().__init__("Invalid turn!")