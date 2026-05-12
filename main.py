import pygame
from moviepy.editor import VideoFileClip
from engine.settings import *
from engine.player import Player
from engine.Ferb import Ferb
from engine.world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phineas & Ferb: Open World")

clock = pygame.time.Clock()

# -----------------------------
# GAME STATE
# -----------------------------
game_state = "start"

# -----------------------------
# LOAD MP4 VIDEO WITH MOVIEPY
# -----------------------------
clip = VideoFileClip("engine/assets/backgrounds/startbg.mp4")
clip = clip.resize((WIDTH, HEIGHT))  # scale to screen

video_time = 0  # track playback time
video_speed = 1  # normal speed


# -----------------------------
# GAME OBJECTS
# -----------------------------
player = Player(300, 200)
ferb = Ferb(400, 200)
world = World()


# -----------------------------
# START SCREEN FUNCTION
# -----------------------------
def draw_start_screen(screen, dt):
    global video_time

    # advance video time
    video_time += dt * video_speed
    if video_time >= clip.duration:
        video_time = 0  # loop video

    # get current frame
    frame = clip.get_frame(video_time)
    frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

    # draw video frame
    screen.blit(frame_surface, (0, 0))

    # draw centered text
    font_big = pygame.font.Font(None, 70)
    font_small = pygame.font.Font(None, 35)

    title = font_big.render("Phineas & Ferb: Open World", True, (255, 255, 255))
    prompt = font_small.render("Press SPACE to Start", True, (230, 230, 230))

    screen_rect = screen.get_rect()

    title_rect = title.get_rect(center=(screen_rect.centerx, screen_rect.centery - 120))
    prompt_rect = prompt.get_rect(center=(screen_rect.centerx, screen_rect.centery + 40))

    screen.blit(title, title_rect)
    screen.blit(prompt, prompt_rect)


# -----------------------------
# MAIN LOOP
# -----------------------------
running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------------------
    # START SCREEN
    # -----------------------------
    if game_state == "start":
        draw_start_screen(screen, dt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "playing"

    # -----------------------------
    # GAMEPLAY
    # -----------------------------
    elif game_state == "playing":
        player.update(dt, world)
        ferb.update(dt, world)

        world.draw(screen)
        player.draw(screen)
        ferb.draw(screen)

    pygame.display.flip()

pygame.quit()
