from .pawn import Pawn
from constants import *
import pygame


class RoundPawn(Pawn):
    def __init__(self, player_id, color):
        super().__init__(player_id, color)
        self.radius = PAWN_RADIUS

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.color, (x, y), self.radius)

    def is_valid_move(self, start_coords, end_coords):
        y_start, x_start = start_coords
        y_end, x_end = end_coords

        dx = abs(x_end - x_start)
        dy = abs(y_end - y_start)

        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)