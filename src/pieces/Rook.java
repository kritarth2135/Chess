package src.pieces;

public class Rook extends Piece {
    private static final String ICON_WHITE = "♖";
    private static final String ICON_BLACK = "♜";

    public Rook(Color color) {
        this.color = color;

        name = Pieces.ROOK;
        isSlider = true;
        isMoved = false;
        icon = color == Color.WHITE ? ICON_WHITE : ICON_BLACK;
    }
}
