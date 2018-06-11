import pygame
from pygame.locals import *
from pygame import transform


class Piece(pygame.sprite.Sprite):
    def __init__(self, rect, piece_name):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.name = piece_name
        self.pos = (0, 0)

    def moveIt(self, newX, newY):
        self.pos = (newX, newY)


class Player:
    def __init__(self, player, piecesSprite, board):
        self.pieceNames = ["RR", "RK", "RB", "K", "Q", "LB", "LK", "LR", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
        self.player = player
        self.pieces = []
        self.pieceSprites = piecesSprite
        self.board = board
        self.opponent = None

    def make_pieces(self):
        if self.player == 1:
            y = 5
        else:
            y = 65
        self.pieces.append(Piece(Rect(220, y, 50, 50), "RR"))
        self.pieces.append(Piece(Rect(163, y, 50, 50), "RK"))
        self.pieces.append(Piece(Rect(107, y, 50, 50), "RB"))
        self.pieces.append(Piece(Rect(5, y, 50, 50), "K"))
        self.pieces.append(Piece(Rect(57, y, 50, 50), "Q"))
        self.pieces.append(Piece(Rect(107, y, 50, 50), "LB"))
        self.pieces.append(Piece(Rect(163, y, 50, 50), "LK"))
        self.pieces.append(Piece(Rect(220, y, 50, 50), "LR"))
        for i in range(8):
            self.pieces.append(Piece(Rect(267, y, 50, 50), "P{0}".format(i+1)))
        if self.player == 1:
            square_index = 0
            for piece in self.pieces:
                square = self.board.squares[square_index]
                piece.pos = (square.x, square.y)
                square_index += 1
        else:
            y = 65
            square_index = 63
            for piece in self.pieces:
                square = self.board.squares[square_index]
                piece.pos = (square.x, square.y)
                square_index -= 1



    def drawPieces(self):
        for piece in self.pieces:
            self.board.window.blit(self.pieceSprites, piece.pos, piece.rect)


    def move_piece(self):
        choice = False
        selctedAPiece = False
        while choice == False:
            ev = pygame.event.poll()
            if ev.type == KEYDOWN:
                key = ev.dict['key']
                if key == 27:
                    quit()
            if ev.type == MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                print(mouseX, mouseY)
                for piece in self.pieces:
                    if piece.rect.collidepoint(mouseX, mouseY):
                        selctedPiece = piece
                        selctedAPiece = True
                        print("Clicked Here")

                for square in self.board.squares:
                    if square.collidepoint(mouseX, mouseY):
                        if selctedAPiece == True:
                            if (square.x, square.y) != selctedPiece.pos:
                                selctedPiece.moveIt(square.x, square.y)
                                choice = True
                                print("Nope Here")

class Board:
    def __init__(self, window):
        self.squares = []
        self.window = window
        self.colors = [(0, 0, 255), (255, 0, 0)]

    def makeSquares(self):
        square_index = 0
        for j in range(8):
            y = j * 50
            square_index += 1
            for i in range(8):
                x = i * 50
                self.squares.append(Rect(x, y, 50, 50))
                c_index = square_index % 2
                self.window.fill(self.colors[c_index], Rect(x, y, 50, 50))
                square_index += 1

    def drawBoard(self):
        square_index = 0
        for j in range(8):
            y = j * 50
            square_index += 1
            for i in range(8):
                x = i * 50
                c_index = square_index % 2
                self.window.fill(self.colors[c_index], Rect(x, y, 50, 50))
                square_index += 1


class ChessGame:
    def __init__(self, window, pieceSprites):
        self.window = window
        self.board = Board(window)
        self.board.makeSquares()
        self.player1 = Player(1, pieceSprites, self.board)
        self.player2 = Player(2, pieceSprites, self.board)
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        self.player1.make_pieces()
        self.player2.make_pieces()

    def drawMatch(self):
        self.board.drawBoard()
        self.player1.drawPieces()
        self.player2.drawPieces()
        pygame.display.flip()

def main():
    pygame.init()
    timeKeeper = pygame.time.Clock()
    screenrect = Rect(0, 0, 400, 400)  # Size of screen.
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(screenrect.size, winstyle, 32)
    window= pygame.display.set_mode(screenrect.size, winstyle, bestdepth)
    thePiecesSprites = pygame.image.load("C:/Users/pratere/github/python/Summer_Projects_2018/ChessSprites.png")
    thePiecesSprites = pygame.transform.scale(thePiecesSprites, (320, 120))
    window.fill((200, 0, 0), screenrect)

    theGame = ChessGame(window, thePiecesSprites)
    theGame.drawMatch()
    pygame.display.flip()
    time = 0
    while 1:
        ev = pygame.event.poll()
        theGame.player1.move_piece()
        theGame.drawMatch()
        if ev.type == KEYDOWN:
            key = ev.dict['key']
            if key == 27:
                quit()
        timeKeeper.tick(60)
    pygame.quit()

main()
