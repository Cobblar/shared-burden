import pygame

from constants import (
    BG_COLOR,
    GREEN_COLOR,
    NODE_SIZE,
    ORANGE_COLOR,
    PURPLE_COLOR,
    RED_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from selector import selector_func

OUTLINE_WIDTH = SCREEN_WIDTH - 100
OUTLINE_HEIGHT = SCREEN_HEIGHT - 100
NODE_SPACER = OUTLINE_WIDTH / 6
OUTLINE_OFFSET = 58

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working With Shapes")
# yellow_box = pygame.rect((NODE_SPACER * 2) + OUTLINE_OFFSET, 300, NODE_SIZE, NODE_SIZE)

run = True
while run:
    screen.fill(BG_COLOR)
    # outline

    selector_func(screen, 1000)

    pygame.draw.rect(
        screen, (216, 222, 233), (50, 50, OUTLINE_WIDTH, OUTLINE_HEIGHT), width=8
    )
    # squares
    pygame.draw.rect(
        screen, GREEN_COLOR, (NODE_SPACER + OUTLINE_OFFSET, 300, NODE_SIZE, NODE_SIZE)
    )
    # pygame.draw.rect(screen, YELLOW_COLOR, yellow_box)
    pygame.draw.rect(
        screen,
        ORANGE_COLOR,
        ((NODE_SPACER * 3) + OUTLINE_OFFSET, 300, NODE_SIZE, NODE_SIZE),
    )
    pygame.draw.rect(
        screen,
        PURPLE_COLOR,
        ((NODE_SPACER * 4) + OUTLINE_OFFSET, 300, NODE_SIZE, NODE_SIZE),
    )
    pygame.draw.rect(
        screen,
        RED_COLOR,
        ((NODE_SPACER * 5) + OUTLINE_OFFSET, 300, NODE_SIZE, NODE_SIZE),
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
