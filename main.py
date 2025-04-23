import pygame
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (255, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Color for hitbox

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 150, 240  # Increased size
MAX_SPEED = 10  # Maximum speed
ACCELERATION = MAX_SPEED / 0.15  # Adjusted acceleration for 0.15s startup
PUNCH_DAMAGE = 10
PUNCH_COOLDOWN = 2000  # Increased cooldown to 2 seconds
INPUT_COOLDOWN = 2000  # Cooldown for attack input
GRAVITY = 4  # Stronger gravity
JUMP_FORCE = -30  # Stronger jump
KNOCKBACK_FORCE = 25  # Increased knockback force
HITBOX_WIDTH = 50
HITBOX_HEIGHT = 50

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game")

# Load images
player1_img = pygame.image.load("assets/player1.png")
player2_img = pygame.image.load("assets/player2.png")
background_img = pygame.image.load("assets/background.png")

# Scale images
player1_img = pygame.transform.scale(player1_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
player2_img = pygame.transform.scale(player2_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Player positions
player1 = pygame.Rect(400, HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
player2 = pygame.Rect(1400, HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)

# Physics variables
player1_vel_y = 0
player2_vel_y = 0
player1_vel_x = 0
player2_vel_x = 0
player1_speed = 0
player2_speed = 0

# Health
player1_health = 100
player2_health = 100

# Attack cooldown timers
player1_last_punch = 0
player2_last_punch = 0
player1_last_input = 0
player2_last_input = 0

# Movement acceleration
player1_accel = 0
player2_accel = 0

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(30)
    screen.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # Player 1 movement
    if keys[pygame.K_a]:
        player1_accel = max(player1_accel - ACCELERATION, -MAX_SPEED)
    elif keys[pygame.K_d]:
        player1_accel = min(player1_accel + ACCELERATION, MAX_SPEED)
    else:
        player1_accel = 0
    player1.x += player1_accel

    # Player 2 movement
    if keys[pygame.K_LEFT]:
        player2_accel = max(player2_accel - ACCELERATION, -MAX_SPEED)
    elif keys[pygame.K_RIGHT]:
        player2_accel = min(player2_accel + ACCELERATION, MAX_SPEED)
    else:
        player2_accel = 0
    player2.x += player2_accel

    # Player 1 jump
    if keys[pygame.K_SPACE] and player1.y >= HEIGHT - PLAYER_HEIGHT - 100:
        player1_vel_y = JUMP_FORCE

    # Player 2 jump
    if keys[pygame.K_RETURN] and player2.y >= HEIGHT - PLAYER_HEIGHT - 100:
        player2_vel_y = JUMP_FORCE

    # Player 1 punch with input cooldown
    if keys[pygame.K_w] and current_time - player1_last_input > INPUT_COOLDOWN:
        player1_last_input = current_time
        if abs(player1.x - player2.x) < PLAYER_WIDTH and current_time - player1_last_punch > PUNCH_COOLDOWN:
            player2_health -= PUNCH_DAMAGE
            player2_vel_y = JUMP_FORCE  # Knockback effect
            if player1.x < player2.x:
                player2_vel_x = KNOCKBACK_FORCE  # Push player2 to the right
            else:
                player2_vel_x = -KNOCKBACK_FORCE  # Push player2 to the left
            player1_last_punch = current_time

    # Player 2 punch with input cooldown
    if keys[pygame.K_UP] and current_time - player2_last_input > INPUT_COOLDOWN:
        player2_last_input = current_time
        if abs(player1.x - player2.x) < PLAYER_WIDTH and current_time - player2_last_punch > PUNCH_COOLDOWN:
            player1_health -= PUNCH_DAMAGE
            player1_vel_y = JUMP_FORCE  # Knockback effect
            if player2.x < player1.x:
                player1_vel_x = KNOCKBACK_FORCE  # Push player1 to the right
            else:
                player1_vel_x = -KNOCKBACK_FORCE  # Push player1 to the left
            player2_last_punch = current_time

    # Apply gravity
    player1_vel_y += GRAVITY
    player2_vel_y += GRAVITY
    player1.y += player1_vel_y
    player2.y += player2_vel_y

    if player1.y >= HEIGHT - PLAYER_HEIGHT - 100:
        player1.y = HEIGHT - PLAYER_HEIGHT - 100
        player1_vel_y = 0

    if player2.y >= HEIGHT - PLAYER_HEIGHT - 100:
        player2.y = HEIGHT - PLAYER_HEIGHT - 100
        player2_vel_y = 0

    # Draw players
    screen.blit(player1_img, (player1.x, player1.y))
    screen.blit(player2_img, (player2.x, player2.y))

    # Draw health bars
    pygame.draw.rect(screen, RED, (50, 20, player1_health * 5, 20))
    pygame.draw.rect(screen, BLUE, (WIDTH - 550, 20, player2_health * 5, 20))

    # Check for game over
    if player1_health <= 0 or player2_health <= 0:
        running = False

    pygame.display.flip()

pygame.quit()
