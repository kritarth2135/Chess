package src.positions;

import java.util.Map;
import java.util.HashMap;

import static src.board.Board.BOARD_SIZE;

public class PositionTuple {
    private static final Map<String, PositionTuple> RELATIVE_DIRS = new HashMap<>();
    static {
        RELATIVE_DIRS.put("up", new PositionTuple(-1, 0));
        RELATIVE_DIRS.put("down", new PositionTuple(1, 0));
        RELATIVE_DIRS.put("left", new PositionTuple(0, -1));
        RELATIVE_DIRS.put("right", new PositionTuple(0, 1));
        RELATIVE_DIRS.put("upleft", new PositionTuple(-1, -1));
        RELATIVE_DIRS.put("upright", new PositionTuple(-1, 1));
        RELATIVE_DIRS.put("downleft", new PositionTuple(1, -1));
        RELATIVE_DIRS.put("downright", new PositionTuple(1, 1));
    }

    private final int rank;
    private final int file;

    public PositionTuple(int rank, int file) {
        this.rank = rank;
        this.file = file;
    }

    public PositionTuple(String square) {
        rank = 7 - ((square.charAt(1) - '0') - 1);
        file = Character.toUpperCase(square.charAt(0)) - 'A';
    }

    public int rank() {
        return this.rank;
    }

    public int file() {
        return this.file;
    }

    public PositionTuple add(PositionTuple other) {
        return new PositionTuple(this.rank + other.rank, this.file + other.file);
    }

    public boolean equals(PositionTuple other) {
        return this.rank == other.rank && this.file == other.file;
    }

    public boolean isOutOfBounds() {
        return this.rank < 0 || this.rank >= BOARD_SIZE || this.file < 0 || this.file >= BOARD_SIZE;
    }

    public PositionTuple getRelativeDirection(String direction) {
        return this.add(RELATIVE_DIRS.get(direction));
    }

    @Override
    public String toString() {
        return "[" + (char) (((int) 'A') + file) + (8 - rank) + "]";
    }
}
