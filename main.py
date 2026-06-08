import pygame
import random
import sys

pygame.init()

# -----------------------
# SETTINGS
# -----------------------

WIDTH = 500
HEIGHT = 700
FPS = 60

GRAVITY = 0.5
JUMP_STRENGTH = -9

PIPE_SPEED = 5
PIPE_WIDTH = 100
PIPE_HEIGHT = 400

GAP_SIZE = 180

# -----------------------
# WINDOW
# -----------------------

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("nakAA play")

clock = pygame.time.Clock()

# -----------------------
# FONTS
# -----------------------

title_font = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 40)

# -----------------------
# IMAGES
# -----------------------

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(
    bird_img,
    (60, 60)
)

pillar_img = pygame.image.load("pillar.png").convert_alpha()
pillar_img = pygame.transform.scale(
    pillar_img,
    (PIPE_WIDTH, PIPE_HEIGHT)
)

# -----------------------
# GAME VARIABLES
# -----------------------

bird_x = 120

game_state = "menu"


def reset_game():
    global bird_y
    global bird_velocity
    global pipe_x
    global gap_y
    global distance

    bird_y = HEIGHT // 2
    bird_velocity = 0

    pipe_x = WIDTH + 100

    gap_y = random.randint(
        220,
        HEIGHT - 220
    )

    distance = 0


reset_game()

# -----------------------
# MAIN LOOP
# -----------------------

while True:

    # -----------------------
    # EVENTS
    # -----------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":

                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "playing"

            elif game_state == "playing":

                if event.key == pygame.K_SPACE:
                    bird_velocity = JUMP_STRENGTH

            elif game_state == "gameover":

                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "menu"

    # -----------------------
    # UPDATE
    # -----------------------

    if game_state == "playing":

        bird_velocity += GRAVITY
        bird_y += bird_velocity

        pipe_x -= PIPE_SPEED

        distance += PIPE_SPEED

        if pipe_x < -PIPE_WIDTH:

            pipe_x = WIDTH

            gap_y = random.randint(
                220,
                HEIGHT - 220
            )

        bird_rect = bird_img.get_rect(
            center=(bird_x, bird_y)
        )

        top_rect = pygame.Rect(
            pipe_x,
            0,
            PIPE_WIDTH,
            gap_y - GAP_SIZE // 2
        )

        bottom_rect = pygame.Rect(
            pipe_x,
            gap_y + GAP_SIZE // 2,
            PIPE_WIDTH,
            HEIGHT
        )

        if (
            bird_rect.colliderect(top_rect)
            or bird_rect.colliderect(bottom_rect)
            or bird_y < 0
            or bird_y > HEIGHT
        ):
            game_state = "gameover"

    # -----------------------
    # DRAW BACKGROUND
    # -----------------------

    screen.blit(background, (0, 0))

    # -----------------------
    # MENU
    # -----------------------

    if game_state == "menu":

        title = title_font.render(
            "nakAA play",
            True,
            (255, 255, 255)
        )

        start = font.render(
            "Press SPACE to Start",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                250
            )
        )

        screen.blit(
            start,
            (
                WIDTH // 2 - start.get_width() // 2,
                330
            )
        )

    else:

        # -----------------------
        # PILLARS
        # -----------------------

        top_pillar = pygame.transform.flip(
            pillar_img,
            False,
            True
        )

        screen.blit(
            top_pillar,
            (
                pipe_x,
                gap_y - GAP_SIZE // 2 - PIPE_HEIGHT
            )
        )

        screen.blit(
            pillar_img,
            (
                pipe_x,
                gap_y + GAP_SIZE // 2
            )
        )

        # -----------------------
        # BIRD
        # -----------------------

        angle = max(
            -30,
            min(30, -bird_velocity * 3)
        )

        rotated_bird = pygame.transform.rotate(
            bird_img,
            angle
        )

        bird_rect_draw = rotated_bird.get_rect(
            center=(bird_x, bird_y)
        )

        screen.blit(
            rotated_bird,
            bird_rect_draw
        )

        # -----------------------
        # DISTANCE
        # -----------------------

        distance_text = font.render(
            f"Distance: {distance // 10} m",
            True,
            (255, 255, 255)
        )

        screen.blit(
            distance_text,
            (20, 20)
        )

    # -----------------------
    # GAME OVER
    # -----------------------

    if game_state == "gameover":

        over = title_font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        restart = font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        screen.blit(
            over,
            (
                WIDTH // 2 - over.get_width() // 2,
                260
            )
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                340
            )
        )

    pygame.display.update()
    clock.tick(FPS)