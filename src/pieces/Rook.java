package piece;

public class Rook extends Piece {
    public Rook(int color, PositionTuple position) {
        super(color, position);

        name = Piece.ROOK;
        isSlider = true;
        icon = Piece.ICONS[name];
    }
}
