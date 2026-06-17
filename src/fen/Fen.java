package src.fen;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static src.board.Board.BOARD_SIZE;

public class Fen {
    private static final Pattern FEN_PATTERN = Pattern.compile(
        "^([1-8kqrbnp]+\\/){7}[1-8kqrbnp]+\\s[wb]\\s([-]|[kq]+)\\s([-]|[a-h][1-8])\\s(\\d+)\\s(\\d+)$",
        Pattern.CASE_INSENSITIVE
    );

    // Position data in a FEN string
    private static final int BOARD_STATE = 0;
    private static final int ACTIVE_COLOR = 1;
    private static final int CASTLING_AVAILABILITY = 2;
    private static final int EN_PASSANT_MOVE = 3;
    private static final int HALF_MOVE_COUNT = 4;
    private static final int FULL_MOVE_COUNT = 5;

    public char[][] boardState;
    public char activeColor;

    public boolean canWhiteCastleKingSide = false;
    public boolean canWhiteCastleQueenSide = false;
    public boolean canBlackCastleKingSide = false;
    public boolean canBlackCastleQueenSide = false;

    public String enPassantMove;

    public int halfMoveCounter;
    public int fullMoveCounter;

    public Fen(String fenString) throws InvalidFenStringException {
        Matcher matcher = FEN_PATTERN.matcher(fenString);
        if (!matcher.matches()) {
            throw new InvalidFenStringException();
        }

        String[] fenData = fenString.split(" ");

        boardState = new char[BOARD_SIZE][BOARD_SIZE];
        parseBoardState(fenData[BOARD_STATE]);

        activeColor = fenData[ACTIVE_COLOR].charAt(0);

        setCastlingAvailability(fenData[CASTLING_AVAILABILITY]);

        enPassantMove = fenData[EN_PASSANT_MOVE];

        halfMoveCounter = Integer.parseInt(fenData[HALF_MOVE_COUNT]);
        fullMoveCounter = Integer.parseInt(fenData[FULL_MOVE_COUNT]);
    }

    private void parseBoardState(String boardStateString) throws InvalidFenStringException {
        String[] ranks = boardStateString.split("/");

        for (int i = 0; i < BOARD_SIZE; i++) {
            int j = 0;

            for (char ch: ranks[i].toCharArray()) {
                if (j >= BOARD_SIZE) throw new InvalidFenStringException();

                if (Character.isDigit(ch)) {
                    int noOfEmptySquares = ch - '0';

                    for (int k = 0; k < noOfEmptySquares; k++) {
                        if (j >= BOARD_SIZE) throw new InvalidFenStringException();

                        boardState[i][j] = '-';
                        j++;
                    }
                }

                else {
                    boardState[i][j] = ch;
                    j++;
                }
            }
        }
    }

    private void setCastlingAvailability(String castlingData) {
        for (char ch: castlingData.toCharArray()) {
            switch (ch) {
                case 'K' -> { canWhiteCastleKingSide = true; }
                case 'Q' -> { canWhiteCastleQueenSide = true; }
                case 'k' -> { canBlackCastleKingSide = true; }
                case 'q' -> { canBlackCastleQueenSide = true; }
            }
        }
    }
}
