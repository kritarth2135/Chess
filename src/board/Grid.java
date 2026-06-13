package src.board;

import src.pieces.*;

import static src.board.Board.BOARD_SIZE;

class Grid {
    private Piece[][] grid;

    public Grid(char[][] boardState) {
        grid = new Piece[BOARD_SIZE][BOARD_SIZE];

        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                switch (boardState[i][j]) {
                    case 'K' -> { grid[i][j] = new King(Color.WHITE); }
                    case 'Q' -> { grid[i][j] = new Queen(Color.WHITE); }
                    case 'R' -> { grid[i][j] = new Rook(Color.WHITE); }
                    case 'B' -> { grid[i][j] = new Bishop(Color.WHITE); }
                    case 'N' -> { grid[i][j] = new Knight(Color.WHITE); }
                    case 'P' -> { grid[i][j] = new Pawn(Color.WHITE); }
                    case 'k' -> { grid[i][j] = new King(Color.BLACK); }
                    case 'q' -> { grid[i][j] = new Queen(Color.BLACK); }
                    case 'r' -> { grid[i][j] = new Rook(Color.BLACK); }
                    case 'b' -> { grid[i][j] = new Bishop(Color.BLACK); }
                    case 'n' -> { grid[i][j] = new Knight(Color.BLACK); }
                    case 'p' -> { grid[i][j] = new Pawn(Color.BLACK); }
                    case '-' -> {}
                }
            }
        }
    }

    public void setPiece(int rank, int file, Piece piece) {
        grid[rank][file] = piece;
    }

    public Piece getPiece(int rank, int file) {
        return grid[rank][file];
    }
}