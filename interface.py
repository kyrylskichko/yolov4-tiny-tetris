import pygame
from objects import Tetris


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (800, 1000)
screen = pygame.display.set_mode(size)

game = Tetris(20, 10)