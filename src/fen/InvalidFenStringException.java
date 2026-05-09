package fen;

public class InvalidFenStringException extends Exception {
    public InvalidFenStringException() {
        super("Invalid Fen String");
    }
}
