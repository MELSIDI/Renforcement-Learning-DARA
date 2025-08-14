from constants import RED, BLUE

class Player:
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color
        self.pawns_left = 12

    def capture_pawn(self):
        self.pawns_left -= 1

    def __str__(self):
        return f"Player Id : {self.player_id}\nPawns Lefts : {self.pawns_left}"