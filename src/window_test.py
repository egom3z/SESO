import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 1600
window_height = 9004804
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)

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
    screen.fill((236, 175, 162))  # enrique-color background

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
