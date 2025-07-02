import pygame

from constants import (
    GREEN_COLOR,
    NODE_SIZE,
    NODE_SPACER,
    ORANGE_COLOR,
    OUTLINE_OFFSET,
    PURPLE_COLOR,
    RED_COLOR,
    SCREEN_HEIGHT,
    YELLOW_COLOR,
)

box_names = ["yellow_box", "green_box", "purple_box", "orange_box", "red_box"]
box_colors = [YELLOW_COLOR, GREEN_COLOR, PURPLE_COLOR, ORANGE_COLOR, RED_COLOR]

boxes = {}

node_mod = 1

for name, color in zip(box_names, box_colors):
    x = (NODE_SPACER * node_mod) + OUTLINE_OFFSET
    y = SCREEN_HEIGHT / 2
    rect = pygame.Rect(x, y, NODE_SIZE, NODE_SIZE)
    boxes[name] = {"rect": rect, "color": color}
    node_mod += 1
