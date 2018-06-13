import pygame
from pygame.locals import *
from pygame import transform


class Piece(pygame.sprite.Sprite):
    def __init__(self, spriteRect, piece_name, player):
        pygame.sprite.Sprite.__init__(self)
        self.rect = None
        self.spriteRect = spriteRect
        self.name = piece_name
        self.team = player
        self.moved = False

    def moveIt(self, x, y):
        if self.checkLegality(x, y):
            self.rect.x, self.rect.y = (x, y)
            return True

    def checkLegality(self, x, y):
        if self.name[0] == "P":
            if self.team.player == 1:
                if y - self.rect.y <= 100 and abs(x - self.rect.x) == 50:
                    for piece in self.team.opponent.pieces:
                        if (piece.rect.x, piece.rect.y) == (x, y):
                            self.moved = True
                            return True
                elif not self.moved:
                    if abs(self.rect.y - y) <= 100 and y - self.rect.y > 0 and self.rect.x - x == 0:
                        for piece in self.team.opponent.pieces:
                            if (piece.rect.x, piece.rect.y) == (x, y):
                                return False
                        self.moved = True
                        return True
                elif abs(self.rect.y - y) == 50 and y - self.rect.y > 0 and self.rect.x - x == 0:
                    for piece in self.team.opponent.pieces:
                        if (piece.rect.x, piece.rect.y) == (x, y):
                            return False
                    return True
            else:
                if self.rect.y - y <= 100 and abs(x - self.rect.x) == 50:
                    for piece in self.team.opponent.pieces:
                        if (piece.rect.x, piece.rect.y) == (x, y):
                            self.moved = True
                            return True
                if not self.moved:
                    if abs(self.rect.y - y) <= 100 and y - self.rect.y < 0 and self.rect.x - x == 0:
                        for piece in self.team.opponent.pieces:
                            if (piece.rect.x, piece.rect.y) == (x, y):
                                return False
                        self.moved = True
                        return True
                elif abs(self.rect.y - y) == 50 and y - self.rect.y < 0 and self.rect.x - x == 0:
                    for piece in self.team.opponent.pieces:
                        if (piece.rect.x, piece.rect.y) == (x, y):
                            return False
                    return True

        elif self.name == "K":
            if abs(self.rect.y - y) <= 50 and abs(x - self.rect.x) <= 50:
                return True

        elif self.name == "Q":
            if (abs(self.rect.x - x) == abs(self.rect.y - y)) or self.rect.x == x or self.rect.y == y:
                return True

        elif self.name[1] == "R":
            if self.rect.x == x or self.rect.y == y:
                return True

        elif self.name[1] == "B":
            if abs(self.rect.x - x) == abs(self.rect.y - y):
                return True

        elif self.name[1] == "K":
            if (abs(self.rect.x - x) == 50 and abs(self.rect.y - y) == 100) or (abs(self.rect.x - x) == 100 and abs(self.rect.y - y) == 50):
                return True

        else:
            return False

