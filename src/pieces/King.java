package src.pieces;

public class King extends Piece {
    private static final String ICON_WHITE = "♔";
    private static final String ICON_BLACK = "♚";

    public King(Color color) {
        this.color = color;

        name = Pieces.KING;
        isSlider = false;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
