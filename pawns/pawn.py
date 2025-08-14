from abc import ABC, abstractmethod
import pygame

class Pawn(ABC):
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color

    @abstractmethod
    def draw(self, screen, x, y):
        pass

    @abstractmethod
    def is_valid_move(self, start_coords, end_coords):
        pass