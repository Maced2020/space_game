import pygame

# Initialize Pygame
pygame.init()

# Set the initial dimensions of the game window
window_width = 800
window_height = 1200
game_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

# Set the title of the window
pygame.display.set_caption("Space Shooter")

# Load the background image
background_image = pygame.image.load('E:\Tim\code\Shooter_game\space.jpeg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update the game window size when resized and scale the background
            window_width, window_height = event.w, event.h
            game_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            background_image = pygame.transform.scale(background_image, (window_width, window_height))

    # Draw the background image
    game_window.blit(background_image, (0, 0))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
