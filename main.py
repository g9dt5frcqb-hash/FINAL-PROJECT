import pygame
from engine.settings import *
from engine.player import Player
from engine.Ferb import Ferb
from engine.world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phineas & Ferb: Open World")

clock = pygame.time.Clock()

# Create game objects
player = Player(300, 200)
ferb = Ferb(400, 200)  # spawn Ferb a bit to the right of Phineas
world = World()

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update(dt, world)
    ferb.update(dt, world)

    # Draw
    world.draw(screen)
    player.draw(screen)
    ferb.draw(screen)

    pygame.display.flip()

pygame.quit()