import pygame

from constants import CONTROL_SURFACE_HEIGHT


def load_sound_effects():
    """Loads all sound effects and returns them in a dictionary."""
    sounds = {
        # saw sounds
        "saw_1": pygame.mixer.Sound("sound/saw/1.ogg"),
        "saw_2": pygame.mixer.Sound("sound/saw/2.ogg"),
        "saw_3": pygame.mixer.Sound("sound/saw/3.ogg"),
        "saw_4": pygame.mixer.Sound("sound/saw/4.ogg"),
        "saw_5": pygame.mixer.Sound("sound/saw/5.ogg"),
        # # voice sounds
        "voice_1": pygame.mixer.Sound("sound/voice/1.ogg"),
        "voice_2": pygame.mixer.Sound("sound/voice/2.ogg"),
        "voice_3": pygame.mixer.Sound("sound/voice/3.ogg"),
        "voice_4": pygame.mixer.Sound("sound/voice/4.ogg"),
        "voice_5": pygame.mixer.Sound("sound/voice/5.ogg"),
        # # rasp sounds
        "rasp_1": pygame.mixer.Sound("sound/rasp/1.ogg"),
        "rasp_2": pygame.mixer.Sound("sound/rasp/2.ogg"),
        "rasp_3": pygame.mixer.Sound("sound/rasp/3.ogg"),
        "rasp_4": pygame.mixer.Sound("sound/rasp/4.ogg"),
        "rasp_5": pygame.mixer.Sound("sound/rasp/5.ogg"),
        # # bitnoise sounds
        "bitnoise_1": pygame.mixer.Sound("sound/bitnoise/1.ogg"),
        "bitnoise_2": pygame.mixer.Sound("sound/bitnoise/2.ogg"),
        "bitnoise_3": pygame.mixer.Sound("sound/bitnoise/3.ogg"),
        "bitnoise_4": pygame.mixer.Sound("sound/bitnoise/4.ogg"),
        "bitnoise_5": pygame.mixer.Sound("sound/bitnoise/5.ogg"),
        # # whistle sounds
        "whistle_1": pygame.mixer.Sound("sound/whistle/1.ogg"),
        "whistle_2": pygame.mixer.Sound("sound/whistle/2.ogg"),
        "whistle_3": pygame.mixer.Sound("sound/whistle/3.ogg"),
        "whistle_4": pygame.mixer.Sound("sound/whistle/4.ogg"),
        "whistle_5": pygame.mixer.Sound("sound/whistle/5.ogg"),
        # misc control surface sounds
        "cycle": pygame.mixer.Sound("sound/selectors/forward.ogg"),
        "restart_cycle": pygame.mixer.Sound("sound/selectors/restart.ogg"),
        "bump_edge": pygame.mixer.Sound("sound/bump_edge.ogg"),
        # crt sounds
        "shield": pygame.mixer.Sound("sound/shield.ogg"),
        "laser": pygame.mixer.Sound("sound/laser.ogg"),
        "asteroid_impact": pygame.mixer.Sound("sound/asteroid_impact.ogg"),
        "terraformer_death": pygame.mixer.Sound("sound/terraformer_death.ogg"),
    }
    return sounds


def chirper(objy, sfx_lib, selected_box):
    positions = [
        (1, "5"),  # highest note
        (2, "4"),
        (3, "3"),
        (4, "2"),
        (5, "1"),  # lowest note
    ]

    box_sounds = {
        "green_box": "saw_",
        "yellow_box": "voice_",
        "red_box": "bitnoise_",
        "orange_box": "rasp_",
        "purple_box": "whistle_",
    }

    for pos, note in positions:
        if objy == (CONTROL_SURFACE_HEIGHT // 6) * pos:
            prefix = box_sounds.get(selected_box)
            key = f"{prefix}{note}"
            sfx_lib[key].play()


last_played_times = {}


def other_sounds(sfx_lib, sound_name):
    now = pygame.time.get_ticks()  # Milliseconds since pygame.init()

    # If we've played it before, check time since last play
    if sound_name in last_played_times:
        last_time = last_played_times[sound_name]
        if now - last_time < 50:
            return  # Too soon, skip playing

    # Play the sound and update the time
    sfx_lib[sound_name].play()
    last_played_times[sound_name] = now


played_sounds = {}


def play_sound_once(name):
    if not played_sounds.get(name, False):
        other_sounds(load_sound_effects(), name)
        played_sounds[name] = True
