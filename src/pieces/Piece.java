package piece;

public class Piece {
    public static final int KING = 0;
    public static final int QUEEN = 1;
    public static final int ROOK = 2;
    public static final int BISHOP = 3;
    public static final int KNIGHT = 4;
    public static final int PAWN = 5;

    public static final String[] ICONS = {
        {"♔", "♕", "♖", "♗", "♘", "♙"},
        {"♚", "♛", "♜", "♝", "♞", "♟"}
    };

    public int name;
    public int color;
    public PositionTuple position;

    public String icon;
    public boolean isMoved;
    public boolean isSlider;

    public Piece(int color, PositionTuple position) {
        this.color = color;
        this.position = position;

        isMoved = false;
    }
}
