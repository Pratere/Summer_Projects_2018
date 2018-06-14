import pygame
from pygame.locals import *

pygame.init()
time = pygame.time.Clock()
# mario = pygame.image.load("Mario.png")
chessPieces = pygame.image.load("C:/Users/pratere/github/python/Summer_Projects_2018/ChessSprites.png")
rook = pygame.image.load("C:/Users/pratere/github/python/Summer_Projects_2018/WhiteRook.png")
rook = pygame.transform.scale(rook, (80, 80))
chessPieces = pygame.transform.scale(chessPieces, (320, 120))
screenrect = Rect(0, 0, 500, 500)  # Size of screen.
winstyle = 0  # |FULLSCREEN
bestdepth = pygame.display.mode_ok(screenrect.size, winstyle, 32)
main_surface = pygame.display.set_mode(screenrect.size, winstyle, bestdepth)
mario_rect = Rect(217, 65, 50, 50)
rook_rect = Rect(20, 20, 50, 50)
main_surface.blit(chessPieces, (0, 0), mario_rect)
frame = 0
while True:
    count = 0
    frame += 1
    ev = pygame.event.poll()
    if ev.type == KEYDOWN:
        key = ev.dict['key']
        if key == 27:
            quit()

    main_surface.fill((200, 0, 0), screenrect)
    main_surface.blit(chessPieces, (0, 0), mario_rect)
    main_surface.blit(rook, (50, 0), rook_rect)
    pygame.display.flip()
    time.tick(60)
