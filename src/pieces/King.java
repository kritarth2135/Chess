package pieces;

public class King extends Piece {
    private static String ICON_WHITE = "♔";
    private static String ICON_BLACK = "♚";

    public King(Color color) {
        this.color = color;

        name = Pieces.KING;
        isSlider = false;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
