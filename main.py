# main.py
import pygame
from game import Game
from boards.board import Board
from player import Player
from  constants import RED, BLUE
#from ai.random_ai import RandomAI

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # Définir les composants du jeu
    board = Board()
    human_player1 = Player("J1", RED)
    human_player2 = Player("J2", BLUE)
    #ai_player = RandomAI("IA", BLUE)

    # Créer une instance de Game en utilisant ces composants
    my_game = Game(board, human_player1, human_player2)
    my_game.run()