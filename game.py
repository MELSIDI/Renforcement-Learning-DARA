import pygame
import sys
import copy
import datetime
import os
from time import sleep
from boards.board import Board
from players.player import HumanPlayer
from constants import *
from pawns.round_pawn import RoundPawn


class Game:
    def __init__(self, board, player1, player2):
        # Initialisation de Pygame et des composants de base du jeu
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Jeu de l'alignement")

        self.FONT = pygame.font.Font(None, FONT_SIZE)

        # Les composants sont maintenant passés en paramètres pour plus de flexibilité
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

        # Variables de l'état du jeu
        self.phase = "placement"
        self.placement_turn = 0
        self.selected_pawn_coords = None
        self.message_info = "Player 1, place your first pawn."
        self.game_over = False
        self.position_history = []

        # Historique des coups pour la sauvegarde
        self.player1_moves = []
        self.player2_moves = []
        self.winner = None
        self.running = True

    def draw_text(self, text, y_pos, color=BLACK):
        """Affiche un texte centré sur l'écran."""
        text_surface = self.FONT.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, y_pos))
        self.screen.blit(text_surface, text_rect)

    def draw_message(self, message, color=BLACK):
        """Affiche le message d'information du jeu."""
        self.draw_text(message, MESSAGE_POS, color)

    def draw_move_history(self):
        """Affiche l'historique des coups sur les côtés de l'écran."""
        y_start = 50
        x_p1 = MARGIN_X // 2
        x_p2 = WINDOW_SIZE[0] - MARGIN_X // 2

        # Titres des joueurs
        p1_title_surface = self.FONT.render(f"{self.player1.player_id}", True, self.player1.color)
        p1_title_rect = p1_title_surface.get_rect(midtop=(x_p1, y_start))
        self.screen.blit(p1_title_surface, p1_title_rect)

        p2_title_surface = self.FONT.render(f"{self.player2.player_id}", True, self.player2.color)
        p2_title_rect = p2_title_surface.get_rect(midtop=(x_p2, y_start))
        self.screen.blit(p2_title_surface, p2_title_rect)

        y_start += 40
        # Pions Restant par Joueur
        p1_pawns_surface = self.FONT.render(f"Pawns Lefts : {self.player1.pawns_left}", True, self.player1.color)
        p1_pawns_rect = p1_pawns_surface.get_rect(midtop=(x_p1, y_start))
        self.screen.blit(p1_pawns_surface, p1_pawns_rect)

        p2_pawns_surface = self.FONT.render(f"Pawns Lefts : {self.player2.pawns_left}", True, self.player2.color)
        p2_pawns_rect = p2_pawns_surface.get_rect(midtop=(x_p2, y_start))
        self.screen.blit(p2_pawns_surface, p2_pawns_rect)

        # Affichage des 12 derniers coups
        y_offset = y_start + 40
        last_player1_moves = self.player1_moves[-12:] if len(self.player1_moves) > 12 else self.player1_moves
        for move in last_player1_moves:
            move_surface = self.FONT.render(move, True, self.player1.color)
            move_rect = move_surface.get_rect(midtop=(x_p1, y_offset))
            self.screen.blit(move_surface, move_rect)
            y_offset += 25

        y_offset = y_start + 40
        last_player2_moves = self.player2_moves[-12:] if len(self.player2_moves) > 12 else self.player2_moves
        for move in last_player2_moves:
            move_surface = self.FONT.render(move, True, self.player2.color)
            move_rect = move_surface.get_rect(midtop=(x_p2, y_offset))
            self.screen.blit(move_surface, move_rect)
            y_offset += 25

    def get_chess_notation(self, y, x):
        """Convertit des coordonnées de grille en notation de type échiquier (e.g. (0,0) -> 'a1')."""
        column_char = chr(ord('a') + x)
        row_num = GRID_Y_SIZE - y
        return f"{column_char}{row_num}"

    def get_grid_coords(self, pos):
        """Convertit les coordonnées de la souris en coordonnées de grille."""
        x, y = pos
        if MARGIN_X <= x < MARGIN_X + GRID_X_SIZE * SQUARE_SIZE and \
                MARGIN_Y <= y < MARGIN_Y + GRID_Y_SIZE * SQUARE_SIZE:
            col = (x - MARGIN_X) // SQUARE_SIZE
            row = (y - MARGIN_Y) // SQUARE_SIZE
            return row, col
        return None

    def update_history(self):
        """Sauvegarde l'état du plateau dans l'historique."""
        self.position_history.append(copy.deepcopy(self.board.grid))

    def save_game_history_to_file(self):
        """Sauvegarde l'historique complet de la partie dans un fichier texte."""
        directory = "dataset"
        if not os.path.exists(directory):
            os.makedirs(directory)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"game_history_{timestamp}.txt"
        file_path = os.path.join(directory, filename)

        with open(file_path, "w") as f:
            f.write(f"Game History - Winner: Player {self.winner}\n\n")

            max_len = max(len(self.player1_moves), len(self.player2_moves))
            for i in range(max_len):
                p1_move = self.player1_moves[i] if i < len(self.player1_moves) else ""
                p2_move = self.player2_moves[i] if i < len(self.player2_moves) else ""
                f.write(f"Turn {i + 1}:\n")
                f.write(f"  Player 1: {p1_move}\n")
                f.write(f"  Player 2: {p2_move}\n")
                f.write("-" * 20 + "\n")

    def has_valid_moves(self, player_id):
        """
        Vérifie si le joueur `player_id` a au moins un coup valide sur le plateau.
        Cette méthode parcourt toutes les pièces du joueur et vérifie s'il existe
        au moins une case adjacente vide où il peut se déplacer.
        """
        for y in range(GRID_Y_SIZE):
            for x in range(GRID_X_SIZE):
                pawn = self.board.grid[y][x]
                if pawn and pawn.player_id == player_id:
                    # Vérifie les 4 directions autour du pion (haut, bas, gauche, droite)
                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_y, new_x = y + dy, x + dx
                        # Vérifie si les nouvelles coordonnées sont dans les limites du plateau
                        if 0 <= new_y < GRID_Y_SIZE and 0 <= new_x < GRID_X_SIZE:
                            # Si la case adjacente est vide, c'est un coup valide
                            if not self.board.grid[new_y][new_x]:
                                return True
        return False

    def handle_placement_click(self, coords):
        """Gère les clics de la souris pendant la phase de placement des pions."""
        y, x = coords
        if not self.board.grid[y][x]:
            self.board.grid[y][x] = RoundPawn(self.current_player.player_id, self.current_player.color)

            if self.board.check_for_alignment(y, x, self.current_player.player_id):
                self.board.grid[y][x] = None
                self.message_info = "Invalid move. You cannot form a 3-pawn alignment during placement."
            else:
                notation = f"_,{self.get_chess_notation(y, x)}"
                if self.current_player == self.player1:
                    self.player1_moves.append(notation)
                else:
                    self.player2_moves.append(notation)

                self.update_history()
                self.placement_turn += 1
                if self.placement_turn == self.player1.pawns_left + self.player2.pawns_left:
                    self.phase = "game"
                    self.current_player = self.player1
                    self.message_info = f"Placement finished. {self.player1.player_id}, select a pawn to move."
                    # Vérification après le placement : le joueur qui commence le mouvement est-il bloqué ?
                    if not self.has_valid_moves(self.current_player.player_id):
                        self.game_over = True
                        self.winner = self.player2.player_id if self.current_player == self.player1 else self.player1.player_id
                        self.message_info = f"Player {self.current_player.player_id} is blocked. Player {self.winner} wins!"
                        self.running = False
                else:
                    self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                    self.message_info = f"Placement turn for {self.current_player.player_id}."
        else:
            self.message_info = "Invalid spot. The square must be empty."

    def handle_game_click(self, coords):
        """Gère les clics de la souris pendant la phase de mouvement."""
        y_end, x_end = coords
        if self.selected_pawn_coords is None:
            if self.board.grid[y_end][x_end] and self.board.grid[y_end][x_end].player_id == self.current_player.player_id:
                self.selected_pawn_coords = (y_end, x_end)
                self.message_info = "Pawn selected. Click on the destination square."
            else:
                self.message_info = "That's not your pawn or the square is empty."
        else:
            y_start, x_start = self.selected_pawn_coords
            pawn_to_move = self.board.grid[y_start][x_start]

            if pawn_to_move.is_valid_move((y_start, x_start), (y_end, x_end)):
                if not self.board.grid[y_end][x_end]:
                    self.board.grid[y_end][x_end] = pawn_to_move
                    self.board.grid[y_start][x_start] = None

                    notation = f"{self.get_chess_notation(y_start, x_start)},{self.get_chess_notation(y_end, x_end)}"

                    if self.board.check_for_alignment(y_end, x_end, self.current_player.player_id):
                        if self.current_player == self.player1:
                            self.player1_moves.append(notation)
                        else:
                            self.player2_moves.append(notation)
                        self.update_history()
                        self.phase = "capture"
                        self.message_info = "Alignment! Click on an opponent's pawn to capture."
                    else:
                        if self.current_player == self.player1:
                            self.player1_moves.append(notation)
                        else:
                            self.player2_moves.append(notation)
                        self.update_history()
                        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                        self.message_info = f"Turn for {self.current_player.player_id}. Move a pawn."
                        # Vérification après un coup : le prochain joueur est-il bloqué ?
                        if not self.has_valid_moves(self.current_player.player_id):
                            self.game_over = True
                            self.winner = self.player2.player_id if self.current_player == self.player1 else self.player1.player_id
                            self.message_info = f"Player {self.current_player.player_id} is blocked. Player {self.winner} wins!"
                            self.running = False
                    self.selected_pawn_coords = None
                else:
                    self.message_info = "Invalid move. The destination square is occupied."
                    self.selected_pawn_coords = None
            else:
                self.message_info = "Invalid move. This pawn cannot move that way."
                self.selected_pawn_coords = None

    def handle_capture_click(self, coords):
        """Gère les clics de la souris pendant la phase de capture."""
        y, x = coords
        opponent = self.player2 if self.current_player == self.player1 else self.player1
        if self.board.grid[y][x] and self.board.grid[y][x].player_id == opponent.player_id:
            captured_pawn_notation = self.get_chess_notation(y, x)
            self.board.grid[y][x] = None

            if self.current_player == self.player1:
                self.player1_moves[-1] += f"->{captured_pawn_notation}"
            else:
                self.player2_moves[-1] += f"->{captured_pawn_notation}"

            opponent.capture_pawn()
            if opponent.pawns_left < 3:
                self.game_over = True
                self.winner = self.current_player.player_id
                self.message_info = f"Player {self.current_player.player_id} wins!"
                self.running = False
            else:
                self.update_history()
                self.phase = "game"
                self.current_player = opponent
                self.message_info = f"Opponent's pawn captured! It's {self.current_player.player_id}'s turn."
                # Vérification après la capture : le prochain joueur est-il bloqué ?
                if not self.has_valid_moves(self.current_player.player_id):
                    self.game_over = True
                    self.winner = self.player2.player_id if self.current_player == self.player1 \
                        else self.player1.player_id
                    self.message_info = f"Player {self.current_player.player_id} is blocked. Player {self.winner} wins!"
                    self.running = False
        else:
            self.message_info = "Invalid coords or not an opponent's pawn. Try again."

    def run(self):
        """La boucle de jeu principale."""

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Le joueur humain prend son tour via les clics de souris
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if isinstance(self.current_player, HumanPlayer):
                        coords = self.get_grid_coords(event.pos)
                        if coords:
                            if self.phase == "placement":
                                self.handle_placement_click(coords)
                            elif self.phase == "game":
                                self.handle_game_click(coords)
                            elif self.phase == "capture":
                                self.handle_capture_click(coords)

            # Le tour de l'IA est géré ICI
            if not isinstance(self.current_player, HumanPlayer) and not self.game_over:
                self.current_player.take_turn(self)

            self.board.draw(self.screen, self.selected_pawn_coords, self.FONT)
            self.draw_message(self.message_info, self.current_player.color if self.phase != "capture" else BLACK)
            self.draw_move_history()
            pygame.display.flip()

            if not isinstance(self.current_player, HumanPlayer) and not self.game_over:
                pygame.time.wait(10000)


        self.save_game_history_to_file()
        pygame.quit()
        sys.exit()
