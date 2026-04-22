import pygame
from engine.settings import PLAYER_SPEED

# Slices a single row of the sprite sheet
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


class Player:
    def __init__(self, x, y):
        # Load sprite sheet
        self.sheet = pygame.image.load("assets/sprites/phineas.png").convert_alpha()

        # Your measured row height
        self.frame_height = 60

        # WALKING ANIMATIONS
        # Row 3 = walking right (12 frames)
        self.walk_right = slice_row(self.sheet, 2, 12, self.frame_height)

        # Walking left = flipped walking right
        self.walk_left = [pygame.transform.flip(frame, True, False) for frame in self.walk_right]

        # Placeholder walking down = first frame of Row 1
        self.walk_down = [slice_row(self.sheet, 0, 8, self.frame_height)[0]]

        # Placeholder walking up = flipped vertically
        self.walk_up = [pygame.transform.flip(self.walk_down[0], False, True)]

        # Animation state
        self.current_animation = self.walk_down
        self.frame_index = 0
        self.animation_speed = 12  # smooth animation
        self.image = self.current_animation[self.frame_index]

        # Position
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt, world):
        keys = pygame.key.get_pressed()
        moving = False

        # Movement + animation selection
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

        # Animate only when moving
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0
            self.image = self.current_animation[int(self.frame_index)]
        else:
            # Idle = first frame of current direction
            self.image = self.current_animation[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
