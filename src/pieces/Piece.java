package pieces;

public abstract class Piece {
    Pieces name;
    Color color;

    String icon;
    boolean isMoved;
    boolean isSlider;

    public Color getColor() {
        return color;
    }

    public Pieces getName() {
        return name;
    }

    public String getIcon() {
        return icon;
    }
}
