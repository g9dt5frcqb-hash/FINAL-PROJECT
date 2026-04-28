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


class Player:
    def __init__(self, x, y):
        # --- Load sprite sheet ---
        self.sheet = pygame.image.load(
            os.path.join("engine", "assets", "sprites", "phineas.png")
        ).convert_alpha()

        # Height of each row in the sprite sheet (adjust if yours differs)
        self.frame_height = 60

        # --- Slice animation rows ---
        # Row 0 = walk down, Row 1 = walk up, Row 2 = walk right
        # Adjust frame_count to match your sheet's actual column count per row
        self.walk_down  = slice_row(self.sheet, 0, 8,  self.frame_height)
        self.walk_up    = slice_row(self.sheet, 1, 8,  self.frame_height)
        self.walk_right = slice_row(self.sheet, 2, 12, self.frame_height)
        self.walk_left  = [
            pygame.transform.flip(f, True, False) for f in self.walk_right
        ]

        # --- Animation state ---
        self.current_animation = self.walk_down
        self.frame_index       = 0.0          # float so dt-based stepping is smooth
        self.animation_speed   = 10           # frames per second (tweak to taste)
        self.image             = self.current_animation[0]

        # --- Position / collision rect ---
        self.rect = self.image.get_rect(topleft=(x, y))

        # Separate float position so sub-pixel movement accumulates correctly
        self.pos_x = float(x)
        self.pos_y = float(y)

    # ------------------------------------------------------------------
    def update(self, dt, world):
        keys   = pygame.key.get_pressed()
        moving = False

        # Pick direction — vertical keys take priority if both axes pressed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos_y -= PLAYER_SPEED * dt
            self._set_anim(self.walk_up)
            moving = True

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos_y += PLAYER_SPEED * dt
            self._set_anim(self.walk_down)
            moving = True

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos_x -= PLAYER_SPEED * dt
            if not moving:                    # only switch row anim if not already moving vertically
                self._set_anim(self.walk_left)
            moving = True

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += PLAYER_SPEED * dt
            if not moving:
                self._set_anim(self.walk_right)
            moving = True

        # Sync rect to float position
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

        # --- Animate ---
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0.0
            self.image = self.current_animation[int(self.frame_index)]
        else:
            # Idle: freeze on frame 0 of whichever direction we're facing
            self.frame_index = 0.0
            self.image = self.current_animation[0]

    # ------------------------------------------------------------------
    def _set_anim(self, anim):
        """Switch animation row without resetting frame if already playing it."""
        if anim is not self.current_animation:
            self.current_animation = anim
            self.frame_index = 0.0

    # ------------------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.image, self.rect)