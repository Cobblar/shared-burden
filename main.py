import asyncio  # needed for Pygbag async
import pygame

pygame.init()
display = pygame.display.set_mode((1080, 1440))


from sound import load_sound_effects
from selector import selector_func
from controls import handle_input
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
from classes import Box
from crt_surface import crt




# importing constant variables from constants.py


# importing the function that selects the squares from selector.py

# system stuff
clock = pygame.time.Clock()
aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT

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


async def main():
    global selected_index, selected_box
    run = True
    while run:
        dt = clock.tick(60)

        for event in pygame.event.get():
            run, selected_index, selected_box = handle_input(
                event, display, selected_index, selected_box, sfx, Box
            )
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
        selector_func(control_surface, selected_box.x, selected_box.y)
        # Display debug information on screen
        debug_display_string = f"selected_box: {selected_box.name}"
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
