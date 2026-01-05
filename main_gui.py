import sys
import pygame

import constants as const
from board import Board
from pieces import Piece
# from positions import PositionTuple, MovementTuple
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

    all_piece_sprites: list[PieceSprite] = []
    initialize_sprites(board, all_piece_sprites)

    running: bool = True
    dragging: bool = False
    dragging_index: int = 0
    
    while running:
        clock.tick(const.MAX_FPS)
        # clock.tick()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = not running
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos: tuple[int, int] = event.pos
                for index, sprite in enumerate(all_piece_sprites):
                    if sprite.rect.collidepoint(pos[const.X_VALUE], pos[const.Y_VALUE]):
                        dragging = not dragging
                        dragging_index = index
                        sprite.rect.center = pos
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = not dragging
                pos: tuple[int, int] = event.pos
                all_piece_sprites[dragging_index].rect.x = const.X_OFFSET + (((pos[const.X_VALUE] - const.X_OFFSET) // const.GRID_SIZE) * const.GRID_SIZE)
                all_piece_sprites[dragging_index].rect.y = const.Y_OFFSET + (((pos[const.Y_VALUE] - const.Y_OFFSET) // const.GRID_SIZE) * const.GRID_SIZE)
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    all_piece_sprites[dragging_index].rect.center = event.pos
                    

        # try:
        #     if initial_position != const.SENTINAL_POSITION and final_position != const.SENTINAL_POSITION:
        #         board.move(MovementTuple((initial_position, final_position)))
        # except errors.CustomException as e:
        #     print(f"{const.RED}{e}{const.RESET}")

        screen.blit(pygame.transform.scale(chess_board, (const.BOARD_HEIGHT, const.BOARD_HEIGHT)), chess_board_rect)
        for sprite in all_piece_sprites:
            screen.blit(sprite.image, sprite.rect)
        pygame.display.update()
        # print(clock.get_fps())

    pygame.quit()

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece: Piece) -> None:
        super().__init__()
        self.piece: Piece = piece
        self.image: pygame.Surface = pygame.transform.scale(piece.icon, (const.PIECE_HEIGHT, const.PIECE_HEIGHT))
        self.rect: pygame.Rect = self.image.get_rect() 
        self.rect.x = const.X_OFFSET + (piece.position.file * const.GRID_SIZE)
        self.rect.y = const.Y_OFFSET + (piece.position.rank * const.GRID_SIZE)
        self.rect.width = const.PIECE_WIDTH
        self.rect.height = const.PIECE_HEIGHT


def initialize_sprites(board: Board, all_piece_sprites: list[PieceSprite]) -> None:
    for rank in range(const.SIZE):
        for file in range(const.SIZE):
            if board.grid.array[rank][file].color == const.EMPTY:
                continue
            all_piece_sprites.append(PieceSprite(board.grid.array[rank][file]))


if __name__ == "__main__":
    main()
