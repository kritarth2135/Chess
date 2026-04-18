package piece;

public class Queen extends Piece {
    public Queen(int color, PositionTuple position) {
        super(color, position);

        name = Piece.QUEEN;
        isSlider = true;
        icon = Piece.ICONS[name];
    }
}
