import pygame
from game import Game
from boards.board import Board
from players.player import HumanPlayer
from constants import RED, BLUE
from players.ai.random_ai import RandomAI

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # Définir les composants du jeu
    board = Board()
    human_player1 = HumanPlayer("J1", RED)
    # human_player2 = HumanPlayer("J2", BLUE)
    ai_player = RandomAI("IA", BLUE)

    # Créer une instance de Game en utilisant ces composants
    my_game = Game(board, human_player1, ai_player)
    my_game.run()