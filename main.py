import asyncio  # needed for Pygbag async

import pygame

from classes import Box

# importing constant variables from constants.py
from constants import (
    BG_COLOR,
    # BOX_NAMES,
    BOX_Y,
    # BOX_COLORS,
    GREEN_COLOR,
    NODE_SIZE,
    ORANGE_COLOR,
    PURPLE_COLOR,
    RED_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    YELLOW_COLOR,
)
from grad import grad_box_create

# importing the function that selects the squares from selector.py
from selector import selector_func
from sound import chirper, load_sound_effects

# system stuff
clock = pygame.time.Clock()
pygame.init()
debug_font = pygame.font.Font(None, 30)
sfx = load_sound_effects()


# local variables
selected_index = 0
selected_box = 0

yellow_box = Box("yellow_box", YELLOW_COLOR, 266, BOX_Y, NODE_SIZE)
green_box = Box("green_box", GREEN_COLOR, 533, BOX_Y, NODE_SIZE)
orange_box = Box("orange_box", ORANGE_COLOR, 800, BOX_Y, NODE_SIZE)
purple_box = Box("purple_box", PURPLE_COLOR, 1066, BOX_Y, NODE_SIZE)
red_box = Box("red_box", RED_COLOR, 1332, BOX_Y, NODE_SIZE)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


async def main():
    global selected_index, selected_box
    run = True
    while run:
        clock.tick(60)

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    selected_index = (selected_index + 1) % len(Box.all_boxes)
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    if selected_box.y > 100:
                        selected_box.move_y(-250)
                        chirper(selected_box.y, sfx, selected_box.name)
                elif event.y < 0:
                    if selected_box.y < 1100:
                        selected_box.move_y(250)
                        chirper(selected_box.y, sfx, selected_box.name)
        # Fill the background
        screen.fill(BG_COLOR)

        # Draw all boxes
        for box in Box.all_boxes:
            pygame.draw.rect(
                screen,
                box.color,
                box.rect,
            )

        selected_box = Box.all_boxes[selected_index]
        selector_func(screen, selected_box.x, selected_box.y)

        grad_box_create(
            screen,
            YELLOW_COLOR,
            GREEN_COLOR,
            False,
            True,
            19,
            yellow_box,
            green_box,
        )
        # Display debug information on screen
        debug_display_string = f"selected_box: {selected_box.name}"
        text_surface = debug_font.render(debug_display_string, True, (0, 200, 0))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()
    return


asyncio.run(main())