class Player:
    def __init__(self, player, piecesSprite, board):
        self.player = player
        self.pieces = pygame.sprite.Group()
        self.pieceSprites = piecesSprite
        self.board = board
        self.opponent = None

    def make_pieces(self):
        if self.player == 1:
            y = 5
        else:
            y = 65
        self.pieces.add(Piece(Rect(217, y, 50, 50), "RR", self))
        self.pieces.add(Piece(Rect(163, y, 50, 50), "RK", self))
        self.pieces.add(Piece(Rect(107, y, 50, 50), "RB", self))
        self.pieces.add(Piece(Rect(5, y, 50, 50), "K", self))
        self.pieces.add(Piece(Rect(57, y, 50, 50), "Q", self))
        self.pieces.add(Piece(Rect(107, y, 50, 50), "LB", self))
        self.pieces.add(Piece(Rect(163, y, 50, 50), "LK", self))
        self.pieces.add(Piece(Rect(217, y, 50, 50), "LR", self))
        for i in range(8):
            self.pieces.add(Piece(Rect(267, y, 50, 50), "P{0}".format(i+1), self))
        if self.player == 1:
            square_index = 0
            for piece in self.pieces:
                square = self.board.squares[square_index]
                piece.rect = Rect(square.x, square.y, 50, 50)
                square_index += 1
        else:
            square_index = 63
            for piece in self.pieces:
                square = self.board.squares[square_index]
                piece.rect = Rect(square.x, square.y, 50, 50)
                square_index -= 1
            for piece in self.pieces:
                if piece.name == "K":
                    Qx, Qy = piece.rect.x, piece.rect.y
                if piece.name == "Q":
                    Kx, Ky = piece.rect.x, piece.rect.y
            for piece in self.pieces:
                if piece.name == "K":
                    piece.rect.x, piece.rect.y = Kx, Ky
                if piece.name == "Q":
                    piece.rect.x, piece.rect.y = Qx, Qy


    def drawPieces(self):
        for piece in self.pieces:
            self.board.window.blit(self.pieceSprites, (piece.rect.x, piece.rect.y), piece.spriteRect)


    def move_piece(self):
        choice = False
        selectedPiece = None
        selectedAPiece = False
        pieceBlocking = False
        while choice == False:
            pieceBlocking = False
            ev = pygame.event.poll()
            if ev.type == KEYDOWN:
                key = ev.dict['key']
                if key == 27:
                    quit()
            if ev.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if selectedAPiece:
                    for square in self.board.squares:
                        if square.collidepoint(x, y):
                            for piece in self.pieces:
                                if (piece.rect.x, piece.rect.y) == (square.x, square.y):
                                    pieceBlocking = True
                            if not pieceBlocking:
                                if self.checkPath(selectedPiece, square):
                                    if selectedPiece.moveIt(square.x, square.y):
                                        self.checkTakePiece(selectedPiece)
                                        choice = True
                for piece in self.pieces:
                    if piece.rect.collidepoint(x, y):
                        selectedPiece = piece
                        selectedAPiece = True

    def checkTakePiece(self, pieceMoved):
        for piece in self.opponent.pieces:
            if (piece.rect.x, piece.rect.y) == (pieceMoved.rect.x, pieceMoved.rect.y):
                piece.kill()

    def checkPath(self, pieceToMove, destinationSquare):
        if pieceToMove.name == "K":
            return True
        if pieceToMove.name == "Q":
            if destinationSquare.x == pieceToMove.rect.x:
                diff = abs(pieceToMove.rect.y - destinationSquare.y)
                diff = diff // 50
                for i in range(1, diff):
                    add = i * 50
                    if pieceToMove.rect.y < destinationSquare.y:
                        for piece in self.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y + add)):
                                return False
                    if pieceToMove.rect.y > destinationSquare.y:
                        for piece in self.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y - add)):
                                return False
            elif destinationSquare.y == pieceToMove.rect.y:
                diff = abs(pieceToMove.rect.x - destinationSquare.x)
                diff = diff // 50
                for i in range(1, diff):
                    add = i * 50
                    if pieceToMove.rect.x < destinationSquare.x:
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x + add)):
                                return False
                    if pieceToMove.rect.x > destinationSquare.x:
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x - add)):
                                return False
            elif destinationSquare.x > pieceToMove.rect.x:
                diff = abs(pieceToMove.rect.x - destinationSquare.x)
                diff = diff // 50
                if destinationSquare.y > pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x + add)):
                                return False
                if destinationSquare.y < pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x + add)):
                                return False
            elif destinationSquare.x < pieceToMove.rect.x:
                diff = abs(pieceToMove.rect.x - destinationSquare.x)
                diff = diff // 50
                if destinationSquare.y > pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x - add)):
                                return False
                if destinationSquare.y < pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x - add)):
                                return False

        elif pieceToMove.name[0] == "P" or pieceToMove.name[1] == "R":
            if destinationSquare.x == pieceToMove.rect.x:
                diff = abs(pieceToMove.rect.y - destinationSquare.y)
                diff = diff // 50
                for i in range(1, diff):
                    add = i * 50
                    if pieceToMove.rect.y < destinationSquare.y:
                        for piece in self.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y + add)):
                                return False
                    if pieceToMove.rect.y > destinationSquare.y:
                        for piece in self.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.x, piece.rect.y) == (pieceToMove.rect.x, (pieceToMove.rect.y - add)):
                                return False
            elif destinationSquare.y == pieceToMove.rect.y:
                diff = abs(pieceToMove.rect.x - destinationSquare.x)
                diff = diff // 50
                for i in range(1, diff):
                    add = i * 50
                    if pieceToMove.rect.x < destinationSquare.x:
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x + add)):
                                return False
                    if pieceToMove.rect.x > destinationSquare.x:
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == (pieceToMove.rect.y, (pieceToMove.rect.x - add)):
                                return False

        elif pieceToMove.name[1] == "B":
            if destinationSquare.x > pieceToMove.rect.x:
                diff = abs(pieceToMove.rect.x - destinationSquare.x)
                diff = diff // 50
                if destinationSquare.y > pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x + add)):
                                return False
                if destinationSquare.y < pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x + add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x + add)):
                                return False
            elif destinationSquare.x < pieceToMove.rect.x:
                diff = abs(pieceToMove.rect.x - destinationSquare.x)
                diff = diff // 50
                if destinationSquare.y > pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y + add), (pieceToMove.rect.x - add)):
                                return False
                if destinationSquare.y < pieceToMove.rect.y:
                    for i in range(1, diff):
                        add = i * 50
                        for piece in self.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x - add)):
                                return False
                        for piece in self.opponent.pieces:
                            if (piece.rect.y, piece.rect.x) == ((pieceToMove.rect.y - add), (pieceToMove.rect.x - add)):
                                return False

        return True

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
        theGame.player2.move_piece()
        theGame.drawMatch()
        if ev.type == KEYDOWN:
            key = ev.dict['key']
            if key == 27:
                quit()
        timeKeeper.tick(60)
    pygame.quit()

main()
