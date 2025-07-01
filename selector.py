import pygame


def selector_func(screen, x, y):
    border = 8
    pygame.draw.rect(
        screen, (216, 222, 233), (x - border, y - border, 36, 36), width=border
    )
