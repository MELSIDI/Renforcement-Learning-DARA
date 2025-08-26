from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color
        self.pawns_left = 12

    def capture_pawn(self):
        self.pawns_left -= 1

    def __str__(self):
        return f"Player Id : {self.player_id}\nPawns Lefts : {self.pawns_left}"

    @abstractmethod
    def take_turn(self, game):
        """
            Gère le tour du joueur.
            La logique est implémentée dans les classes filles (humain ou IA).
        """
        pass


class HumanPlayer(Player):
    def take_turn(self, game):
        # La logique de prise de décision pour un joueur humain se fait via le clic de souris.
        # Nous n'avons rien à faire ici, la boucle principale de 'Game'
        # continuera d'attendre un événement de clic.
        pass