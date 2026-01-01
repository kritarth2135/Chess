import pygame
pygame.init()

import constants as const
from board import Board
from inputs import input_str_to_movement_tuple
import errors

chess_board = pygame.image.load("assets/chess_board.png")
chess_board.convert()
chess_board_rect = chess_board.get_rect()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess")

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.blit(chess_board, chess_board_rect)
    pygame.display.update()

pygame.quit()
