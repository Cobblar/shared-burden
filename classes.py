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
        self.original_y = 0
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.one_notch_cd = False
        Box.all_boxes.append(self)  # adds each box to all_boxes

    def update(self):
        if self.one_notch_cd:
            print("test2")
            print(self.y)
            if self.y >= self.original_y:
                self.one_notch_cd = False
                self.position -= 1
            else:
                self.y += 0.5
                self.rect.y = self.y

    def move_y(self, amount):
        self.y += amount
        self.rect.y = self.y

    def one_notch_cd_method(self):
        self.original_y = self.y
        self.one_notch_cd = True
        print("test1")

    @classmethod
    def create_box(cls, name, color, x, y, size):
        return cls(name, color, x, y, size)


class Selector:
    def __init__(self, border, surface):
        self.border = border
        self.surface = surface
        self.color = (216, 222, 233)
        self.width = 36
        self.height = 36

    def update(self, x, y):
        self.x = x
        self.y = y
        pygame.draw.rect(
            self.surface,
            self.color,
            (self.x - self.border, self.y - self.border, self.width, self.height),
            width=self.border,
        )


class Terraformer(pygame.sprite.Sprite):
    def __init__(self, image, name, x, y, orbiting_behavior=None):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
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

            if self.orbit.tidal_lock:
                facing_angle = self.orbit.get_tidal_lock_angle()
                self.image = pygame.transform.rotate(self.original_image, facing_angle)
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # If no orbit, update self.vector some other way
            self.rect.center = self.vector


class Planet(pygame.sprite.Sprite):
    all_planets = []

    def __init__(self, image, name, x, y, orbiting_behavior=None):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.image = image
        self.name = name
        self.vector = Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.orbit = orbiting_behavior
        self.damage_level = 0
        Planet.all_planets.append(self)

    def update(self):
        if self.orbit:
            self.orbit.update()
            new_pos = self.orbit.get_position()
            self.vector = Vector2(new_pos)
            self.rect.center = new_pos

            if self.orbit.tidal_lock:
                facing_angle = self.orbit.get_tidal_lock_angle()
                self.image = pygame.transform.rotate(self.original_image, facing_angle)
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # If no orbit, update self.vector some other way
            self.rect.center = self.vector

    def damage(self):
        self.damage_level += 1
        print(self.damage_level)
        # Always start from the original image, so repeated hits can add up
        if self.damage_level == 2:
            self.image.fill((255, 0, 0, 254), special_flags=pygame.BLEND_RGBA_MULT)
            self.damage_level = 0


class Asteroid(pygame.sprite.Sprite):
    all_asteroids = []

    def __init__(self, x, y, image, scale, death_anim, surface):
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector2(x, y)
        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)
        self.keep_moving = 1
        self.death_anim = death_anim
        self.playing_death_anim = False
        self.surface = surface
        Asteroid.all_asteroids.append(self)

    def move(self, speed, target):
        if self.keep_moving:
            movement = target - self.pos
            if movement.length() > 0:
                self.pos += movement.normalize() * speed
            self.rect.center = self.pos

    def impact(self):
        self.keep_moving = 0
        if not self.playing_death_anim:
            self.death_anim.reset()
            self.death_anim.pos = self.pos
            self.playing_death_anim = True

    def update(self, dt):
        if self.playing_death_anim:
            self.death_anim.update(dt)
            self.surface.blit(self.death_anim.get_current_frame(), self.death_anim.pos)
            if self.death_anim.finished:
                self.playing_death_anim = False
                self.kill()
        else:
            self.surface.blit(self.image, self.rect)

    def draw(self):
        if not self.playing_death_anim:
            self.surface.blit(self.image, self.rect)


class ShieldEffect:
    def __init__(self, anim, sfx_library):
        self.anim = anim
        self.sfx_library = sfx_library
        self.playing = False
        self._prev_pos = None

    def check_collision(self, other_sprite):
        """Returns True if this shield's mask collides with another sprite's mask"""
        offset = (
            other_sprite.rect.left - self.anim.rect.left,
            other_sprite.rect.top - self.anim.rect.top,
        )
        return self.anim.mask.overlap(other_sprite.mask, offset) is not None

    def trigger(self):
        """Start the animation and sound if not already playing"""
        if not self.playing:
            self.anim.reset()
            self.sfx_library["shield"].play()
            self.playing = True

    def update_and_draw(self, dt, surface, green_box, mars):
        """Update the animation and draw it if active."""
        pos = green_box.position

        # Only trigger if it toggles to 1 from something else
        if pos == 1 and self._prev_pos != 1:
            self.trigger()

        self._prev_pos = pos

        if self.playing:
            self.anim.pos = mars.rect.center
            self.anim.update(dt)
            frame = self.anim.get_current_frame()
            frame_rect = frame.get_rect(center=mars.rect.center)
            surface.blit(frame, frame_rect)

            if self.anim.is_done():
                self.playing = False
