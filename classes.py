import pygame
from pygame.math import Vector2


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
        self.current_angle = 0
        # self.mask = pygame.mask.from_surface(self.image)

    def death(self, death_image):
        rotated = pygame.transform.rotate(death_image, self.current_angle)
        self.image = rotated
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.orbit = False

    def update(self):
        if self.orbit:
            self.orbit.update()
            new_pos = self.orbit.get_position()
            self.vector = Vector2(new_pos)
            self.rect.center = new_pos

            if self.orbit.tidal_lock:
                facing_angle = self.orbit.get_tidal_lock_angle()
                self.current_angle = facing_angle
                self.image = pygame.transform.rotate(self.original_image, facing_angle)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pygame.mask.from_surface(self.image)
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
        self.remaining = False
        self.surface = surface
        self.last_move_direction = Vector2(1, 0)
        self.impact_angle = 0
        self.push_velocity = Vector2(0, 0)
        self.impact_remain_sprite = None
        self.impacted_group = None
        self.asteroid_group = None

        Asteroid.all_asteroids.append(self)

    def move(self, speed, target):
        if self.keep_moving:
            movement = target - self.pos
            if movement.length() > 0:
                self.last_move_direction = movement.normalize()
                self.pos += self.last_move_direction * speed
            self.rect.center = self.pos

    def impact_remain(
        self,
        impact_remain_sprite,
        asteroids_group,
        impacted_group,
        push_distance=10,
        push_target=None,
    ):
        self.impact_remain_sprite = impact_remain_sprite
        self.impacted_group = impacted_group
        self.asteroid_group = asteroids_group
        self.asteroid_group.remove(self)
        self.impacted_group.add(self)
        self.remaining = True
        self.keep_moving = 0
        self.mask = pygame.mask.from_surface(impact_remain_sprite)

        if push_target is not None:
            direction = push_target - self.pos
            if direction.length() != 0:
                self.push_velocity = direction.normalize() * push_distance
                self.last_move_direction = self.push_velocity.normalize()

    def impact(self):
        self.keep_moving = 0
        if not self.playing_death_anim:
            direction = Vector2(self.last_move_direction)
            if direction.length() == 0 and self.push_velocity.length() > 0:
                direction = self.push_velocity.normalize()
            if direction.length() != 0:
                # Rotate so the bottom of the animation faces the movement direction
                self.impact_angle = -direction.angle_to(Vector2(0, -1))
            else:
                self.impact_angle = 0

            self.death_anim.reset()
            self.death_anim.pos = self.pos
            self.playing_death_anim = True

    def update(self, dt):
        # Apply push movement with friction
        if self.push_velocity.length() > 0.1:
            self.pos += self.push_velocity
            self.rect.center = self.pos
            self.push_velocity *= 0.99
            if self.push_velocity.length() > 0:
                self.last_move_direction = self.push_velocity.normalize()
        else:
            self.push_velocity = Vector2(0, 0)

        # Play death animation with correct rotation
        if self.playing_death_anim:
            self.death_anim.update(dt)
            frame = self.death_anim.get_current_frame()
            rotated_frame = pygame.transform.rotate(frame, self.impact_angle)
            rect = rotated_frame.get_rect(center=self.death_anim.pos)
            self.surface.blit(rotated_frame, rect)
            if self.death_anim.finished:
                self.playing_death_anim = False
                self.kill()
        elif self.remaining:
            remain_rect = self.impact_remain_sprite.get_rect(center=self.pos)
            self.surface.blit(self.impact_remain_sprite, remain_rect)
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
