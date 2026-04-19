package pieces;

public class Knight extends Piece {
    private static String ICON_WHITE = "♘";
    private static String ICON_BLACK = "♞";

    public Knight(Color color) {
        this.color = color;

        name = Pieces.KNIGHT;
        isSlider = false;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
