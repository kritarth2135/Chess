package pieces;

public class Bishop extends Piece {
    private static String ICON_WHITE = "♗";
    private static String ICON_BLACK = "♝";

    public Bishop(Color color) {
        this.color = color;

        name = Pieces.BISHOP;
        isSlider = true;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
