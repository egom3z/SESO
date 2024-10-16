import pygame
import sys
from enum import Enum

# direction class
class direction(Enum):
    STOP = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

def title_screen():
    # Set up fonts
    pygame.font.init()
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    
    # Load and play background music
    pygame.mixer.music.load('sounds/Memorabilia.mp3')
    pygame.mixer.music.play(-1)  # Play the music in an infinite loop (-1)

    # Set up the game window
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    
    title_text = font.render('Terraria', True, green)
    start_text = small_font.render('Press Enter to Start', True, white)
    quit_text = small_font.render('Press Q to Quit', True, white)
    
    while True:
        screen.fill(black)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Start game when Enter is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return  # Start the game by breaking out of the loop
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

def game_loop():
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
    sprite_sheet = pygame.image.load('images/character_sheet2.png').convert_alpha()
    sprite0_rect = pygame.Rect(16, 96, 16, 16)  # Character standing facing right
    sprite1_rect = pygame.Rect(64, 96, 16, 16)  # Character standing facing left
    spriteR_rect = pygame.Rect(32, 96, 16, 16)  # Character walking to the right
    spriteL_rect = pygame.Rect(0, 96, 16, 16)  # Character walking to the left
    spriteJ_rect = pygame.Rect(16, 80, 16, 16)  # Character jumping up facing right
    spriteJL_rect = pygame.Rect(0, 80, 16, 16)  # Character jumping up facing left
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
    MAX_VELOCITY = 4
    X_VELOCITY = 0

    # Jump cooldown parameters
    jump_cooldown_time = 500 # in milliseconds
    last_jump_time = 0 # Track the last time of the jump

    # Frame counter and animation parameters
    frame_count = 0
    animation_speed = 3  # Switch sprites every 3 frames

    # Vector2: 2D Vector (x, y) for character
    player_pos = pygame.Vector2(center_x, center_y)
    dynamic_rect = pygame.Rect(player_pos.x - 16, player_pos.y - 16, 32, 32)

    # Set window title
    pygame.display.set_caption('My Pygame Window')
    
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

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
        
        # Get the current time
        current_time = pygame.time.get_ticks()

        # Handle jumping
        if keys[pygame.K_SPACE] and (on_ground or on_platform) and (current_time - jump_cooldown_time >= last_jump_time):
            jumping = True
            Y_VELOCITY = JUMP_HEIGHT
            on_ground = False
            on_platform = False
            falling = False
            last_jump_time = current_time

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

        # Sprite animation logic
        frame_count += 1
        if walking and not jumping and not falling:
            # Alternate between the standing and walking sprites
            if frame_count // animation_speed % 2 == 0:
                current_sprite = scaled_spriteR if forward_facing else scaled_spriteL
            else:
                current_sprite = scaled_sprite0 if forward_facing else scaled_sprite1
        else:
            # Use the jumping sprite if jumping or falling
            if jumping or falling:
                current_sprite = scaled_spriteJ if forward_facing else scaled_spriteJL
            else:
                current_sprite = scaled_sprite0 if forward_facing else scaled_sprite1

        # Display character sprite
        screen.blit(current_sprite, (player_pos.x - 16, player_pos.y - 16))

        pygame.display.flip()
        clock.tick(60)
        
def main():
    # Initialize Pygame and Sound Mixer
    pygame.init()
    pygame.mixer.init()

    # Title and game loop
    title_screen()
    game_loop()
    
    # Quit game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()