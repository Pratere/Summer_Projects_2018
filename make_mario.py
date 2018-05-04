import pygame
from pygame.locals import *


class Mario(pygame.sprite.Sprite):
    def __int__(self, image_sheet, position=(25, 25), controls=(276, 275, 273, 274), heading=0, speed=2):
        pygame.sprite.Sprite.__init__(self)
        self.pos = position
        self.controls = controls
        self. heading = heading
        self.speed = speed
        self.rect = Rect(self.pos, 20, 20)
        self.img = image_sheet
        self.ev = pygame.event.poll()
        self.mario_rect = Rect(112, 68, 20, 40)

    def update(self, key):
        if self.ev.type == pygame.KEYDOWN:
            if key == 275:
                speed = self.speed

            elif key == 276:
                speed = -self.speed

            elif key == 273:
                vertical_speed = 5

        if self.ev.type == pygame.KEYUP:
            speed = 0
            vertical_speed = 0

        self.rect.x += speed
        self.rect.y += vertical_speed

    def draw(self, surface):
        surface.blit(self.img, self.rect, self.mario_rect)


def main():
    pygame.init()
    time = pygame.time.Clock()
    mario = pygame.image.load("Mario.png")
    screenrect = Rect(0, 0, 1000, 800)  # Size of screen.
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(screenrect.size, winstyle, 32)
    main_surface = pygame.display.set_mode(screenrect.size, winstyle, bestdepth)
    myrio = Mario(mario)

    pygame.display.flip()
    while True:
        count = 0
        ev = pygame.event.poll()
        main_surface.fill((100, 200, 50))
        myrio.draw(main_surface)
        if ev.type == KEYDOWN:
            key = ev.dict['key']
            if key == 27:
                quit()
        pygame.display.flip()
        time.tick(60)

main()