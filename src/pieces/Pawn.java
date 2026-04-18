package piece;

public class Pawn extends Piece {
    public Pawn(int color, PositionTuple position) {
        super(color, position);

        name = Piece.PAWN;
        isSlider = false;
        icon = Piece.ICONS[name];
    }
}
