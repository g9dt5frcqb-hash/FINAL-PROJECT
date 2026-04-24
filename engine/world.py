import pygame

class World:
    def __init__(self):
        self.color = (34, 139, 34)

    def draw(self, screen):
        screen.fill(self.color)
