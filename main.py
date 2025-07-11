import asyncio  # nopep8
import pygame  # nopep8
import score  # nopep8

pygame.init()  # nopep8
display = pygame.display.set_mode((1080, 1440))  # nopep8

from crt_surface import crt, crt_handle_event
from classes import Box, Selector
from constants import (
    BG_COLOR,
    CONTROL_SURFACE_BG_COLOR,
    CONTROL_SURFACE_HEIGHT,
    CONTROL_SURFACE_WIDTH,
    CONTROL_SURFACE_Y_HEIGHT,
    GREEN_COLOR,
    NODE_SIZE,
    ORANGE_COLOR,
    PURPLE_COLOR,
    RED_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    YELLOW_COLOR,
)
from controls import handle_input
from sound import load_sound_effects


# importing constant variables from constants.py


# importing the function that selects the squares from selector.py

# system stuff
clock = pygame.time.Clock()
aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT


bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)
debug_font = pygame.font.Font(None, 30)
sfx = load_sound_effects()

# local variables
selected_index = 0
selected_box = 0

yellow_box = Box(
    "yellow_box",
    YELLOW_COLOR,
    ((CONTROL_SURFACE_WIDTH // 6) * 1),
    CONTROL_SURFACE_HEIGHT / 2,
    NODE_SIZE,
)
green_box = Box(
    "green_box",
    GREEN_COLOR,
    ((CONTROL_SURFACE_WIDTH // 6) * 2),
    CONTROL_SURFACE_HEIGHT / 2,
    NODE_SIZE,
)
orange_box = Box(
    "orange_box",
    ORANGE_COLOR,
    ((CONTROL_SURFACE_WIDTH // 6) * 3),
    CONTROL_SURFACE_HEIGHT / 2,
    NODE_SIZE,
)
purple_box = Box(
    "purple_box",
    PURPLE_COLOR,
    ((CONTROL_SURFACE_WIDTH // 6) * 4),
    CONTROL_SURFACE_HEIGHT / 2,
    NODE_SIZE,
)
red_box = Box(
    "red_box",
    RED_COLOR,
    ((CONTROL_SURFACE_WIDTH // 6) * 5),
    CONTROL_SURFACE_HEIGHT / 2,
    NODE_SIZE,
)


control_surface = pygame.Surface(
    (CONTROL_SURFACE_WIDTH, CONTROL_SURFACE_HEIGHT), pygame.SRCALPHA
)

main_selector = Selector(8, control_surface)


def pause():
    text = bigfont.render("Click Me to Resume", 13, (0, 0, 0))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(
        display,
        (255, 255, 255),
        ((textx - 5, texty - 5), (textx_size + 10, texty_size + 10)),
    )

    display.blit(
        text,
        (
            SCREEN_WIDTH / 2 - text.get_width() / 2,
            SCREEN_HEIGHT / 2 - text.get_height() / 2,
        ),
    )

    clock = pygame.time.Clock()
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False
                        break


async def main():
    global selected_index, selected_box
    current_score = 0
    run = True
    while run:
        dt = clock.tick(60)

        for event in pygame.event.get():
            crt_handle_event(dt, event)
            run, selected_index, selected_box = handle_input(
                event, display, selected_index, selected_box, sfx, Box
            )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
        # Assign the surface and the screen to local variables
        # it's not required, but I guess it's best practice
        game_surface = display
        # Fill the background
        game_surface.fill(BG_COLOR)
        control_surface.fill(CONTROL_SURFACE_BG_COLOR)

        crt(game_surface, yellow_box, green_box, Box, dt, sfx)
        # Draw all boxes
        for box in Box.all_boxes:
            pygame.draw.rect(
                control_surface,
                box.color,
                box.rect,
            )

        selected_box = Box.all_boxes[selected_index]
        main_selector.update(selected_box.x, selected_box.y)
        # selector_func(control_surface, selected_box.x, selected_box.y)
        green_box.update()
        if score.score_tracker:
            current_score += 0.016
        # Display debug information on screen
        debug_display_string = f"Score: {'%.2f' % (current_score)}"
        text_surface = debug_font.render(debug_display_string, True, (0, 200, 0))
        display.blit(text_surface, (10, 10))

        # BLIT control_surface ONTO game_surface (not directly to screen)
        game_surface.blit(control_surface, (0, CONTROL_SURFACE_Y_HEIGHT))
        # Scale and blit the game surface to the screen

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()
    return


asyncio.run(main())
