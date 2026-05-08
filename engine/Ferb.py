import pygame
import numpy as np
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


def remove_background(surface, sample_pos=(0, 0), tolerance=30):
    """Replace background pixels (similar color to sample_pos) with transparency."""
    surface = surface.copy()
    arr = pygame.surfarray.pixels3d(surface)
    alpha = pygame.surfarray.pixels_alpha(surface)

    target = arr[sample_pos[0], sample_pos[1]]  # sample bg color from corner

    diff = np.abs(arr.astype(int) - target.astype(int))
    mask = diff.max(axis=2) < tolerance

    alpha[mask] = 0  # make those pixels transparent

    del arr, alpha   # unlock surface
    return surface


class Ferb:
    def __init__(self, x, y):
        self.sheet = pygame.image.load(
            os.path.join("engine", "assets", "sprites", "Ferb.png")
        ).convert_alpha()

        # Remove blue background (top-left pixel is (33, 62, 118))
        self.sheet = remove_background(self.sheet, sample_pos=(0, 0), tolerance=30)

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
        self.animation_speed   = 10
        self.image             = self.current_animation[0]

        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)

    # ------------------------------------------------------------------
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

        # Sync rect to float position
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

        # --- Screen boundary ---
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(screen_rect)

        # Write clamped position back to floats so they don't drift past the wall
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        # --- Animate ---
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0.0
            self.image = self.current_animation[int(self.frame_index)]
        else:
            self.frame_index = 0.0
            self.image = self.current_animation[0]

    # ------------------------------------------------------------------
    def _set_anim(self, anim):
        if anim is not self.current_animation:
            self.current_animation = anim
            self.frame_index = 0.0

    # ------------------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.image, self.rect)