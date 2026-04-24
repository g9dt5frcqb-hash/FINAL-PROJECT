import pygame
import os
from engine.settings import PLAYER_SPEED

def slice_row(sheet, row_index, frame_count, frame_height):
    frames = []
    sheet_width = sheet.get_width()
    frame_width = sheet_width // frame_count
    y = row_index * frame_height
    for i in range(frame_count):
        x = i * frame_width
        frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)
    return frames

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Player:
    def __init__(self, x, y):
        sprite_path = os.path.join(BASE_DIR, "assets", "sprites", "phineas.png")
        self.sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frame_height = 60
        self.walk_right = slice_row(self.sheet, 2, 12, self.frame_height)
        self.walk_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_right]
        self.walk_down = [slice_row(self.sheet, 0, 8, self.frame_height)[0]]
        self.walk_up = [pygame.transform.flip(self.walk_down[0], False, True)]
        self.current_animation = self.walk_down
        self.frame_index = 0
        self.animation_speed = 12
        self.image = self.current_animation[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt, world):
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_w]:
            self.current_animation = self.walk_up
            self.rect.y -= PLAYER_SPEED * dt
            moving = True
        elif keys[pygame.K_s]:
            self.current_animation = self.walk_down
            self.rect.y += PLAYER_SPEED * dt
            moving = True
        elif keys[pygame.K_a]:
            self.current_animation = self.walk_left
            self.rect.x -= PLAYER_SPEED * dt
            moving = True
        elif keys[pygame.K_d]:
            self.current_animation = self.walk_right
            self.rect.x += PLAYER_SPEED * dt
            moving = True
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0
            self.image = self.current_animation[int(self.frame_index)]
        else:
            self.image = self.current_animation[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
