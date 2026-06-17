package src.positions;

public class MovementTuple {
    private final PositionTuple initialPosition;
    private final PositionTuple finalPosition;

    public MovementTuple(PositionTuple initialPosition, PositionTuple finalPosition) {
        this.initialPosition = initialPosition;
        this.finalPosition = finalPosition;
    }

    public PositionTuple initialPosition() {
        return this.initialPosition;
    }

    public PositionTuple finalPosition() {
        return this.finalPosition;
    }

    @Override
    public String toString() {
        return initialPosition + "-" + finalPosition;
    }
}
