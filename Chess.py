import pygame
from pygame.locals import *
from pygame import transform


class Piece:
    def __init__(self, rect, pos, piece_name):
        self.rect = rect
        self.pos = pos
        self.name = piece_name


class Player:
    def __init__(self, player, piecesSprite):
        self.pieceNames = ["K", "Q", "LR", "RR", "LB", "RB", "LK", "RK", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
        self.player = player
        self.pieces = []

    def make_pieces(self):
        x = 5
        if self.player == 1:
            y = 5
        else:
            y = 10000

        for piece in self.pieceNames:
            pass


    def move_piece(self):
        choice = False


class ChessGame:
    def __init__(self, player_1, player_2):
        self.p1 = player_1
        self.p2 = player_2
