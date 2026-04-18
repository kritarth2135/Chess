package piece;

public class Bishop extends Piece {
    public Bishop(int color, PositionTuple position) {
        super(color, position);

        name = Piece.BISHOP;
        isSlider = true;
        icon = Piece.ICONS[name];
    }
}
