package pieces;

public enum Pieces {
    KING(0),
    QUEEN(1),
    ROOK(2),
    BISHOP(3),
    KNIGHT(4),
    PAWN(5);

    private int value;

    private Pieces(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}
