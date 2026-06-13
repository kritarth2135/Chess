package src.pieces;

public enum Color {
    WHITE(0),
    BLACK(1);

    private final int value;

    private Color(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}
