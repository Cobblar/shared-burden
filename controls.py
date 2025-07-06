import pygame

from constants import CONTROL_SURFACE_HEIGHT
from sound import chirper, other_sounds


def handle_input(event, display, selected_index, selected_box, sfx, Box):
    """
    Handles a single event. Returns updated (selected_index, selected_box).
    """
    if event.type == pygame.QUIT:
        return False, selected_index, selected_box  # signal to stop loop
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            selected_index = (selected_index + 1) % len(Box.all_boxes)
            if selected_index == 0:
                other_sounds(sfx, "restart_cycle")
            else:
                other_sounds(sfx, "cycle")
    if event.type == pygame.MOUSEWHEEL:
        if event.y > 0:
            if selected_box.y > 100:
                selected_box.move_y(-(CONTROL_SURFACE_HEIGHT // 6))
                selected_box.position += 1
                chirper(selected_box.y, sfx, selected_box.name)

        elif event.y < 0:
            if selected_box.y < 350:
                selected_box.move_y((CONTROL_SURFACE_HEIGHT // 6))
                chirper(selected_box.y, sfx, selected_box.name)
                selected_box.position -= 1
    return True, selected_index, selected_box
