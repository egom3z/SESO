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

direction = Enum('direction', ['STOP', 'LEFT', 'RIGHT','UP'])
current_direction = direction.STOP


# Defining colors for conveniance
white = (255,255,255)
blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

# Set up the game window
screen_width = 1280 # Victor-circumference(cm)
screen_height = 720
window_size = (screen_width, screen_height)
center_x = screen_width // 2
center_y = screen_height // 2
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
seconds_elapsed = 0
last_time = pygame.time.get_ticks()

# Box object definition
box_rect = pygame.Rect(center_x+150, center_y-84, 100, 100)
box_border = 5



# Set up the sprite sheets
sprite_sheet = pygame.image.load('src/images/character_sheet2.png').convert_alpha()
sprite0_rect = pygame.Rect(16,96,16,16)
spriteR_rect = pygame.Rect(32,96,16,16)
spriteL_rect = pygame.Rect(0,96,16,16)
sprite0 = sprite_sheet.subsurface(sprite0_rect)
spriteR = sprite_sheet.subsurface(spriteR_rect)
spriteL = sprite_sheet.subsurface(spriteL_rect)
scaled_sprite0 = pygame.transform.scale(sprite0, (32,32))
scaled_spriteR = pygame.transform.scale(spriteR, (32,32))
scaled_spriteL = pygame.transform.scale(spriteL, (32,32))



# Movement parameters
Y_GRAVITY = 1
JUMP_HEIGHT = 15
Y_VELOCITY = JUMP_HEIGHT
jumping = False
walking = False
MAX_VELOCITY = 10
MIN_VELOCITY = -10
X_VELOCITY = 1


# Vector2: 2D Vector (x, y) for character
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
dynamic_rect = pygame.Rect(player_pos.x - 16, player_pos.y - 16, 32, 32)



# Set window title
pygame.display.set_caption('My Pygame Window')

# Game loop
running = True
while running:
    # Check for events (e.g., window close, key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the close button is clicked
            running = False
    
    # Fill the screen with a color (RGB)
    screen.fill(white) # background

    # Box object implementation
    pygame.draw.rect(screen, black, box_rect, box_border) 
    
    # Old player dot
    # pygame.draw.circle(screen, black, player_pos, 5)


        # Boundry Check
    if player_pos.x - 5 < 0:
         player_pos.x = 5
         X_VELOCITY = 0
    elif player_pos.x + 5 > screen_width:
         player_pos.x = screen_width - 5
         X_VELOCITY = 0
    if player_pos.y - 5 < 0:
         player_pos.y = 5
    elif player_pos.y + 5 > screen_height:
         player_pos.y = screen_height - 5
    if player_pos.x < 0:
        player_pos.x = 0
    elif player_pos.x > 1600:
         player_pos.x = 1600
    if player_pos.y < 0:
        player_pos.y = 0
    elif player_pos.y > 900:
         player_pos.y = 900


    # Keep track of time
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= 1000:
        seconds_elapsed += 1
        last_time = current_time
    
    keys = pygame.key.get_pressed()

    # Limits velocity to ensure control
    if(X_VELOCITY > MAX_VELOCITY):
            X_VELOCITY = 5
    if(X_VELOCITY < MIN_VELOCITY ):
            X_VELOCITY = -5


    # Post-input functions
    if keys[pygame.K_SPACE]:
            jumping = True
    elif keys[pygame.K_a]:
        walking = keys[pygame.K_a]
        current_direction = direction.LEFT
        X_VELOCITY -= 1
    elif keys[pygame.K_d]:
        walking = keys[pygame.K_d]
        current_direction = direction.RIGHT
        X_VELOCITY += 1
    elif not keys[pygame.K_d] and not keys[pygame.K_a]:
         current_direction = direction.STOP
         X_VELOCITY = 0
    
    
    # Walking mechanics
    if walking:
        player_pos.x += X_VELOCITY
        

    # Jumping mechanics
    if jumping:
        player_pos.y -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT     

    # Display character sprite
    if current_direction == direction.LEFT:
         screen.blit(scaled_spriteL, (player_pos.x - 16, player_pos.y - 16))
    elif current_direction == direction.RIGHT:
         screen.blit(scaled_spriteR, (player_pos.x - 16, player_pos.y - 16))
    else:
         screen.blit(scaled_sprite0, (player_pos.x - 16, player_pos.y - 16))

    # Collision management
    dynamic_rect.topleft = (player_pos.x - 16, player_pos.y - 16)
    if dynamic_rect.colliderect(box_rect):
        pygame.draw.rect(screen, red, box_rect)

    # Update the display
    pygame.display.flip()
    # pygame.display.update() # Alternate option to the same function (I think)
    
    clock.tick(60)  # limits FPS to 60
    

# Quit Pygame
pygame.quit()
sys.exit()
