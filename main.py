import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    game = Game()
    game.run()