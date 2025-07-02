import pygame


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
