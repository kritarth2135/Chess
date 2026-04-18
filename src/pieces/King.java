package piece;

public class King extends Piece {
    public King(int color, PositionTuple position) {
        super(color, position);

        name = Piece.KING;
        isSlider = false;
        icon = Piece.ICONS[name];
    }
}
