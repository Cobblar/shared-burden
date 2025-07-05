import pygame


class Box:
    # keeps a list of all boxes
    all_boxes = []

    def __init__(self, name, color, x, y, size):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        Box.all_boxes.append(self)  # adds each box to all_boxes

    def move_y(self, amount):
        self.y += amount
        self.rect.y = self.y

    @classmethod
    def create_box(cls, name, color, x, y, size):
        return cls(name, color, x, y, size)

    @classmethod
    def clear_boxes(cls):
        cls.all_boxes = []
