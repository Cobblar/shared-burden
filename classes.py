import pygame
from pygame.math import Vector2
from images import asteroid_hit_img


class Box:
    # keeps a list of all boxes
    all_boxes = []

    def __init__(self, name, color, x, y, size):
        self.name = name
        self.color = color
        self.position = 0
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        Box.all_boxes.append(self)  # adds each box to all_boxes

    def move_y(self, amount):
        self.y += amount
        self.rect.y = self.y

    @classmethod
    def create_box(cls, name, color, x, y, size):
        return cls(name, color, x, y, size)


class Terraformer(pygame.sprite.Sprite):
    def __init__(self, image, name, x, y, orbiting_behavior=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.name = name
        self.vector = Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.orbit = orbiting_behavior
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.orbit:
            self.orbit.update()
            new_pos = self.orbit.get_position()
            self.vector = Vector2(new_pos)
            self.rect.center = new_pos
        else:
            # If no orbit, update self.vector some other way
            self.rect.center = self.vector


class Planet(pygame.sprite.Sprite):
    all_planets = []

    def __init__(self, image, name, x, y, orbiting_behavior=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.name = name
        self.vector = Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.orbit = orbiting_behavior
        Planet.all_planets.append(self)

    def update(self):
        if self.orbit:
            self.orbit.update()
            new_pos = self.orbit.get_position()
            self.vector = Vector2(new_pos)
            self.rect.center = new_pos
        else:
            # If no orbit, update self.vector some other way
            self.rect.center = self.vector

    def darken(self):  # call for when taking damage
        self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)


class Asteroid(pygame.sprite.Sprite):
    all_asteroids = []
    death_timer = 0
    keep_moving = 1

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.pos = Vector2(x, y)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        Asteroid.all_asteroids.append(self)

    def move(self, speed, target):
        self.speed = speed
        self.target = target

        self.movement = self.target - self.pos

        # avoids normalizing zero vector
        if self.movement.length() > 0:
            if Asteroid.keep_moving == 1:
                self.pos += self.movement.normalize() * self.speed

        self.rect.center = self.pos

    def impact(self):
        self.image = asteroid_hit_img
        Asteroid.death_timer += 0.1
        Asteroid.keep_moving = 0
        # if Asteroid.death_timer == 10:
        #    Asteroid.all_asteroids.remove(self)
