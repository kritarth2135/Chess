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
    dragging: bool = False
    selected_piece: PositionTuple = PositionTuple((0, 0))
    
    while running:
        clock.tick(const.MAX_FPS)
        # clock.tick()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rank in range(const.SIZE):
                    for file in range(const.SIZE):
                        if board.grid.array[rank][file].color != const.EMPTY and board.grid.array[rank][file].rect.collidepoint(event.pos):
                            selected_piece.update(PositionTuple((rank, file)))
                            dragging = True

                            board.grid[selected_piece].rect.center = event.pos
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                board.grid[selected_piece].rect.x = const.X_OFFSET + (((event.pos[0] - const.X_OFFSET) // const.GRID_SIZE) * const.GRID_SIZE)
                board.grid[selected_piece].rect.y = const.Y_OFFSET + (((event.pos[1] - const.Y_OFFSET) // const.GRID_SIZE) * const.GRID_SIZE)
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    board.grid[selected_piece].rect.center = event.pos

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
