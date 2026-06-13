package src.pieces;

public class Knight extends Piece {
    private static final String ICON_WHITE = "♘";
    private static final String ICON_BLACK = "♞";

    public Knight(Color color) {
        this.color = color;

        name = Pieces.KNIGHT;
        isSlider = false;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
