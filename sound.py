import pygame


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
    }
    return sounds


def chirper(objx, sfx_lib, selected_box):
    if objx == 100:
        # position 1 highest note
        if selected_box == "green_box":
            sfx_lib["saw_5"].play()
        elif selected_box == "yellow_box":
            sfx_lib["voice_5"].play()
        elif selected_box == "red_box":
            sfx_lib["bitnoise_5"].play()
        elif selected_box == "orange_box":
            sfx_lib["rasp_5"].play()
        elif selected_box == "purple_box":
            sfx_lib["whistle_5"].play()
    elif objx == 350:
        # position 2
        if selected_box == "green_box":
            sfx_lib["saw_4"].play()
        elif selected_box == "yellow_box":
            sfx_lib["voice_4"].play()
        elif selected_box == "red_box":
            sfx_lib["bitnoise_4"].play()
        elif selected_box == "orange_box":
            sfx_lib["rasp_4"].play()
        elif selected_box == "purple_box":
            sfx_lib["whistle_4"].play()
    elif objx == 600:
        # position 3
        if selected_box == "green_box":
            sfx_lib["saw_3"].play()
        elif selected_box == "yellow_box":
            sfx_lib["voice_3"].play()
        elif selected_box == "red_box":
            sfx_lib["bitnoise_3"].play()
        elif selected_box == "orange_box":
            sfx_lib["rasp_3"].play()
        elif selected_box == "purple_box":
            sfx_lib["whistle_3"].play()
    elif objx == 850:
        # position 4
        if selected_box == "green_box":
            sfx_lib["saw_2"].play()
        elif selected_box == "yellow_box":
            sfx_lib["voice_2"].play()
        elif selected_box == "red_box":
            sfx_lib["bitnoise_2"].play()
        elif selected_box == "orange_box":
            sfx_lib["rasp_2"].play()
        elif selected_box == "purple_box":
            sfx_lib["whistle_2"].play()
    elif objx == 1100:
        # position 5 and lowest note
        if selected_box == "green_box":
            sfx_lib["saw_1"].play()
        elif selected_box == "yellow_box":
            sfx_lib["voice_1"].play()
        elif selected_box == "red_box":
            sfx_lib["bitnoise_1"].play()
        elif selected_box == "orange_box":
            sfx_lib["rasp_1"].play()
        elif selected_box == "purple_box":
            sfx_lib["whistle_1"].play()
