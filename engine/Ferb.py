import pygame
import os
from engine.settings import PLAYER_SPEED


def slice_row(sheet, row_index, frame_count, frame_height):
    """Slice a horizontal row of frames from a sprite sheet."""
    frames = []
    sheet_width = sheet.get_width()
    frame_width = sheet_width // frame_count
    y = row_index * frame_height

    for i in range(frame_count):
        x = i * frame_width
        frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)

    return frames


class Ferb:
    def __init__(self, x, y):
        
        self.sheet = pygame.image.load(
            os.path.join("engine", "assets", "sprites", "Ferb.png")
        ).convert_alpha()

        
        self.sheet.set_colorkey((0, 0, 139))

        
        self.frame_height = 60

        
        self.walk_right = slice_row(self.sheet, 2, 9, self.frame_height)
        self.walk_left  = [
            pygame.transform.flip(f, True, False) for f in self.walk_right
        ]
        self.walk_down  = slice_row(self.sheet, 0, 9, self.frame_height)
        self.walk_up    = [
            pygame.transform.flip(f, False, True) for f in self.walk_down
        ]

        
        self.current_animation = self.walk_down
        self.frame_index       = 0.0
        self.animation_speed   = 10           # frames per second
        self.image             = self.current_animation[0]

       
        self.rect = self.image.get_rect(topleft=(x, y))

        # Float position for smooth sub-pixel movement
        self.pos_x = float(x)
        self.pos_y = float(y)

    
    def update(self, dt, world):
        keys   = pygame.key.get_pressed()
        moving = False

        
        if keys[pygame.K_i]:
            self.pos_y -= PLAYER_SPEED * dt
            self._set_anim(self.walk_up)
            moving = True

        elif keys[pygame.K_k]:
            self.pos_y += PLAYER_SPEED * dt
            self._set_anim(self.walk_down)
            moving = True

        if keys[pygame.K_j]:
            self.pos_x -= PLAYER_SPEED * dt
            if not moving:
                self._set_anim(self.walk_left)
            moving = True

        elif keys[pygame.K_l]:
            self.pos_x += PLAYER_SPEED * dt
            if not moving:
                self._set_anim(self.walk_right)
            moving = True

        
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

        
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0.0
            self.image = self.current_animation[int(self.frame_index)]
        else:
            
            self.frame_index = 0.0
            self.image = self.current_animation[0]

    
    def _set_anim(self, anim):
        """Switch animation row without resetting frame if already playing it."""
        if anim is not self.current_animation:
            self.current_animation = anim
            self.frame_index = 0.0

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)