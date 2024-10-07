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

forward_facing = True # last direction faced

direction = Enum('direction', ['STOP', 'LEFT', 'RIGHT','UP','DOWN'])
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
box_rect = pygame.Rect(center_x + 150, center_y - 84, 100, 100)
box_border = 5



# Set up the sprite sheets
sprite_sheet = pygame.image.load('src/images/character_sheet2.png').convert_alpha()
sprite0_rect = pygame.Rect(16,96,16,16) # Character standing facing right
sprite1_rect = pygame.Rect(64,96,16,16)  # Character standing facing left
spriteR_rect = pygame.Rect(32,96,16,16) # Character walking to the right
spriteL_rect = pygame.Rect(0,96,16,16)  # Character walking to the left
spriteJ_rect = pygame.Rect(16,80,16,16) # Character jumping up facing right
spriteJL_rect = pygame.Rect(0,80,16,16) # Character jumping up facing left
sprite0 = sprite_sheet.subsurface(sprite0_rect)
sprite1 = sprite_sheet.subsurface(sprite1_rect)
spriteR = sprite_sheet.subsurface(spriteR_rect)
spriteL = sprite_sheet.subsurface(spriteL_rect)
spriteJ = sprite_sheet.subsurface(spriteJ_rect)
spriteJL = sprite_sheet.subsurface(spriteJL_rect)
scaled_sprite0 = pygame.transform.scale(sprite0, (32,32)) # Scales up 16x16 sprite
scaled_sprite1 = pygame.transform.scale(sprite1, (32,32))
scaled_spriteR = pygame.transform.scale(spriteR, (32,32))
scaled_spriteL = pygame.transform.scale(spriteL, (32,32))
scaled_spriteJ = pygame.transform.scale(spriteJ, (32,32))
scaled_spriteJL = pygame.transform.scale(spriteJL, (32,32))



# Movement parameters
Y_GRAVITY = 1
JUMP_HEIGHT = 15
Y_VELOCITY = JUMP_HEIGHT
jumping = False
falling = False
walking = False
MAX_VELOCITY = 10
MIN_VELOCITY = -10
X_VELOCITY = 1


# Vector2: 2D Vector (x, y) for character
player_pos = pygame.Vector2(center_x, center_y)
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
            # if Y_VELOCITY > 0:
            #     current_direction = direction.UP
            # elif Y_VELOCITY < 0:
            #     current_direction = direction.DOWN
    elif keys[pygame.K_a]: # moving left
        walking = keys[pygame.K_a]
        forward_facing = False
        current_direction = direction.LEFT
        X_VELOCITY -= 1
    elif keys[pygame.K_d]: # moving right
        forward_facing = True
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
        if X_VELOCITY == 0:
             current_direction = direction.UP
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT 

    falling = (Y_VELOCITY < 0)
    if falling: current_direction = direction.DOWN

    # Display character sprite
    if current_direction == direction.LEFT:
         screen.blit(scaled_spriteL, (player_pos.x - 16, player_pos.y - 16))
    elif current_direction == direction.RIGHT:
         screen.blit(scaled_spriteR, (player_pos.x - 16, player_pos.y - 16))
    elif current_direction == direction.UP:
        if forward_facing:
            screen.blit(scaled_spriteJ, (player_pos.x - 16, player_pos.y - 16))
        elif not forward_facing:
            screen.blit(scaled_spriteJL, (player_pos.x - 16, player_pos.y - 16))
    elif current_direction == direction.DOWN:
        if forward_facing:
            screen.blit(scaled_sprite0, (player_pos.x - 16, player_pos.y - 16)) # TO BE REPLACED WITH DOWN RIGHT SPRITE
        elif not forward_facing:
            screen.blit(scaled_sprite1, (player_pos.x - 16, player_pos.y - 16)) # TO BE REPLACED WITH DOWN LEFT SPRITE
    else:
        if forward_facing:
            screen.blit(scaled_sprite0, (player_pos.x - 16, player_pos.y - 16))
        elif not forward_facing:
            screen.blit(scaled_sprite1, (player_pos.x - 16, player_pos.y - 16))

    # Collision detection and response
    dynamic_rect.topleft = (player_pos.x - 16, player_pos.y - 16)
    collision_occured = dynamic_rect.colliderect(box_rect)

    if collision_occured:
        if current_direction == direction.RIGHT:
            # Prevent moving further into the box
            player_pos.x = box_rect.left - dynamic_rect.width / 2
            X_VELOCITY = 0
        if current_direction == direction.LEFT:
            player_pos.x = box_rect.right + dynamic_rect.width / 2
            X_VELOCITY = 0
        if current_direction == direction.UP:
            player_pos.y = box_rect.bottom + dynamic_rect.height / 2
            Y_VELOCITY = 0
            jumping = True
        if current_direction == direction.DOWN:
            player_pos.y = box_rect.top - dynamic_rect.height / 2
            Y_VELOCITY = 0
            jumping = False

    
    if collision_occured: print("Collision!")
    else: print("No Collision!")

    # Update the display
    pygame.display.flip()
    # pygame.display.update() # Alternate option to the same function (I think)
    
    clock.tick(60)  # limits FPS to 60
    
# Quit Pygame
pygame.quit()
sys.exit()
