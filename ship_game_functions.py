import pygame
from pygame.locals import *
from pygame import transform


class Ship(pygame.sprite.Sprite):
    """
    Ship class inherits from the pygame.sprite.Sprite. class, this class is controlled by set keys.
    """
    def __init__(self, image, explosion, start_pos=(25, 25), controls=(276, 275, 273, 274), heading=0, velocity=0.1, clr=(255, 255, 255), text="", trail=False):
        """
        Initializes an instance of the Ship class.
        :param image: The image shown on the screen for the ship.
        :param start_pos: Starting position of the ship.
        :param controls: Set of key numbers corresponding to the keys that control each ship.
        :param explosion: The sprite sheet that will be used to create the explosion animation.
        :param heading: The direction the ship faces.
        :param velocity: The speed of the ship.
        :param clr: The color of the ship.
        :param text: Used to tell ships apart for adding score and printing win screen.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = transform.rotate(image, heading)
        self.start_pos = start_pos  # This is so ship can be reset to starting position for next match
        self.x, self.y = start_pos  # This is so image position can be updated
        self.controls = controls
        self.explosion = explosion
        self.heading = heading
        self.start_heading = heading  # So ship can be reset to original heading
        self.vel = velocity
        self.image = transform.rotate(image, heading)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_pos
        self.color = clr
        if trail == True:
            if self.heading == 180 or self.heading == 0:  # These if statements set the image position based on the heading.
                self.y = self.rect.y - self.rect.height/2 - self.rect.width/2
            elif self.heading == 90 or self.heading == 270:
                self.x = self.rect.x - self.rect.width/2 - self.rect.height/2
            if self.heading == 0:  # Creates the starting trail that will follow the ship in the correct position.
                self.trail = Trail((self.rect.x, self.rect.y), self.heading, self.color)
            elif self.heading == 180:
                self.trail = Trail((self.rect.x + self.rect.width, self.rect.y), self.heading, self.color)
            elif self.heading == 90:
                self.trail = Trail((self.rect.x, self.rect.y + self.rect.height), self.heading, self.color)
            elif self.heading == 270:
                self.trail = Trail((self.rect.x, self.rect.y), self.heading, self.color)
        self.col = False  # A attribute that describes if the ship has collided with anything.
        self.old_trail = 0  # A starting value that is just a place holder.
        self.expo_rect = Rect(0, 0, 52, 40)  # The size and starting location of the first square on the explosion sprite sheet.
        self.score = 0  # Holds the score of the ship.
        self.text = text  # Holds the number of the ship.
        self.played = False
        self.expo_sound = pygame.mixer.music
        self.expo_sound.load("8 Bit Explosion.mp3")  # Sound for explosion

    def update(self, key, trails):
        """
        Updates the location and image of the Ship() off the velocity and any keys input by user.
        :param key: A value that corresponds to a key being pressed.
        :param trails: A pygame.sprite.Group().
        :return: None
        """
        if not self.col:  # Tests to see if the ship has collided with something.
            (x, y) = self.rect.x, self.rect.y  # Creates variables that can be updated without effecting rect position.

            if self.trail is not self.old_trail:  # Tests to see if the ship has a different trail than before.
                trails.add(self.trail)
                self.old_trail = self.trail

            (L, R, U, D) = self.controls  # Sets the keys that control the ship.

            if key == L:  # Checks to see if the left turn key has been pressed.
                if self.heading != 0:  # Makes sure you are not turning around and immediately killing yourself on accident.
                    if self.heading == 90:
                        x, y = x - self.rect.height + self.rect.width/2 + 1, y + self.rect.height - self.rect.width/2  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    if self.heading == 270:
                        x, y = x - self.rect.height + self.rect.width/2 + 1, y - self.rect.width/2  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    new_heading = 180
                    self.trail = Trail((x + 30, y), new_heading, self.color)  # Creates a new trail to be used until turned again.
                else:
                    new_heading = self.heading  # If ship tried to turn back on its self then the new_heading is the same as the old.

            elif key == R:
                if self.heading != 180:  # Makes sure you are not turning around and immediately killing yourself on accident.
                    new_heading = 0
                    if self.heading == 90:
                        x, y = x + (self.rect.width/2) + 1, y + self.rect.height  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    if self.heading == 270:
                        x, y = x + (self.rect.width/2) - 1, y - self.rect.width/2  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    self.trail = Trail((x, y), new_heading, self.color)  # Creates a new trail to be used until turned again.
                else:
                    new_heading = self.heading  # If ship tried to turn back on its self then the new_heading is the same as the old.

            elif key == U:
                if self.heading != 270:  # Makes sure you are not turning around and immediately killing yourself on accident.
                    if self.heading == 0:
                        x, y = x + self.rect.height/2 - 1, y - self.rect.width + self.rect.height/2 + 1  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    if self.heading == 180:
                        x, y = x + self.rect.width, y - self.rect.width  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    new_heading = 90
                    self.trail = Trail((x, y + 30), new_heading, self.color)  # Creates a new trail to be used until turned again.
                else:
                    new_heading = self.heading  # If ship tried to turn back on its self then the new_heading is the same as the old.

            elif key == D:
                if self.heading != 90:  # Makes sure you are not turning around and immediately killing yourself on accident.
                    if self.heading == 0:
                        x, y = x - self.rect.height/2, y + self.rect.height/2 - 1  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    if self.heading == 180:
                        x, y = x + self.rect.width, y + 1  # Moves the rectangle into the correct position to turn and not collide with the trail it has just made.
                    new_heading = 270
                    self.trail = Trail((x, y), new_heading, self.color)  # Creates a new trail to be used until turned again.
                else:
                    new_heading = self.heading  # If ship tried to turn back on its self then the new_heading is the same as the old.

            else:
                new_heading = self.heading  # If ship did not turn then the new_heading is the same as the old.

            angle = new_heading - self.heading  # Calculates the angle that the ship has turned.
            self.image = transform.rotate(self.image, angle)  # Rotates the image of the ship to face the new direction.
            self.heading = new_heading  # Updates the ships heading.

            if self.heading == 0:
                x += self.vel  # Moves the ship right.
                self.rect.width = 20  # Makes ships rect the appropriate dimensions.
                self.rect.height = 2

            elif self.heading == 90:
                y -= self.vel  # Moves the ship down.
                self.rect.width = 2  # Makes ships rect the appropriate dimensions.
                self.rect.height = 20

            elif self.heading == 180:
                x -= self.vel  # Moves the ship left.
                self.rect.width = 20  # Makes ships rect the appropriate dimensions.
                self.rect.height = 2

            elif self.heading == 270:
                y += self.vel  # Moves the ship up.
                self.rect.width = 2  # Makes ships rect the appropriate dimensions.
                self.rect.height = 20

            self.rect.x, self.rect.y = x, y  # Updates rect's position.

            if self.heading == 180 or self.heading == 0:  # Positions the ships image relative to the ships rect.
                self.y = self.rect.y - 14
                if self.heading == 0:
                    self.x = self.rect.x
                else:
                    self.x = self.rect.x - 10

            if self.heading == 90 or self.heading == 270:  # Positions the ships image relative to the ships rect.
                self.x = self.rect.x - 14
                if self.heading == 90:
                    self.y = self.rect.y - 10
                else:
                    self.y = self.rect.y

            if self.heading == 180:  # If the ship is heading left then the position of the rect and the width are updated so that the top left point which the position of the rect is based on moves with the ship.
                self.trail.update(self.rect.x + self.rect.width, self.rect.y)

            if self.heading == 90:  # If the ship is heading up then the position of the rect and the width are updated so that the top left point which the position of the rect is based on moves with the ship.
                self.trail.update(self.rect.x, self.rect.y + self.rect.height)

            else:  # Updates the trails width and height.
                self.trail.update(self.rect.x, self.rect.y)

    def draw(self, target, frame):
        """
        Draws the ship on to the pygame surface.
        :param target: Surface on which to blit the images.
        :param frame: The number of frames that the game is on.
        :return: None
        """
        if self.col:  # If the ship has collided with something the explosion animation plays.
            if self.heading == 270:  # These if statements just move the explosions position to be ontop of where the ship explodes.
                target.blit(self.explosion, (self.x - 15, self.y - 10), self.expo_rect)
            elif self.heading == 0 or self.heading == 180:
                target.blit(self.explosion, (self.x - 15, self.y - 6), self.expo_rect)
            else:
                target.blit(self.explosion, (self.x - 15, self.y), self.expo_rect)
            if not self.played:
                self.expo_sound.play(0)
                self.played = True
            if frame % 5 == 0:  # Update the explosion every 5 frames so it doesnt go to fast.
                self.expo_rect.x += 58.5
                if self.expo_rect.x > 300:
                    self.expo_rect.x = 0
                    self.expo_rect.y += 38
                if self.expo_rect.y > (38 * 6):  # If at the end of the explosion, kill the ship.
                    for group in self.groups():
                        group.remove(self)
        else:  # Otherwise just puts the ship on the surface.
            target.blit(self.image, (self.x, self.y))


class Trail(pygame.sprite.Sprite):
    """
    Trail class inherits from pygame.sprite.Sprite. This class follows and updates behind an instance of a ship to trace their path and make it able to collide with ships.
    """
    def __init__(self, pos, heading=0, clr=(255, 255, 255)):
        """
        Initializes an instance of the Trail Class.
        :param pos: The postion to create the trail at.
        :param heading: The direction in which the trail will update.
        :param clr: The color of the Trail.
        """
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.x, self.y = self.pos
        self.height = 2
        self.width = 2
        self.heading = heading
        self.rect = Rect(self.x, self.y, self.width, self.height)  # Creates the hit box of the trail.
        self.color = clr

    def update(self, x_curr, y_curr):
        """
        Updates the length and position of the Trail to connect with the tail end of the ship.
        :param x_curr: Current x position of ship.
        :param y_curr: Current y position of ship.
        :return: None
        """
        (x, y) = self.pos

        if self.heading == 0 or self.heading == 180:  # updates the width of the rectangle to the distance between the original position of the trail and the new position of the ship if the ship is moving in the x direction.
            width = abs(x - x_curr)
            self.rect.width = width

        else:
            width = 2

        if self.heading == 90 or self.heading == 270:  # updates the height of the rectangle to the distance between the original position of the trail and the new position of the ship if the ship is moving in the y direction.
            height = abs(y - y_curr)
            self.rect.height = height

        else:
            height = 2

        if self.heading == 180:  # If the ship is moving left the defining point of the trails rectangle needs to be moved.
            x = x_curr + 20
            width -= 30

        if self.heading == 90:  # If the ship is moving up the defining point of the trails rectangle needs to be moved.
            y = y_curr
            height -= 10

        self.rect = Rect(x, y, width, height)  # Updates the ships rectangle.

    def draw(self, target):
        """
        Draws the ship to the surface.
        :param target: Surface to be draw to.
        :return: None
        """
        target.fill(self.color, self.rect)


class Border(pygame.sprite.Sprite):
    """
    Basic class that only needs to be class so it can inherit from pygame.sprite.Sprite so other sprites can collide with them.
    """
    def __init__(self, x, y, w, h):
        """
        Initializes a Border object which is basically just a Rect but needs to be a pygame.sprite.Sprite() to be checked for collision.
        :param x: x position.
        :param y: y position.
        :param w: width.
        :param h: height.
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, w, h)


class Button:
    """
    A clickable button.
    """
    def __init__(self, text, position, size, offset, clr=(230, 230, 230), txt_clr=(0, 0, 0)):
        """
        Initializes a button object.
        :param text: Text to be shown on button.
        :param position: position of the button.
        :param size: size of the button (width, height).
        :param offset: tuple to center the button.
        """
        font = pygame.font.SysFont('Wide Latin', 16)
        self.text = font.render(text, True, txt_clr)
        self.pos = position
        self.rect = Rect(self.pos, size)
        self.off = offset
        self.clr = clr

    def draw(self, target):
        """
        Draws the button on the surface.
        :param target: Surface to draw the button on.
        :return: None
        """
        x, y = self.pos
        dx, dy = self.off
        target.fill(self.clr, self.rect)
        target.blit(self.text, (x + dx, y + dy))
