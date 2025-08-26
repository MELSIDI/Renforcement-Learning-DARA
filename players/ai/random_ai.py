from random import choice
from players.player import Player
from constants import GRID_X_SIZE, GRID_Y_SIZE
from pawns.round_pawn import RoundPawn


class RandomAI(Player):
    def take_turn(self, game):
        """
        Gère le tour de l'IA de manière aléatoire.
        :param game: le Jeu dans le quelle joue l'IA
        :return: RIEN
        """
        if game.phase == "placement":
            valid_moves = self.get_valid_placement_moves(game.board)
            if valid_moves:
                coords = choice(valid_moves)
                game.handle_placement_click(coords)
        elif game.phase == "game":
            valid_moves = self.get_valid_movement_moves(game.board)
            if valid_moves:
                start_coords, end_coords = choice(valid_moves)
                game.selected_pawn_coords = start_coords
                game.handle_game_click(end_coords)
            else:
                # Si l'IA n'as pas de coups valides, elle est bloquée
                game.game_over = True
                opponent = game.player2 if self == game.player1 else game.player1
                game.winner = opponent.player_id
                game.message_info = f"Player {self.player_id} is blocked. Player {game.winner} wins!"
                game.running = False
        elif game.phase == "capture":
            opponent = game.player2 if self == game.player1 else game.player1
            capturable_pawns = self.get_capturable_pawns(game.board, opponent.player_id)
            if capturable_pawns:
                coords = choice(capturable_pawns)
                game.handle_capture_click(coords)

    def get_valid_placement_moves(self, board):
        """
        Trouve et Retourne une liste de toutes les positions de placement
         valides sur l'echiquier .
        :param board: L'echiquier
        :return: une liste de coordonnées d'emplacements valides
        """
        valid_moves = []
        for y in range(GRID_Y_SIZE):
            for x in range(GRID_X_SIZE):
                if not board.grid[y][x]:
                    # Crée un pion temporaire pour vérifier si le placement est valide
                    temp_pawn = RoundPawn(self.player_id, self.color)
                    board.grid[y][x] = temp_pawn
                    if not board.check_for_alignment(y, x, self.player_id):
                        valid_moves.append((y, x))
                    board.grid[y][x] = None  # Retire le pion temporaire
        return valid_moves

    def get_valid_movement_moves(self, board):
        """
        Retourne une liste de tous les mouvements valides pour tous les pions de l'IA.
        :param board: L'echiquier
        :return: une liste de coordonnées mouvements valides
        """
        valid_moves = []
        for y_start in range(GRID_Y_SIZE):
            for x_start in range(GRID_X_SIZE):
                pawn = board.grid[y_start][x_start]
                if pawn and pawn.player_id == self.player_id:
                    # Vérifie les mouvements vers les cases adjacentes vides
                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        y_end, x_end = y_start + dy, x_start + dx
                        if 0 <= y_end < GRID_Y_SIZE and 0 <= x_end < GRID_X_SIZE:
                            if not board.grid[y_end][x_end]:
                                valid_moves.append(((y_start, x_start), (y_end, x_end)))
        return valid_moves

    @staticmethod
    def get_capturable_pawns(board, opponent_id):
        """
        Retourne une liste de tous les pions adverses qui peuvent être capturés.
        :param board: L'Echiquier
        :param opponent_id: l'Id de l'adverseur
        :return: une liste de coordonées de pions capturables
        """
        capturable_pawns = []
        for y in range(GRID_Y_SIZE):
            for x in range(GRID_X_SIZE):
                pawn = board.grid[y][x]
                if pawn and pawn.player_id == opponent_id:
                    capturable_pawns.append((y, x))
        return capturable_pawns
