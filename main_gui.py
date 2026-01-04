import sys
import pygame

import constants as const
from board import Board
from pieces import Empty
from positions import PositionTuple
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

    pygame.init()
    screen = pygame.display.set_mode((const.BOARD_WIDTH, const.BOARD_HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    chess_board: pygame.Surface = pygame.image.load("assets/chess_board.png")
    chess_board.convert()
    chess_board_rect = chess_board.get_rect()

    running: bool = True
    while running:
        clock.tick(const.MAX_FPS)
        selected_piece: PositionTuple | None = None

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rank in range(const.SIZE):
                    for file in range(const.SIZE):
                        if board.grid.array[rank][file].color != const.EMPTY and board.grid.array[rank][file].rect.collidepoint(event.pos):
                            selected_piece = PositionTuple((rank, file))
                            board.grid[selected_piece].rect.centerx = event.pos[0]
                            board.grid[selected_piece].rect.centery = event.pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_piece = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    board.grid[selected_piece].rect.centerx = event.pos[0]
                    board.grid[selected_piece].rect.centery = event.pos[1]

        screen.blit(pygame.transform.scale(chess_board, (const.BOARD_HEIGHT, const.BOARD_HEIGHT)), chess_board_rect)
        blit_icons(screen, board)
        pygame.display.update()
        # print(clock.get_fps())

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
                board.grid.array[rank][file].rect
            )

if __name__ == "__main__":
    main()
