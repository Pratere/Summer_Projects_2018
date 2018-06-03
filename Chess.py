class Player():
    def __init__(self, player):
        self.pieceNames = ["K", "Q", "LR", "RR", "LB", "RB", "LK", "RK", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
        self.player = player


class ChessGame():
    def __init__(self, player_1, player_2):
        self.p1 = player_1
        self.p2 = player_2