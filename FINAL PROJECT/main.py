import pygame
from engine.settings import *
from engine.player import Player
from engine.world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phineas & Ferb: Open World")

clock = pygame.time.Clock()

# Create game objects
player = Player(300, 200)
world = World()

running = True
while running:
    dt = clock.tick(60) / 1000  # delta time for smooth movement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(dt, world)

    # Draw
    screen.fill((135, 206, 235))  # sky blue background
    world.draw(screen)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
