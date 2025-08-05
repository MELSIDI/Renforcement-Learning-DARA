class Pawn:
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color

    def __repr__(self):
        return f"Pawn({self.player_id})"