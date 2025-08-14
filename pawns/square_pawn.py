from .pawn import Pawn
from constants import *
import pygame


class SquarePawn(Pawn):
    def __init__(self, player_id, color):
        super().__init__(player_id, color)
        self.size = SQUARE_SIZE - 20

    def draw(self, screen, x, y):
        rect = pygame.Rect(x - self.size // 2, y - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)

    def is_valid_move(self, start_coords, end_coords):
        y_start, x_start = start_coords
        y_end, x_end = end_coords

        dx = abs(x_end - x_start)
        dy = abs(y_end - y_start)

        return dx == 1 and dy == 1