import pygame
import numpy as np
import os
from engine.settings import PLAYER_SPEED


# ------------------------------------------------------------
# BACKGROUND REMOVAL
# ------------------------------------------------------------
def remove_background(surface, sample_pos=(0, 0), tolerance=30):
    """Replace background pixels (similar color to sample_pos) with transparency."""
    surface = surface.copy()
    arr = pygame.surfarray.pixels3d(surface)
    alpha = pygame.surfarray.pixels_alpha(surface)

    target = arr[sample_pos[0], sample_pos[1]]  # sample bg color from corner
    diff = np.abs(arr.astype(int) - target.astype(int))
    mask = diff.max(axis=2) < tolerance

    alpha[mask] = 0  # make those pixels transparent

    del arr, alpha
    return surface


# ------------------------------------------------------------
# SLICING HELPERS
# ------------------------------------------------------------
def slice_horizontal(sheet, row_index, frame_count, frame_height):
    """Slice frames arranged left→right."""
    frames = []
    sheet_width = sheet.get_width()
    frame_width = sheet_width // frame_count
    y = row_index * frame_height

    for i in range(frame_count):
        x = i * frame_width
        frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)

    return frames


def slice_vertical(sheet, col_index, frame_count, frame_width):
    """Slice frames arranged top→bottom."""
    frames = []
    sheet_height = sheet.get_height()
    frame_height = sheet_height // frame_count
    x = col_index * frame_width

    for i in range(frame_count):
        y = i * frame_height
        frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)

    return frames


# ------------------------------------------------------------
# PHINEAS CLASS
# ------------------------------------------------------------
class Player:
    def __init__(self, x, y):
        # Load sprite sheet
        self.sheet = pygame.image.load(
            os.path.join("engine", "assets", "sprites", "phineas.png")
        ).convert_alpha()

        # Remove background
        self.sheet = remove_background(self.sheet, sample_pos=(0, 0), tolerance=30)

        # ------------------------------------------------------------
        # AUTO-DETECT ORIENTATION
        # ------------------------------------------------------------
        sheet_w = self.sheet.get_width()
        sheet_h = self.sheet.get_height()

        frame_count = 12   # Phineas has 12 frames per animation
        rows = 3           # down, up, right

        if sheet_w > sheet_h:
            # Horizontal layout
            self.frame_height = sheet_h // rows
            self.frame_width = sheet_w // frame_count
            self.slice = slice_horizontal
            self.orientation = "horizontal"

        else:
            # Vertical layout (sideways)
            self.frame_width = sheet_w // rows
            self.frame_height = sheet_h // frame_count
            self.slice = slice_vertical
            self.orientation = "vertical"

        # ------------------------------------------------------------
        # SLICE ANIMATIONS
        # ------------------------------------------------------------
        if self.orientation == "horizontal":
            self.walk_down  = self.slice(self.sheet, 0, frame_count, self.frame_height)
            self.walk_up    = [pygame.transform.flip(f, False, True) for f in self.walk_down]
            self.walk_right = self.slice(self.sheet, 2, frame_count, self.frame_height)
            self.walk_left  = [pygame.transform.flip(f, True, False) for f in self.walk_right]

        else:  # vertical
            self.walk_down  = self.slice(self.sheet, 0, frame_count, self.frame_width)
            self.walk_up    = [pygame.transform.flip(f, False, True) for f in self.walk_down]
            self.walk_right = self.slice(self.sheet, 2, frame_count, self.frame_width)
            self.walk_left  = [pygame.transform.flip(f, True, False) for f in self.walk_right]

        # ------------------------------------------------------------
        # DEFAULT STATE
        # ------------------------------------------------------------
        self.current_animation = self.walk_down
        self.frame_index = 0.0
        self.animation_speed = 10
        self.image = self.current_animation[0]

        # Position
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos_x = float(x)
        self.pos_y = float(y)

    # ------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------
    def update(self, dt, world):
        keys = pygame.key.get_pressed()
        moving = False

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
            if not moving:
                self._set_anim(self.walk_left)
            moving = True

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos_x += PLAYER_SPEED * dt
            if not moving:
                self._set_anim(self.walk_right)
            moving = True

        # Sync rect
        self.rect.topleft = (int(self.pos_x), int(self.pos_y))

        # Clamp to screen
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(screen_rect)

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        # Animate
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0.0
            self.image = self.current_animation[int(self.frame_index)]
        else:
            self.frame_index = 0.0
            self.image = self.current_animation[0]

    # ------------------------------------------------------------
    def _set_anim(self, anim):
        if anim is not self.current_animation:
            self.current_animation = anim
            self.frame_index = 0.0

    # ------------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.image, self.rect)
