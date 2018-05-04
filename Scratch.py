import pygame
from pygame.locals import *

pygame.init()
time = pygame.time.Clock()
mario = pygame.image.load("Mario.png")
screenrect = Rect(0, 0, 1000, 800)  # Size of screen.
winstyle = 0  # |FULLSCREEN
bestdepth = pygame.display.mode_ok(screenrect.size, winstyle, 32)
main_surface = pygame.display.set_mode(screenrect.size, winstyle, bestdepth)
mario_rect = Rect(112, 68, 20, 40)
main_surface.blit(mario, (0, 0), mario_rect)
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
    if frame % 5 == 0:
        mario_rect.x += 20
        if mario_rect.x > 270:
            mario_rect.x = 112
    main_surface.blit(mario, (0, 0), mario_rect)
    pygame.display.flip()
    time.tick(60)