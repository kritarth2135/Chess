import sys
import pygame
pygame.init()

import constants as const
from board import Board
from pieces import Empty
# from inputs import input_str_to_movement_tuple
import errors

def main():
    if len(sys.argv) == 2:
        starting_fen = sys.argv[1]
    else:
        starting_fen = const.DEFAULT_FEN
    
    try:
        board = Board(starting_fen)
    except errors.InvalidFEN:
        print("Invalid FEN string passed.")
        sys.exit(1)

    screen = pygame.display.set_mode((const.BOARD_WIDTH, const.BOARD_HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    chess_board: pygame.Surface = pygame.image.load("assets/chess_board.png")
    chess_board.convert()
    chess_board_rect = chess_board.get_rect()

    running = True
    while running:
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                ...
            if event.type == pygame.QUIT:
                running = False

        print(clock.get_fps())

        screen.blit(pygame.transform.scale(chess_board, (const.BOARD_HEIGHT, const.BOARD_HEIGHT)), chess_board_rect)
        blit_icons(screen, board)
        pygame.display.update()

    pygame.quit()

def blit_icons(screen: pygame.Surface, board: Board) -> None:
    for rank in range(const.SIZE):
        for file in range(const.SIZE):
            if isinstance(board.grid.array[rank][file], Empty):
                continue
            icon: pygame.Surface = board.grid.array[rank][file].icon
            icon.convert()
            screen.blit(
                pygame.transform.scale(icon, (const.PIECE_WIDTH, const.PIECE_HEIGHT)),
                (const.X_OFFSET + (file * const.GRID_SIZE), const.Y_OFFSET + (rank * const.GRID_SIZE))
            )

if __name__ == "__main__":
    main()