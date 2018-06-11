from "C:/Users/pratere/github/python/Summer_Projects_2018/Chess.py" import *

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

    def drawBoard(self):
        self.window.blit(self.player1.pieceSprites)
        pygame.display.flip()

def main():
    pygame.init()
    window_size = 100

    window = pygame.display.set_mode((window_size, window_size))
    thePiecesSprites = pygame.image.load("C:/Users/pratere/github/python/Summer_Projects_2018/ChessSprites.png")

    theGame = ChessGame(window, thePiecesSprites)

    theGame.drawBoard()

    pygame.quit()

main()
