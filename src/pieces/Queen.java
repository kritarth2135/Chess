package src.pieces;

public class Queen extends Piece {
    private static final String ICON_WHITE = "♕";
    private static final String ICON_BLACK = "♛";

    public Queen(Color color) {
        this.color = color;

        name = Pieces.QUEEN;
        isSlider = true;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
