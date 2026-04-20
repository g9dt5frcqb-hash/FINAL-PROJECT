import pygame

class World:
    def __init__(self):
        self.color = (34, 139, 34)  # green grass

    def draw(self, screen):
        screen.fill(self.color)
