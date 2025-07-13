import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for sound

# Load background music and play it
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.3)  # adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Load images
mites_img = pygame.image.load("mites.png")
mites_img = pygame.transform.scale(mites_img, (60, 60))

bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (600, 700))

# Screen setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flying Mites")

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Clock
clock = pygame.time.Clock()

# mites settings
mites_x = 100
mites_y = HEIGHT // 2
mites_speed = 0
gravity = 0.5
flap_power = -8

# Pipe settings
pipe_width = 70
pipe_gap = 200
pipe_speed = 3
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 48)

def create_pipe():
    pipe_height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)
    return (top_pipe, bottom_pipe)

# Add initial pipes
pipes.append(create_pipe())

# Game state
game_over = False
running = True
game_started = False

# Scrolling background variables
bg_x = 0
bg_speed = 2

# Game loop
while running:
    clock.tick(60)

    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + WIDTH, 0))
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                elif not game_over:
                    mites_speed = flap_power

            if event.key == pygame.K_r and game_over:
                mites_y = HEIGHT // 2
                mites_speed = 0
                pipes.clear()
                pipes.append(create_pipe())
                score = 0
                game_over = False
                game_started = False

    if game_started and not game_over:
        mites_speed += gravity
        mites_y += mites_speed

        for pipe_pair in pipes:
            pipe_pair[0].x -= pipe_speed
            pipe_pair[1].x -= pipe_speed

        if pipes[-1][0].x < WIDTH - 300:
            pipes.append(create_pipe())

        if pipes[0][0].x + pipe_width < 0:
            pipes.pop(0)
            score += 1

        hitbox_padding = 5
        mites_rect = pygame.Rect(
            mites_x - mites_img.get_width() // 2 + hitbox_padding,
            mites_y - mites_img.get_height() // 2 + hitbox_padding,
            mites_img.get_width() - hitbox_padding * 2,
            mites_img.get_height() - hitbox_padding * 2,
        )

        for pipe_pair in pipes:
            if mites_rect.colliderect(pipe_pair[0]) or mites_rect.colliderect(pipe_pair[1]):
                game_over = True

        if mites_y - mites_img.get_height() // 2 < 0 or mites_y + mites_img.get_height() // 2 > HEIGHT:
            game_over = True

    for pipe_pair in pipes:
        pygame.draw.rect(screen, GRAY, pipe_pair[0])
        pygame.draw.rect(screen, GRAY, pipe_pair[1])

    screen.blit(mites_img, (mites_x - mites_img.get_width() // 2, int(mites_y) - mites_img.get_height() // 2))

    if game_started:
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

    if not game_started:
        title_text = font.render("Flying Mites", True, WHITE)
        instruction_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))

    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(over_text, (20, HEIGHT // 2 - 30))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
