import pygame


from sound import load_sound_effects, other_sounds, play_sound_once
from images import shield_anim_frames, shield_anim_mask, SpriteAnimation
from constants import CRT_SURFACE_HEIGHT, CRT_SURFACE_WIDTH
from images import (
    mars_img,
    mars_half_x,
    mars_half_y,
    # sun_img,
    moon_img,
    asteroid_img,
    terraformer_img,
)
from orbit import OrbitingBehavior  # <--- Import the OrbitingObject class
from classes import Planet, Asteroid, Terraformer

# create the surface
crt_surface = pygame.Surface((CRT_SURFACE_WIDTH, CRT_SURFACE_HEIGHT))

# instances of classes
mars = Planet(
    mars_img,
    "mars",
    (CRT_SURFACE_WIDTH / 2),
    (CRT_SURFACE_HEIGHT / 2),
    orbiting_behavior=None,
)
asteroid = Asteroid(20, CRT_SURFACE_HEIGHT / 2, asteroid_img)

# --- Instantiate the OrbitingPattern for the sun at the module level ---
moon_orbit_radius = 300
moon_orbit_speed = 1
moon_orbiting_mars = OrbitingBehavior(
    central_pos=(mars.rect.x + mars_half_x, mars.rect.y + mars_half_y),
    orbit_radius=moon_orbit_radius,
    orbit_speed=moon_orbit_speed,
    initial_angle=0.0,
)

moon = Planet(moon_img, "moon", 0, 0, orbiting_behavior=moon_orbiting_mars)

terraformer_orbit_radius = 140
terraformer_orbit_speed = 0.25
terraformer_orbiting_mars = OrbitingBehavior(
    central_pos=(mars.rect.x + mars_half_x, mars.rect.y + mars_half_y),
    orbit_radius=terraformer_orbit_radius,
    orbit_speed=terraformer_orbit_speed,
    initial_angle=270,
)

moon = Planet(moon_img, "moon", 0, 0, orbiting_behavior=moon_orbiting_mars)
terraformer1 = Terraformer(
    terraformer_img, "terraformer1", 0, 0, orbiting_behavior=terraformer_orbiting_mars
)
# load sounds
# load sounds
# sfx = load_sound_effects()
# animations
shield_pos = ((CRT_SURFACE_WIDTH // 2) - 240, (CRT_SURFACE_HEIGHT // 2) - 240)
shield_anim = SpriteAnimation(
    shield_pos, shield_anim_frames, fps=15, masks=shield_anim_mask, loop=False
)

# groups
mars_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
shield_group = pygame.sprite.Group()
# add to the groups
mars_group.add(mars)
asteroid_group.add(asteroid)
shield_group.add(shield_anim)
"""
def play_shield(dt):  # call to play the shield. Contains sound and animation.
    shield_anim.update(dt)
    if not shield_anim.finished:
        crt_surface.blit(
            shield_anim.get_current_frame(),
            ((((CRT_SURFACE_WIDTH / 2) - 240), ((CRT_SURFACE_HEIGHT / 2) - 240))),
        )
        play_sound_once("shield")
"""


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


def crt(surface, yellow_box, green_box, Box, dt, sfx):
    # create background color
    crt_surface.fill((0, 0, 0))
    # draw stuff onto the crt (central image)
    crt_surface.blit(mars.image, mars.rect)
    moon.update()
    crt_surface.blit(moon.image, moon.rect)
    terraformer1.update()
    crt_surface.blit(terraformer1.image, terraformer1.rect)
    crt_surface.blit(asteroid.image, asteroid.rect)
    asteroid.move(1, mars.vector)
    # bases moon orbiting speed on position of yellow box
    # moon_orbiting_mars.orbit_speed = yellow_box.position * 2.5
    # plays the sheild animation
    play_shield(dt, green_box, sfx)
    # Call update_position to calculate the new location and update the internal angle.
    # moon_orbiting_mars.update_position()
    # Now, explicitly blit the sun's image using the updated rect attribute.
    # crt_surface.blit(moon_orbiting_mars.orbiting_image, moon_orbiting_mars.rect)

    if pygame.sprite.spritecollide(asteroid, mars_group, False):
        if pygame.sprite.spritecollide(
            asteroid, mars_group, True, pygame.sprite.collide_mask
        ):
            mars.darken()
            asteroid.impact()
    if pygame.sprite.spritecollide(asteroid, shield_group, False):
        if pygame.sprite.spritecollide(
            asteroid, shield_group, False, pygame.sprite.collide_mask
        ):
            asteroid.impact()
    # draw the crt onto the main game surface
    surface.blit(crt_surface, (0, 0))
