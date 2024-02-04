import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set the initial dimensions of the game window
window_width = 800
window_height = 1000
game_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

# Set the title of the window
pygame.display.set_caption("Space Shooter")

# Load the background image
background_image = pygame.image.load('E:\Tim\code\Shooter_game\space.jpeg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Define colors
WHITE = (255, 255, 255)

# Set up the font for the HUD
font = pygame.font.SysFont(None, 36)

# Initialize score and level
score = 0
level = 1

# Load the player ship image
player_image = pygame.image.load('E:\Tim\code\Shooter_game\Player_ship.jpeg').convert_alpha()
player_rect = player_image.get_rect(center=(window_width//2, window_height - 50))

# Player movement variables
player_speed = 7.5
move_left = move_right = move_up = move_down = False

# Create a clock object to control the frame rate
clock = pygame.time.Clock()


# Load enemy images into a list
enemy_images = []
enemy_folder_path = 'path_to_your_enemy_folder'  # Replace with your actual folder path you left off here making enimies in the enimies folder
for filename in os.listdir(enemy_folder_path):
    if filename.endswith('.png'):  # Assuming your enemy images are .png
        enemy_image = pygame.image.load(os.path.join(enemy_folder_path, filename)).convert_alpha()
        enemy_images.append(enemy_image)

# List to keep track of enemy instances
enemies = []

# Function to create a new enemy with a random image and position
def create_enemy():
    image = random.choice(enemy_images)
    rect = image.get_rect(center=(random.randint(0, window_width), -50))  # Start off-screen above the window
    speed = random.randint(2, 5)  # Random speed for each enemy
    return {'image': image, 'rect': rect, 'speed': speed}

# Function to add enemies to the game
def add_enemy(interval, last_time):
    current_time = pygame.time.get_ticks()
    if current_time - last_time > interval:
        enemies.append(create_enemy())
        return current_time
    return last_time



# Function to draw the HUD
def draw_hud():
    # Render the score and level text
    score_text = font.render(f'Score: {score}', True, WHITE)
    level_text = font.render(f'Level: {level}', True, WHITE)

    # Draw the score and level on the game window
    game_window.blit(score_text, (10, 10))
    game_window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

# Main game loop function
# Main game loop function
def main_game_loop():
    global game_window, background_image, move_left, move_right, move_up, move_down, window_width, window_height
    running = True
    while running:
        # Control the frame rate to be 60 FPS
        clock.tick(60)
        # Within your game loop
        last_enemy_spawn_time = 0
        enemy_spawn_interval = 1000  # Time in milliseconds

        last_enemy_spawn_time = add_enemy(enemy_spawn_interval, last_enemy_spawn_time)


                # Update and draw enemies
        for enemy in enemies:
            enemy['rect'].y += enemy['speed']  # Move the enemy down
            if enemy['rect'].y > window_height:
                enemies.remove(enemy)  # Remove the enemy if it has moved past the bottom of the screen
            else:
                game_window.blit(enemy['image'], enemy['rect'])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update the game window size when resized and scale the background
                window_width, window_height = event.w, event.h
                game_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                background_image = pygame.transform.scale(background_image, (window_width, window_height))
                # Reposition the HUD elements
                level_text = font.render(f'Level: {level}', True, WHITE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False

        # Update player position based on movement flags
        if move_left and player_rect.left > 0:
            player_rect.x -= player_speed
        if move_right and player_rect.right < window_width:
            player_rect.x += player_speed
        if move_up and player_rect.top > 0:
            player_rect.y -= player_speed
        if move_down and player_rect.bottom < window_height:
            player_rect.y += player_speed

        # Draw the background image
        game_window.blit(background_image, (0, 0))

        # Draw the HUD
        draw_hud()

        # Draw the player ship
        game_window.blit(player_image, player_rect)

        # Update the display
        pygame.display.update()

# Call the main game loop function
main_game_loop()

# Quit Pygame
pygame.quit()