class CustomException(Exception):
    ...


class InvalidFEN(CustomException):
    def __init__(self):
        super().__init__("Invalid FEN string!")

class InvalidInput(CustomException):
    def __init__(self):
        super().__init__(
            "Invalid Input format.\n"
            "Format to enter input: \"<starting_square>,<ending_square>\""
        )

class InvalidMove(CustomException):
    def __init__(self):
        super().__init__("Illegal move!")

class KingStillUnderCheck(CustomException):
    def __init__(self):
        super().__init__("Your King is still under Check!")

class InvalidTurn(CustomException):
    def __init__(self):
        super().__init__("Invalid turn!")