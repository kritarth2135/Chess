import sys
import pygame

import constants as const
from board import Board
from pieces import Piece
from positions import PositionTuple, MovementTuple
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

    sprites: AllSprites = AllSprites(board)
    backup_sprites: list[PieceSprite] = sprites.create_backup()

    running: bool = True
    dragging: bool = False
    dragged_sprite_index: int = 0
    initial_position: PositionTuple = const.SENTINAL_POSITION
    final_position: PositionTuple = const.SENTINAL_POSITION
    
    while running:
        clock.tick(const.MAX_FPS)
        # clock.tick()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos: tuple[int, int] = event.pos
                for index, sprite in enumerate(sprites.sprites):
                    if sprite.rect.collidepoint(pos):
                        # backup_sprites = sprites.create_backup()
                        dragging = True
                        dragged_sprite_index = index
                        sprite.rect.center = pos
                        
                        initial_position = PositionTuple((
                            ((pos[const.Y_VALUE] - const.Y_OFFSET) // const.GRID_SIZE),
                            ((pos[const.X_VALUE] - const.X_OFFSET) // const.GRID_SIZE)
                        ))
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    pos: tuple[int, int] = event.pos
                    sprites.sprites[dragged_sprite_index].rect.x = const.X_OFFSET + (((pos[const.X_VALUE] - const.X_OFFSET) // const.GRID_SIZE) * const.GRID_SIZE)
                    sprites.sprites[dragged_sprite_index].rect.y = const.Y_OFFSET + (((pos[const.Y_VALUE] - const.Y_OFFSET) // const.GRID_SIZE) * const.GRID_SIZE)

                    final_position = PositionTuple((
                        ((pos[const.Y_VALUE] - const.Y_OFFSET) // const.GRID_SIZE),
                        ((pos[const.X_VALUE] - const.X_OFFSET) // const.GRID_SIZE)
                    ))

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    sprites.sprites[dragged_sprite_index].rect.center = event.pos
                    
        try:
            if (not initial_position.is_out_of_bounds()) and  (not final_position.is_out_of_bounds()):
                print(initial_position, final_position)
                board.move(MovementTuple((initial_position, final_position)))
                initial_position = const.SENTINAL_POSITION
                final_position = const.SENTINAL_POSITION

        except errors.CustomException as e:
            initial_position = const.SENTINAL_POSITION
            final_position = const.SENTINAL_POSITION
            sprites.restore(backup_sprites)
            print(f"{const.RED}{e}{const.RESET}")

        screen.blit(pygame.transform.scale(chess_board, (const.BOARD_HEIGHT, const.BOARD_HEIGHT)), chess_board_rect)
        for sprite in sprites.sprites:
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
        self.rect.width = round(const.PIECE_WIDTH * 0.8) if piece.name == const.PAWN else const.PIECE_WIDTH
        self.rect.height = round(const.PIECE_HEIGHT * 0.8) if piece.name == const.PAWN else const.PIECE_HEIGHT

    def copy(self):
        copy: PieceSprite = PieceSprite(self.piece)
        copy.rect = self.rect
        return copy


class AllSprites:
    def __init__(self, board: Board) -> None:
        self.sprites: list[PieceSprite] = []
        for rank in range(const.SIZE):
            for file in range(const.SIZE):
                if board.grid.array[rank][file].color == const.EMPTY:
                    continue
                self.sprites.append(PieceSprite(board.grid.array[rank][file]))
    
    def add(self, sprite: PieceSprite) -> None:
        self.sprites.append(sprite)

    def create_backup(self) -> list[PieceSprite]:
        backup: list[PieceSprite] = []
        for sprite in self.sprites:
            backup.append(sprite.copy())
        return backup

    def restore(self, sprites: list[PieceSprite]) -> None:
        self.sprites = sprites


if __name__ == "__main__":
    main()
