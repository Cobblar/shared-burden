import pygame

from constants import CONTROL_SURFACE_HEIGHT
from sound import chirper, other_sounds


def handle_input(event, engine, selected_index, selected_box, sfx, Box):
    if event.type == pygame.QUIT:
        # Signal to the calling scene that the game should stop running
        return False, selected_index, selected_box

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            # Cycle through selected boxes
            selected_index = (selected_index + 1) % len(Box.all_boxes)
            if selected_index == 0:
                other_sounds(sfx, "restart_cycle")
            else:
                other_sounds(sfx, "cycle")
        elif event.key == pygame.K_1:
            # Change resolution using the engine's set_resolution method
            engine.set_resolution(0)
        elif event.key == pygame.K_2:
            # Change resolution using the engine's set_resolution method
            engine.set_resolution(1)
        elif event.key == pygame.K_3:
            # Change resolution using the engine's set_resolution method
            engine.set_resolution(2)

    if event.type == pygame.MOUSEWHEEL:
        if selected_box:  # Ensure a box is selected before attempting to move it
            if event.y > 0:  # Scroll up
                # Check bounds for moving up
                if selected_box.y > 100:  # Assuming 100 is the upper bound
                    selected_box.move_y(-(CONTROL_SURFACE_HEIGHT // 6))
                    chirper(selected_box.y, sfx, selected_box.name)
            elif event.y < 0:  # Scroll down
                # Check bounds for moving down
                if selected_box.y < 350:  # Assuming 350 is the lower bound
                    selected_box.move_y((CONTROL_SURFACE_HEIGHT // 6))
                    chirper(selected_box.y, sfx, selected_box.name)

    # Return True to indicate the game loop should continue, along with updated values
    return True, selected_index, selected_box
