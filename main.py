import pygame

# importing constant variables from constants.py
from constants import (
    BG_COLOR,
    GREEN_COLOR,
    NODE_SIZE,
    # OUTLINE_WIDTH,
    # OUTLINE_HEIGHT,
    NODE_SPACER,
    ORANGE_COLOR,
    OUTLINE_OFFSET,
    PURPLE_COLOR,
    RED_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    YELLOW_COLOR,
)

# importing the function that selects the squares from selector.py
from selector import selector_func
from sound import chirper, load_sound_effects

# system stuff
pygame.init()
debug_font = pygame.font.Font(None, 30)
sfx = load_sound_effects()

# local arrays
box_names = ["yellow_box", "green_box", "purple_box", "orange_box", "red_box"]
box_colors = [YELLOW_COLOR, GREEN_COLOR, PURPLE_COLOR, ORANGE_COLOR, RED_COLOR]

# local variables
boxes = {}
node_mod = 1
selected_index = 0
selected_box = 0
# current_box_name = box_names[selected_index]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# this creates the Rects for the boxes and adds them all to the "boxes" dictionary. You can call properties of these
for name in box_names:
    x = (NODE_SPACER * node_mod) + OUTLINE_OFFSET
    y = SCREEN_HEIGHT / 2
    boxes[name] = pygame.Rect(x, y, NODE_SIZE, NODE_SIZE)
    node_mod += 1

run = True
while run:
    current_box_name = box_names[selected_index]
    # input handler
    # closes the game if the X is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # cycles between nodes if tab is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                selected_index = (selected_index + 1) % len(box_names)
        # moves the selected box with the mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            # scrolling up
            if event.y > 0:
                if selected_box.y > 100:
                    selected_box.y -= 250
                    chirper(selected_box.y, sfx, current_box_name)
            # scrolling down
            elif event.y < 0:
                if selected_box.y < 1100:
                    selected_box.y += 250
                    chirper(selected_box.y, sfx, current_box_name)

    # add bg color
    screen.fill(BG_COLOR)

    # outline
    for name, color in zip(box_names, box_colors):
        pygame.draw.rect(screen, color, boxes[name])

    selected_box = boxes[box_names[selected_index]]
    selector_func(screen, selected_box.x, selected_box.y)

    """
    # a string with the variables to display
    debug_display_string = f"selected_box: {current_box_name}"
    # render the string
    text_surface = debug_font.render(
        debug_display_string, True, (0, 200, 0)
    )
    # draw that text surface onto the main screen
    screen.blit(
        text_surface, (10, 10)
    )
    """

    # system stuff
    pygame.display.flip()

pygame.quit()
