package piece;

public class Knight extends Piece {
    public Knight(int color, PositionTuple position) {
        super(color, position);

        name = Piece.KNIGHT;
        isSlider = false;
        icon = Piece.ICONS[name];
    }
}
