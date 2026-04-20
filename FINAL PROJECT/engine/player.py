import pygame
from engine.settings import PLAYER_SPEED

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)

    def update(self, dt, world):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED * dt
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED * dt
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED * dt

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
