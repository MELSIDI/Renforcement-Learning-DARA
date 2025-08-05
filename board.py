import pygame
from constants import *
from pawn import Pawn


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_X_SIZE)] for _ in range(GRID_Y_SIZE)]

    def draw(self, screen, selected_pawn_coords, font):
        screen.fill(WHITE)

        # Draw grid coordinates
        # Vertical labels (1, 2, 3, 4, 5)
        for y in range(GRID_Y_SIZE):
            label = font.render(str(GRID_Y_SIZE - y), True, BLACK)
            label_rect = label.get_rect(center=(MARGIN_X - 25, MARGIN_Y + y * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(label, label_rect)

        # Horizontal labels (a, b, c, d, e, f)
        for x in range(GRID_X_SIZE):
            label = font.render(chr(ord('a') + x), True, BLACK)
            label_rect = label.get_rect(center=(MARGIN_X + x * SQUARE_SIZE + SQUARE_SIZE // 2, MARGIN_Y - 25))
            screen.blit(label, label_rect)

        # Draw the grid
        for y in range(GRID_Y_SIZE):
            for x in range(GRID_X_SIZE):
                rect = pygame.Rect(MARGIN_X + x * SQUARE_SIZE, MARGIN_Y + y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

        # Draw the pawns
        for y in range(GRID_Y_SIZE):
            for x in range(GRID_X_SIZE):
                pawn = self.grid[y][x]
                if pawn:
                    center_x = MARGIN_X + x * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = MARGIN_Y + y * SQUARE_SIZE + SQUARE_SIZE // 2
                    pygame.draw.circle(screen, pawn.color, (center_x, center_y), PAWN_RADIUS)

        # Highlight the selected pawn
        if selected_pawn_coords:
            y, x = selected_pawn_coords
            center_x = MARGIN_X + x * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = MARGIN_Y + y * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, BLACK, (center_x, center_y), PAWN_RADIUS, 4)

    def check_for_alignment(self, y, x, player_id):
        # ... (le reste de la méthode reste inchangé)
        # Check for EXACTLY 3 pawns in a row (horizontal)
        for i in range(GRID_X_SIZE - 2):
            if (self.grid[y][i] and self.grid[y][i].player_id == player_id and
                    self.grid[y][i + 1] and self.grid[y][i + 1].player_id == player_id and
                    self.grid[y][i + 2] and self.grid[y][i + 2].player_id == player_id):

                is_exactly_3 = True
                if i > 0 and self.grid[y][i - 1] and self.grid[y][i - 1].player_id == player_id:
                    is_exactly_3 = False
                if i < GRID_X_SIZE - 3 and self.grid[y][i + 3] and self.grid[y][i + 3].player_id == player_id:
                    is_exactly_3 = False

                if is_exactly_3:
                    return True

        # Check for EXACTLY 3 pawns in a row (vertical)
        for i in range(GRID_Y_SIZE - 2):
            if (self.grid[i][x] and self.grid[i][x].player_id == player_id and
                    self.grid[i + 1][x] and self.grid[i + 1][x].player_id == player_id and
                    self.grid[i + 2][x] and self.grid[i + 2][x].player_id == player_id):

                is_exactly_3 = True
                if i > 0 and self.grid[i - 1][x] and self.grid[i - 1][x].player_id == player_id:
                    is_exactly_3 = False
                if i < GRID_Y_SIZE - 3 and self.grid[i + 3][x] and self.grid[i + 3][x].player_id == player_id:
                    is_exactly_3 = False

                if is_exactly_3:
                    return True

        return False