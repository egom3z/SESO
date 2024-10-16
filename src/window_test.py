import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 30)

# direction class
class direction(Enum):
    STOP = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

forward_facing = True  # last direction faced
current_direction = direction.STOP

# Defining colors for convenience
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the game window
screen_width = 1280
screen_height = 720
center_x = screen_width // 2
center_y = screen_height // 2
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Box (platform) object definition
box_rect = pygame.Rect(center_x + 150, center_y - 84, 100, 100)
box_border = 5

# Ground level
ground_level = center_y

# Set up the sprite sheets
<<<<<<< HEAD
sprite_sheet = pygame.image.load('images/character_sheet2.png').convert_alpha()
sprite0_rect = pygame.Rect(16, 96, 16, 16)  # Character standing facing right
sprite1_rect = pygame.Rect(64, 96, 16, 16)  # Character standing facing left
spriteR_rect = pygame.Rect(32, 96, 16, 16)  # Character walking to the right
spriteL_rect = pygame.Rect(0, 96, 16, 16)  # Character walking to the left
spriteJ_rect = pygame.Rect(16, 80, 16, 16)  # Character jumping up facing right
spriteJL_rect = pygame.Rect(0, 80, 16, 16)  # Character jumping up facing left
=======
sprite_sheet = pygame.image.load('src/images/character_sheet2.png').convert_alpha()
sprite0_rect = pygame.Rect(16,96,16,16) # Character standing facing right
sprite1_rect = pygame.Rect(64,96,16,16)  # Character standing facing left
spriteR_rect = pygame.Rect(32,96,16,16) # Character walking to the right
spriteL_rect = pygame.Rect(0,96,16,16)  # Character walking to the left
spriteJ_rect = pygame.Rect(16,80,16,16) # Character jumping up facing right
spriteJL_rect = pygame.Rect(0,80,16,16) # Character jumping up facing left
>>>>>>> c6281ca742ffea3831a5846aed2e8f2fa25279a2
sprite0 = sprite_sheet.subsurface(sprite0_rect)
sprite1 = sprite_sheet.subsurface(sprite1_rect)
spriteR = sprite_sheet.subsurface(spriteR_rect)
spriteL = sprite_sheet.subsurface(spriteL_rect)
spriteJ = sprite_sheet.subsurface(spriteJ_rect)
spriteJL = sprite_sheet.subsurface(spriteJL_rect)

scaled_sprite0 = pygame.transform.scale(sprite0, (32, 32))
scaled_sprite1 = pygame.transform.scale(sprite1, (32, 32))
scaled_spriteR = pygame.transform.scale(spriteR, (32, 32))
scaled_spriteL = pygame.transform.scale(spriteL, (32, 32))
scaled_spriteJ = pygame.transform.scale(spriteJ, (32, 32))
scaled_spriteJL = pygame.transform.scale(spriteJL, (32, 32))

# Movement parameters
Y_GRAVITY = 3
JUMP_HEIGHT = 35
Y_VELOCITY = 0
jumping = False
falling = False
walking = False
on_ground = True
on_platform = False
MAX_VELOCITY = 10
X_VELOCITY = 0

# Vector2: 2D Vector (x, y) for character
player_pos = pygame.Vector2(center_x, center_y)
dynamic_rect = pygame.Rect(player_pos.x - 16, player_pos.y - 16, 32, 32)

# Set window title
pygame.display.set_caption('My Pygame Window')

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (RGB)
    screen.fill(white)

    # Draw the box (platform)
    pygame.draw.rect(screen, black, box_rect, box_border)

    keys = pygame.key.get_pressed()

    # Apply horizontal movement
    if keys[pygame.K_a]:  # Moving left
        forward_facing = False
        walking = True
        X_VELOCITY = max(X_VELOCITY - 1, -MAX_VELOCITY)
    elif keys[pygame.K_d]:  # Moving right
        forward_facing = True
        walking = True
        X_VELOCITY = min(X_VELOCITY + 1, MAX_VELOCITY)
    else:
        walking = False
        X_VELOCITY = 0

    # Handle jumping
    if keys[pygame.K_SPACE] and (on_ground or on_platform):
        jumping = True
        Y_VELOCITY = JUMP_HEIGHT
        on_ground = False
        on_platform = False
        falling = False

    # Apply gravity when falling or jumping
    if jumping:
        player_pos.y -= Y_VELOCITY  # Move upward when jumping
        Y_VELOCITY -= Y_GRAVITY  # Apply gravity to reduce upward velocity
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            falling = True

    if falling:
        player_pos.y -= Y_VELOCITY  # Apply gravity when falling
        Y_VELOCITY -= Y_GRAVITY

    # Collision with platform
    if dynamic_rect.colliderect(box_rect):
        falling_on_top = falling and player_pos.y + dynamic_rect.height / 2 >= box_rect.top
        approaching_from_left = player_pos.x < box_rect.left and player_pos.x + dynamic_rect.width / 2 > box_rect.left
        approaching_from_right = player_pos.x > box_rect.right and player_pos.x - dynamic_rect.width / 2 < box_rect.right
        below_rectangle = player_pos.y + dynamic_rect.height / 2 > box_rect.top and player_pos.y < box_rect.bottom
        
        # Handle landing on top of the platform
        if falling_on_top:
            if not (approaching_from_left or approaching_from_right):
                player_pos.y = box_rect.top - dynamic_rect.height / 2  # Land on top of platform
                Y_VELOCITY = 0  # Stop vertical movement
                falling = False
                on_platform = True

        # Handle side collisions
        if below_rectangle:
            if approaching_from_left:
                player_pos.x = box_rect.left - dynamic_rect.width / 2  # Stop on the left side of the platform
                X_VELOCITY = 0
            elif approaching_from_right:
                player_pos.x = box_rect.right + dynamic_rect.width / 2  # Stop on the right side of the platform
                X_VELOCITY = 0

    # If moving off the platform horizontally, start falling
    if on_platform and (player_pos.x + dynamic_rect.width / 2 < box_rect.left or player_pos.x - dynamic_rect.width / 2 > box_rect.right):
        falling = True
        on_platform = False

    # Ground collision
    if player_pos.y >= ground_level:
        player_pos.y = ground_level  # Land on the ground
        Y_VELOCITY = 0  # Reset vertical velocity
        falling = False
        on_ground = True

    # Apply horizontal movement after jump/fall/ground check
    player_pos.x += X_VELOCITY
    dynamic_rect.topleft = (player_pos.x - 16, player_pos.y - 16)

    # Display character sprite
    if jumping or falling:
        if forward_facing:
            screen.blit(scaled_spriteJ, (player_pos.x - 16, player_pos.y - 16))
        else:
            screen.blit(scaled_spriteJL, (player_pos.x - 16, player_pos.y - 16))
    elif walking:
        if forward_facing:
            screen.blit(scaled_spriteR, (player_pos.x - 16, player_pos.y - 16))
        else:
            screen.blit(scaled_spriteL, (player_pos.x - 16, player_pos.y - 16))
    else:
        if forward_facing:
            screen.blit(scaled_sprite0, (player_pos.x - 16, player_pos.y - 16))
        else:
            screen.blit(scaled_sprite1, (player_pos.x - 16, player_pos.y - 16))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
