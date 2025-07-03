import pygame

from constants import CONTROL_SURFACE_HEIGHT
from sound import chirper


def handle_input(event, display, selected_index, selected_box, sfx, Box, resolutions):
    """
    Handles a single event. Returns updated (selected_index, selected_box).
    """
    if event.type == pygame.QUIT:
        return False, selected_index, selected_box  # signal to stop loop

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            selected_index = (selected_index + 1) % len(Box.all_boxes)
        elif event.key == pygame.K_1:
            display.switch_resolution(0)
        elif event.key == pygame.K_2:
            display.switch_resolution(1)
        elif event.key == pygame.K_3:
            display.switch_resolution(2)

    if event.type == pygame.MOUSEWHEEL:
        if event.y > 0:
            if selected_box.y > 100:
                selected_box.move_y(-(CONTROL_SURFACE_HEIGHT // 6))
                chirper(selected_box.y, sfx, selected_box.name)
        elif event.y < 0:
            if selected_box.y < 350:
                selected_box.move_y((CONTROL_SURFACE_HEIGHT // 6))
                chirper(selected_box.y, sfx, selected_box.name)

    return True, selected_index, selected_box
