package src.board;

import src.fen.Fen;
import src.fen.InvalidFenStringException;
import src.pieces.Color;
import src.positions.PositionTuple;

public class Board {
    public static final int BOARD_SIZE = 8;

    private Grid grid;
    private Color activeColor;

    private boolean canWhiteCastleKingSide = false;
    private boolean canWhiteCastleQueenSide = false;
    private boolean canBlackCastleKingSide = false;
    private boolean canBlackCastleQueenSide = false;

    private PositionTuple enPassantMove;

    private int halfMoveCounter;
    private int fullMoveCounter;

    public Board(String fen_string) {
        Fen fen;
        try {
            fen = new Fen(fen_string);
        } catch (InvalidFenStringException err) {
            System.out.println("Error: " + err);
            return;
        }

        grid = new Grid(fen.boardState);

        activeColor = fen.activeColor == 'w' ? Color.WHITE : Color.BLACK;

        canWhiteCastleKingSide = fen.canWhiteCastleKingSide;
        canWhiteCastleQueenSide = fen.canWhiteCastleQueenSide;
        canBlackCastleKingSide = fen.canBlackCastleKingSide;
        canBlackCastleQueenSide = fen.canBlackCastleQueenSide;

        if (fen.enPassantMove.compareTo("-") == 0) {
            enPassantMove = null;
        }
        else {
            enPassantMove = new PositionTuple(fen.enPassantMove);
        }

        halfMoveCounter = fen.halfMoveCounter;
        fullMoveCounter = fen.fullMoveCounter;
    }
}
