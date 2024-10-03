import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 30)

# Defining colors for conveniance
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the game window
screen_width = 1280 # Jeshua size (1600 inches)
screen_height = 720
window_size = (screen_width, screen_height)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
seconds_elapsed = 0
last_time = pygame.time.get_ticks()

# Set up the sprite sheets
sprite_sheet = pygame.image.load('src/images/character_sheet2.png').convert_alpha()
sprite_rect = pygame.Rect(16, 96, 16, 16)
sprite1 = sprite_sheet.subsurface(sprite_rect)
scaled_sprite1 = pygame.transform.scale(sprite1, (32, 32))


center_x = screen_width // 2
center_y = screen_height // 2



# Movement parameters
Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT
jumping = False
walking = False
MAX_VELOCITY = 10
MIN_VELOCITY = -10
X_VELOCITY = 1


# Vector2: 2D Vector (x, y) for character
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)



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
    screen.fill((255, 255, 255)) # background
    
    # pygame.draw.circle(screen, black, player_pos, 5)



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

    if(X_VELOCITY > MAX_VELOCITY):
            X_VELOCITY = 10
    if(X_VELOCITY < MIN_VELOCITY ):
            X_VELOCITY = -10

    if keys[pygame.K_a]:
        walking = keys[pygame.K_a]
        X_VELOCITY -= 1
    if keys[pygame.K_d]:
        walking = keys[pygame.K_d]
        X_VELOCITY += 1
    if keys[pygame.K_SPACE]:
        jumping = True
    
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
         

    # Display sprite
    screen.blit(scaled_sprite1, (player_pos.x - 16, player_pos.y - 16))

    # Update the display
    pygame.display.flip()
    
    clock.tick(60)  # limits FPS to 60
    

# Quit Pygame
pygame.quit()
sys.exit()
