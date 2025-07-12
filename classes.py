import pygame
import math
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
        self.activate = False
        Box.all_boxes.append(self)  # adds each box to all_boxes

    def update(self):
        if self.one_notch_cd:
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

    @classmethod
    def create_box(cls, name, color, x, y, size):
        return cls(name, color, x, y, size)


class Selector:
    def __init__(self, border, surface):
        self.border = border
        self.surface = surface
        self.color = (216, 222, 233)
        self.width = 66
        self.height = 66

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


class Moon(Planet):
    def update(self, yellow_box):
        super().update()
        if yellow_box.position == 1:
            self.orbit.orbit_speed = 0.5
        elif yellow_box.position == 2:
            self.orbit.orbit_speed = 2
        elif yellow_box.position == 0:
            self.orbit.orbit_speed = 0
        elif yellow_box.position == -1:
            self.orbit.orbit_speed = -0.5
        elif yellow_box.position == -2:
            self.orbit.orbit_speed = -2


class Asteroid(pygame.sprite.Sprite):
    all_asteroids = []

    def __init__(self, x, y, image, scale, death_anim, surface, sfx):
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
        self.sfx_library = sfx

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
        # self.sfx_library["asteroid_impact"].play()
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


class LaserEffect:
    def __init__(self, anim, sfx_library):
        self.anim = anim
        self.sfx_library = sfx_library
        self.playing = False
        self.rect = pygame.Rect(0, 0, 0, 0)  # Initialize self.rect
        self.mask = None  # Initialize self.mask

    def trigger(self):
        if not self.playing:
            self.anim.reset()
            self.sfx_library["laser"].play()
            self.playing = True

    def update_and_draw(self, dt, surface, yellow_box, moon, mars):
        if yellow_box.activate:
            self.trigger()
            yellow_box.activate = False

        if self.playing:
            moon_center = Vector2(moon.rect.center)
            mars_center = Vector2(mars.rect.center)

            direction_vector = mars_center - moon_center

            moon_radius = moon.rect.width / 2
            mars_radius = mars.rect.width / 2

            laser_start_pos = moon_center + direction_vector.normalize() * moon_radius
            laser_end_pos = mars_center - direction_vector.normalize() * mars_radius

            visible_laser_vector = laser_end_pos - laser_start_pos
            actual_laser_length = visible_laser_vector.length()

            if actual_laser_length == 0:
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.mask = None  # Clear mask if laser isn't drawn
                return

            angle = visible_laser_vector.angle_to(Vector2(0, -1))

            self.anim.update(dt)
            original_frame = self.anim.get_current_frame()

            scale_factor_h = actual_laser_length / original_frame.get_height()

            scaled_frame = pygame.transform.scale(
                original_frame,
                (
                    original_frame.get_width(),
                    int(original_frame.get_height() * scale_factor_h),
                ),
            )

            rotated_frame = pygame.transform.rotate(scaled_frame, angle)

            base_offset_from_scaled_center = Vector2(0, scaled_frame.get_height() / 2)
            rotated_base_offset = base_offset_from_scaled_center.rotate(-angle)

            target_rotated_center = laser_start_pos - rotated_base_offset

            # --- CRITICAL ADDITIONS FOR MASK COLLISION ---
            self.rect = rotated_frame.get_rect(center=target_rotated_center)
            self.mask = pygame.mask.from_surface(
                rotated_frame
            )  # Create mask from the current rotated frame
            # --- END CRITICAL ADDITIONS ---

            surface.blit(rotated_frame, self.rect)

            # Debug: Draw red circle at laser start (on moon's surface)
            pygame.draw.circle(
                surface,
                (255, 0, 0),
                (int(laser_start_pos.x), int(laser_start_pos.y)),
                5,
            )

            if self.anim.is_done():
                self.playing = False
                # Clear the rect when not playing
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.mask = None  # Clear mask when not playing
