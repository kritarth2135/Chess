package fen;

import java.util.Arrays;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Fen {
    private static Pattern fenPattern = Pattern.compile(
        "^([1-8kqrbnp]+\\/){7}[1-8kqrbnp]+\\s[wb]\\s([-]|[kq]+)\\s([-]|[a-h][1-8])\\s(\\d+)\\s(\\d+)$",
        Pattern.CASE_INSENSITIVE
    );

    // Position data in a FEN string
    private static int BOARD_STATE = 0;
    private static int ACTIVE_COLOR = 1;
    private static int CASTLING_AVAILABILITY = 2;
    private static int EN_PASSANT_MOVE = 3;
    private static int HALF_MOVE_COUNT = 4;
    private static int FULL_MOVE_COUNT = 5;

    private static int BOARD_SIZE = 8;

    private char[][] boardState;
    private char activeColor;

    private boolean canWhiteCastleKingSide = false;
    private boolean canWhiteCastleQueenSide = false;
    private boolean canBlackCastleKingSide = false;
    private boolean canBlackCastleQueenSide = false;

    private String enPassantMove;

    private int halfMoveCounter;
    private int fullMoveCounter;

    public Fen(String fenString) throws InvalidFenStringException {
        Matcher matcher = fenPattern.matcher(fenString);
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
                case 'K':
                    canWhiteCastleKingSide = true;
                    break;
                case 'Q':
                    canWhiteCastleQueenSide = true;
                    break;
                case 'k':
                    canBlackCastleKingSide = true;
                    break;
                case 'q':
                    canBlackCastleQueenSide = true;
                    break;
            }
        }
    }
}
