def fen_parser(fen_string: str) -> dict[str, Any] | None:
    """Takes a FEN string and scrapes all information from it and returns a dictionary of all data."""
    modified_FEN: str = FEN_to_modified_FEN(fen_string)
    if not modified_FEN_string_validator(modified_FEN):
        return None
    
    FEN_data: dict[str, Any] = {}
    (
        piece_placement_data,
        active_color,
        castling_availability,
        en_passant_squares,
        halfmove_count,
        fullmove_count
    ) = modified_FEN.split(" ")
    
    FEN_data["piece_placement_data"] = piece_placement_data.split("/")
    FEN_data["active_color"] = WHITE if active_color == "w" else BLACK
    FEN_data["castling_availability"] = list(castling_availability)
    FEN_data["en_passant_squares"] = en_passant_squares
    FEN_data["halfmove_count"] = int(halfmove_count)
    FEN_data["fullmove_count"] = int(fullmove_count)

    return FEN_data


def modified_FEN_string_validator(modified_FEN: str) -> bool:
    '''Takes modified FEN as input and returns True if it is valid.'''

    modified_FEN_regex: str = r"([kqrbnpKQRBNPE]{8}\/){7}[kqrbnpKQRBNPE]{8}\s[wb]\s[01]{4}\s(.*)"
    return bool(re.fullmatch(modified_FEN_regex, modified_FEN))


def FEN_to_modified_FEN(fen_string: str) -> str:
    """Converts the FEN string into a more usable format by making it fixed length."""
    piece_placement_data, active_color, castling_availability, en_passant_squares, halfmove_count, fullmove_count = fen_string.strip().split(" ")

    modified_piece_placement_data: str = "/".join(modified_piece_placement(piece_placement_data.split("/")))
    updated_castling_availability: str = modified_castling_availability(list(castling_availability))

    return " ".join([modified_piece_placement_data, active_color, updated_castling_availability, en_passant_squares, halfmove_count, fullmove_count])


def modified_piece_placement(piece_placement: list[str]) -> list[str]:
    """Converts the part of FEN string which indicates the position of all pieces and replaces the number of spaces with 'E's"""
    
    new_piece_placement: list[str] = []
    for rank in piece_placement:
        temp_str: str = ""
        for i in range(len(rank)):
            if rank[i].isdigit():
                temp_str += "E" * int(rank[i])
            else:
                temp_str += rank[i]
        new_piece_placement.append(temp_str)
    
    return new_piece_placement


def modified_castling_availability(castling_availability: list[str]):
    """Converts castling availability into a series of 0s and 1s in the sequence shown in valid_castling_sides"""

    from pieces import pieces, NOTATION, KING, QUEEN

    valid_castling_sides: list[str] = [
        pieces[NOTATION][WHITE][KING],
        pieces[NOTATION][WHITE][QUEEN],
        pieces[NOTATION][BLACK][KING],
        pieces[NOTATION][BLACK][QUEEN],
    ]

    modified_castling_availability: str = ""
    for side in valid_castling_sides:
        if side in castling_availability:
            modified_castling_availability += "1"
        else:
            modified_castling_availability += "0"
    
    return modified_castling_availability
