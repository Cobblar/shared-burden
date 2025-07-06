import pygame


from sound import load_sound_effects, other_sounds, play_sound_once
from images import shield_anim_frames, SpriteAnimation
from constants import CRT_SURFACE_HEIGHT, CRT_SURFACE_WIDTH
from images import mars_img, mars_half_x, mars_half_y, sun_img, moon_img
from orbit import OrbitingObject  # <--- Import the OrbitingObject class

crt_surface = pygame.Surface((CRT_SURFACE_WIDTH, CRT_SURFACE_HEIGHT), pygame.SRCALPHA)

# --- Instantiate the OrbitingObject for the sun at the module level ---
moon_orbit_radius = 300
moon_orbit_speed = 0

moon_orbiting_mars = OrbitingObject(
    orbiting_image=moon_img,
    central_pos=(CRT_SURFACE_WIDTH / 2, CRT_SURFACE_HEIGHT / 2),
    orbit_radius=moon_orbit_radius,
    orbit_speed=moon_orbit_speed,
    initial_angle=0.0,
)
# load sounds
# sfx = load_sound_effects()
# animations
shield_anim = SpriteAnimation(shield_anim_frames, fps=15, loop=False)

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
    dt, green_box, _state={"prev_pos": None, "active": False, "last_trigger": -9999}
):
    cooldown_ms = 10000  # 2 sec cooldown
    now = pygame.time.get_ticks()

    pos = green_box.position

    if pos == 1 and _state["prev_pos"] != 1:
        if now - _state["last_trigger"] >= cooldown_ms:
            shield_anim.reset()
            _state["active"] = True
            # <-- no .play_sound_once
            other_sounds(load_sound_effects(), "shield")
            _state["last_trigger"] = now

    _state["prev_pos"] = pos

    if _state["active"]:
        shield_anim.update(dt)
        crt_surface.blit(
            shield_anim.get_current_frame(),
            ((CRT_SURFACE_WIDTH // 2) - 240, (CRT_SURFACE_HEIGHT // 2) - 240),
        )
        if shield_anim.finished:
            _state["active"] = False


def crt(surface, yellow_box, green_box, Box, dt):
    # create background color
    crt_surface.fill((0, 0, 0))
    # draw mars onto the crt (central image)
    # Original blitting logic for mars_img
    crt_surface.blit(
        mars_img,
        (
            ((CRT_SURFACE_WIDTH / 2) - mars_half_x),
            ((CRT_SURFACE_HEIGHT / 2) - mars_half_y),
        ),
    )
    moon_orbiting_mars.orbit_speed = yellow_box.position * 1.5

    play_shield(dt, green_box)
    # Call update_position to calculate the new location and update the internal angle.
    moon_orbiting_mars.update_position()
    # Now, explicitly blit the sun's image using the updated rect attribute.
    crt_surface.blit(moon_orbiting_mars.orbiting_image, moon_orbiting_mars.rect)
    # draw the crt onto the main game surface:w
    surface.blit(crt_surface, (0, 0))
