import pygame
import random


from sound import load_sound_effects, other_sounds, play_sound_once
from images import (
    shield_anim_frames,
    shield_anim_mask,
    SpriteAnimation,
    asteroid_poof_frames,
)
from constants import CRT_SURFACE_HEIGHT, CRT_SURFACE_WIDTH
from images import (
    mars_img,
    # sun_img,
    moon_img,
    asteroid_img,
    terraformer_img,
)
from orbit import OrbitingBehavior  # <--- Import the OrbitingObject class
from classes import Planet, Asteroid, Terraformer, ShieldEffect

# create the surface
crt_surface = pygame.Surface((CRT_SURFACE_WIDTH, CRT_SURFACE_HEIGHT), pygame.SRCALPHA)
"""
--------------INSTANCES OF CLASSES-------------
"""

mars = Planet(
    mars_img,
    "mars",
    (CRT_SURFACE_WIDTH / 2),
    (CRT_SURFACE_HEIGHT / 2),
    orbiting_behavior=None,
)


moon_orbit_radius = 300
moon_orbit_speed = 1
moon_orbiting_mars = OrbitingBehavior(
    central_pos=mars.rect.center,
    orbit_radius=moon_orbit_radius,
    orbit_speed=moon_orbit_speed,
    initial_angle=0.0,
    tidal_lock=False,
    tidal_lock_offset=0,
)

moon = Planet(moon_img, "moon", 0, 0, orbiting_behavior=moon_orbiting_mars)

terraformer_orbit_radius = 130
terraformer_orbit_speed = 0.1
terraformer_orbiting_mars = OrbitingBehavior(
    central_pos=mars.rect.center,
    orbit_radius=terraformer_orbit_radius,
    orbit_speed=terraformer_orbit_speed,
    initial_angle=27,
    tidal_lock=True,
    tidal_lock_offset=270,
)

terraformer1 = Terraformer(
    terraformer_img, "terraformer1", 0, 0, orbiting_behavior=terraformer_orbiting_mars
)
"""
--------------OTHER VARIABLES-------------
"""
# load sounds
sfx = load_sound_effects()

# events
SPAWN_ASTEROID = pygame.USEREVENT + 1

# timers
pygame.time.set_timer(SPAWN_ASTEROID, 2000)

ast_rand_spawn_x = 0
ast_rand_spawn_y = 0

# animations
shield_pos = mars.rect.center
shield_anim = SpriteAnimation(
    shield_pos, shield_anim_frames, fps=15, masks=shield_anim_mask, loop=False
)
shield = ShieldEffect(shield_anim, sfx)

asteroid_poof_pos = (0, 0)
astroid_poof_anim = SpriteAnimation(
    asteroid_poof_pos, asteroid_poof_frames, fps=15, masks=shield_anim_mask, loop=False
)
# groups
mars_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
shield_group = pygame.sprite.Group()
# add to the groups
mars_group.add(mars)
shield_group.add(shield_anim)


"""
--------------FUNCTIONS-------------
"""


# what gets called in main
def crt(surface, yellow_box, green_box, Box, dt, sfx):
    # create background color
    crt_surface.fill((0, 0, 0, 255))
    # draw stuff onto the crt (central image)
    mars.update()
    crt_surface.blit(mars.image, mars.rect)
    moon.update()
    crt_surface.blit(moon.image, moon.rect)
    terraformer1.update()
    crt_surface.blit(terraformer1.image, terraformer1.rect)
    shield.update_and_draw(dt, crt_surface, green_box, mars)
    # bases moon orbiting speed on position of yellow box
    # moon_orbiting_mars.orbit_speed = yellow_box.position * 2.5

    # plays the sheild animation
    # play_shield(dt, green_box, sfx, shield_anim_playing=False)

    for asteroid in asteroid_group:
        asteroid.move(1, mars.vector)
        # crt_surface.blit(asteroid.image, asteroid.rect)
        asteroid.update(dt)

        if pygame.sprite.spritecollide(asteroid, mars_group, False):
            if pygame.sprite.spritecollide(
                asteroid, mars_group, False, pygame.sprite.collide_mask
            ):
                mars.damage()
                asteroid.impact()
        if pygame.sprite.spritecollide(asteroid, shield_group, False):
            if pygame.sprite.spritecollide(
                asteroid, shield_group, False, pygame.sprite.collide_mask
            ):
                asteroid.impact()
    # draw the crt onto the main game surface
    surface.blit(crt_surface, (0, 0))


def create_asteroid(x, y):
    asteroid_poof_anim = SpriteAnimation(
        (x, y), asteroid_poof_frames, fps=15, masks=shield_anim_mask, loop=False
    )
    asteroid = Asteroid(x, y, asteroid_img, 1, asteroid_poof_anim, crt_surface)
    asteroid_group.add(asteroid)


def crt_handle_event(dt, event):
    if event.type == SPAWN_ASTEROID:
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            x = random.randint(0, CRT_SURFACE_WIDTH)
            y = -100
        elif side == "bottom":
            x = random.randint(0, CRT_SURFACE_WIDTH)
            y = CRT_SURFACE_HEIGHT + 100
        elif side == "left":
            x = -100
            y = random.randint(0, CRT_SURFACE_HEIGHT)
        else:  # "right"
            x = CRT_SURFACE_WIDTH + 100
            y = random.randint(0, CRT_SURFACE_HEIGHT)

        create_asteroid(x, y)


"""
def play_shield(dt, green_box, sfx, shield_anim_playing=False):
    pos = green_box.position

    if pos == 1 and not shield_anim_playing:
        shield_anim.reset()
        other_sounds(sfx, "shield")
        shield_anim_playing = True

    if shield_anim_playing:
        shield_anim.update(dt)
        crt_surface.blit(
            shield_anim.get_current_frame(),
            shield_anim.pos,
        )

        if shield_anim.is_done():  # You need this method!
            shield_anim_playing = False


def play_shield(
    dt,
    green_box,
    sfx,
    _state={"prev_pos": None, "active": False, "last_trigger": -9999},
):
    cooldown_ms = 10000  # 2 sec cooldown
    now = pygame.time.get_ticks()

    pos = green_box.position

    if pos == 1 and _state["prev_pos"] != 1:
        if now - _state["last_trigger"] >= cooldown_ms:
            shield_anim.reset()
            _state["active"] = True

            other_sounds(sfx, "shield")
            _state["last_trigger"] = now

    _state["prev_pos"] = pos

    if _state["active"]:
        shield_anim.update(dt)
        crt_surface.blit(
            shield_anim.get_current_frame(),
            shield_anim.pos,
        )
        if shield_anim.finished:
            _state["active"] = False
"""
