import sys
import pygame

import constants as const
from board import Board
from pieces import Piece
from positions import PositionTuple, MovementTuple
import errors

def main_gui(starting_fen: str):
    """Runs game in GUI using pygame."""

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

    check_background: pygame.Surface = pygame.image.load("assets/check_background.png")
    check_background.convert()
    check_background = pygame.transform.scale(check_background, (const.PIECE_HEIGHT, const.PIECE_WIDTH))

    all_sprites: AllSprites = AllSprites(board)

    running: bool = True
    dragging: bool = False
    dragged_sprite_index: int = 0
    initial_position: PositionTuple = const.SENTINAL_POSITION
    final_position: PositionTuple = const.SENTINAL_POSITION

    while running:
        clock.tick(const.MAX_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos: tuple[int, int] = event.pos
                for index, sprite in enumerate(all_sprites.sprites):
                    if sprite.rect.collidepoint(pos):
                        all_sprites.append_backup_sprites()
                        dragging = True
                        dragged_sprite_index = index
                        sprite.rect.center = pos

                        initial_position = position_to_positiontuple(pos)
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                pos: tuple[int, int] = event.pos
                if is_position_out_of_bounds(pos):
                    dragging = False
                    all_sprites.restore()
                elif dragging:
                    dragging = False
                    pos = position_to_grid_position(pos)
                    all_sprites.sprites[dragged_sprite_index].rect.x = pos[0]
                    all_sprites.sprites[dragged_sprite_index].rect.y = pos[1]

                    final_position = position_to_positiontuple(pos)

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    all_sprites.sprites[dragged_sprite_index].rect.center = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    try:
                        all_sprites.undo(board)
                    except errors.NoMoreUndos as e:
                        print(f"{const.RED}{e}{const.RESET}")

        try:
            if (not initial_position.is_out_of_bounds()) and  (not final_position.is_out_of_bounds()):
                print(initial_position, final_position)
                board.move(MovementTuple((initial_position, final_position)))
                initial_position = const.SENTINAL_POSITION
                final_position = const.SENTINAL_POSITION

                for index, sprite in enumerate(all_sprites.sprites):
                    if sprite.piece in board.captured_pieces:
                        all_sprites.sprites.pop(index)
    
            screen.blit(pygame.transform.scale(chess_board, (const.BOARD_HEIGHT, const.BOARD_HEIGHT)), chess_board_rect)
            for sprite in all_sprites.sprites:
                screen.blit(sprite.icon, sprite.rect)
                if sprite.piece.name == const.KING and sprite.piece.is_under_Check:
                    screen.blit(check_background, sprite.rect)
            pygame.display.update()


        except errors.CustomException as e:
            initial_position = const.SENTINAL_POSITION
            final_position = const.SENTINAL_POSITION
            all_sprites.restore()
            print(f"{const.RED}{e}{const.RESET}")

    pygame.quit()


class PieceSprite(pygame.sprite.Sprite):
    """
    Class to generate a sprite for each piece.

    Args:
        piece: The Piece for which the sprite is to be made.

    Attributes:
        piece
        image: Pygame surface for the icon of the piece.
        rect: Pygame rect for the image.
    """

    def __init__(self, piece: Piece) -> None:
        super().__init__()
        self.piece: Piece = piece
        self.icon: pygame.Surface = pygame.transform.scale(piece.icon, (const.PIECE_HEIGHT, const.PIECE_HEIGHT))
        self.rect: pygame.Rect = self.image.get_rect() 
        self.rect.x = const.X_OFFSET + (piece.position.file * const.GRID_BOX_SIZE)
        self.rect.y = const.Y_OFFSET + (piece.position.rank * const.GRID_BOX_SIZE)
        self.rect.width = const.PIECE_WIDTH
        self.rect.height = const.PIECE_HEIGHT

    def copy(self):
        """Create a deepcopy of PieceSprite."""

        copy: PieceSprite = PieceSprite(self.piece)
        copy.rect = self.rect.copy()
        return copy


class AllSprites:
    """
    Class to keep track of all the sprites (pieces) on the board.

    Args:
        board: The Board for which it is to be initialised.

    Attributes:
        sprites: A list of PieceSprite of all pieces on the board.
        backup_sprites: A list of 'sprites' for restoring the board in case of illegal move.
    """

    def __init__(self, board: Board) -> None:
        self.sprites: list[PieceSprite] = []
        for rank in range(const.GRID_SIZE):
            for file in range(const.GRID_SIZE):
                if board.grid.array[rank][file].color == const.EMPTY:
                    continue
                self.sprites.append(PieceSprite(board.grid.array[rank][file]))

        self.create_backup_sprite()

    def create_backup_sprite(self) -> None:
        """Creates a backup of sprites list."""

        self.backup_sprites: list[list[PieceSprite]] = []
        self.backup_sprites.append(self.append_backup_sprites())

    def append_backup_sprites(self) -> list[PieceSprite]:
        """Creates a deepcopy of sprites and appends it to backup_sprites"""

        temp_backup: list[PieceSprite] = []
        for sprite in self.sprites:
            temp_backup.append(sprite.copy())
        self.backup_sprites.append(temp_backup)

    def restore(self) -> None:
        """Restores all the sprites to the latest backup."""

        if self.backup_sprites:
            self.sprites = self.backup_sprites.pop()

    def undo(self, board: Board) -> None:
        """Undo's the latest move."""

        if not board.move_history or not self.backup_sprites:
            raise errors.NoMoreUndos
        board.undo()
        self.restore()


def is_position_out_of_bounds(pos: tuple[int, int]) -> bool:
    """Returns True if position of pixel is out of the board's grid."""

    return (
        pos[const.X_VALUE] < const.VALID_X_LOWER_BOUND
        or pos[const.X_VALUE] > const.VALID_X_UPPER_BOUND
        or pos[const.Y_VALUE] < const.VALID_Y_LOWER_BOUND
        or pos[const.Y_VALUE] > const.VALID_Y_UPPER_BOUND
    )


def position_to_grid_position(pos: tuple[int, int]) -> tuple[int, int]:
    """Converts position of pixel to position of first pixel of corresponding grid box for snapping pieces to grid."""

    grid_pos: list[int] = []
    grid_pos.append(const.X_OFFSET + (((pos[const.X_VALUE] - const.X_OFFSET) // const.GRID_BOX_SIZE) * const.GRID_BOX_SIZE))
    grid_pos.append(const.Y_OFFSET + (((pos[const.Y_VALUE] - const.Y_OFFSET) // const.GRID_BOX_SIZE) * const.GRID_BOX_SIZE))
    return tuple(grid_pos) #type: ignore


def position_to_positiontuple(pos: tuple[int, int]) -> PositionTuple:
    """Converts position of pixel on the board to corresponding PositionTuple."""

    return PositionTuple((
        ((pos[const.Y_VALUE] - const.Y_OFFSET) // const.GRID_BOX_SIZE),
        ((pos[const.X_VALUE] - const.X_OFFSET) // const.GRID_BOX_SIZE)
    ))


if __name__ == "__main__":
    main_gui(const.DEFAULT_FEN)
