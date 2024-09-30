import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

black = (0, 0, 0)
display_surface = pygame.display.set_mode((400, 400))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Diddy.", True, black)
text_rect = text.get_rect()
text_rect.center = (200, 200)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    display_surface.blit(text, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()