import pygame

from constants import CONTROL_SURFACE_HEIGHT


def load_sound_effects():
    """Loads all sound effects and returns them in a dictionary."""
    sounds = {
        # saw sounds
        "saw_1": pygame.mixer.Sound("sound/saw/1.wav"),
        "saw_2": pygame.mixer.Sound("sound/saw/2.wav"),
        "saw_3": pygame.mixer.Sound("sound/saw/3.wav"),
        "saw_4": pygame.mixer.Sound("sound/saw/4.wav"),
        "saw_5": pygame.mixer.Sound("sound/saw/5.wav"),
        # # voice sounds
        "voice_1": pygame.mixer.Sound("sound/voice/1.wav"),
        "voice_2": pygame.mixer.Sound("sound/voice/2.wav"),
        "voice_3": pygame.mixer.Sound("sound/voice/3.wav"),
        "voice_4": pygame.mixer.Sound("sound/voice/4.wav"),
        "voice_5": pygame.mixer.Sound("sound/voice/5.wav"),
        # # rasp sounds
        "rasp_1": pygame.mixer.Sound("sound/rasp/1.wav"),
        "rasp_2": pygame.mixer.Sound("sound/rasp/2.wav"),
        "rasp_3": pygame.mixer.Sound("sound/rasp/3.wav"),
        "rasp_4": pygame.mixer.Sound("sound/rasp/4.wav"),
        "rasp_5": pygame.mixer.Sound("sound/rasp/5.wav"),
        # # bitnoise sounds
        "bitnoise_1": pygame.mixer.Sound("sound/bitnoise/1.wav"),
        "bitnoise_2": pygame.mixer.Sound("sound/bitnoise/2.wav"),
        "bitnoise_3": pygame.mixer.Sound("sound/bitnoise/3.wav"),
        "bitnoise_4": pygame.mixer.Sound("sound/bitnoise/4.wav"),
        "bitnoise_5": pygame.mixer.Sound("sound/bitnoise/5.wav"),
        # # whistle sounds
        "whistle_1": pygame.mixer.Sound("sound/whistle/1.wav"),
        "whistle_2": pygame.mixer.Sound("sound/whistle/2.wav"),
        "whistle_3": pygame.mixer.Sound("sound/whistle/3.wav"),
        "whistle_4": pygame.mixer.Sound("sound/whistle/4.wav"),
        "whistle_5": pygame.mixer.Sound("sound/whistle/5.wav"),
        # misc control surface sounds
        "cycle": pygame.mixer.Sound("sound/selectors/forward.wav"),
        "restart_cycle": pygame.mixer.Sound("sound/selectors/restart.wav"),
        "bump_edge": pygame.mixer.Sound("sound/bump_edge.wav"),
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
