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
 
# Initialize player health
player_health = 100


# Load the player ship image
player_image = pygame.image.load('E:\Tim\code\Shooter_game\enemies\Player_ship.jpg').convert_alpha()
player_rect = player_image.get_rect(center=(window_width // 2, window_height - 50))

# Player movement variables
player_speed = 7.5
move_left = move_right = move_up = move_down = False

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load enemy images into a list
enemy_images = []
enemy_folder_path = 'E:\\Tim\\code\\Shooter_game\\enemies'  # Note the double backslashes for Windows paths
print(f"Loading enemy images from: {enemy_folder_path}")

enemy_images = []  # Make sure this is initialized before the loop

for filename in os.listdir(enemy_folder_path):
    full_path = os.path.join(enemy_folder_path, filename)
    if filename.endswith('.png'):  # Assuming your enemy images are .png
        print(f"Loading: {filename}")
        try:
            enemy_image = pygame.image.load(full_path).convert_alpha()
            enemy_images.append(enemy_image)
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
    else:
        print(f"Skipping: {filename} (not a .png file)")

print(f"Loaded {len(enemy_images)} enemy images.")


# List to keep track of enemy instances
enemies = []


# Function to create a new enemy with a random image and position
def create_enemy():
    image = random.choice(enemy_images)
    # Enemy starts at a random x position, just above the screen
    rect = image.get_rect(center=(random.randint(0, window_width), -50))
    speed_y = random.randint(2, 5)  # Vertical speed
    speed_x = random.choice([-3, -2, -1, 1, 2, 3])  # Horizontal speed, can be negative or positive
    return {'image': image, 'rect': rect, 'speed_y': speed_y, 'speed_x': speed_x}


# Function to add enemies to the game
def add_enemy(interval, last_time):
    current_time = pygame.time.get_ticks()
    if current_time - last_time > interval:
        enemies.append(create_enemy())
        return current_time  # Update last spawn time
    return last_time  # Keep the last spawn time if no enemy is added

# Function to draw the HUD
def draw_hud():
    # Render the score and level text
    score_text = font.render(f'Score: {score}', True, WHITE)
    level_text = font.render(f'Level: {level}', True, WHITE)

    # Draw the score and level on the game window
    game_window.blit(score_text, (10, 10))
    game_window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

    # Health bar parameters
    health_bar_width = 200  # Maximum width of the health bar
    health_bar_height = 5
    health_bar_x = 10
    health_bar_y = 50  # Position the health bar a little below the score

    # Determine health bar color based on current health percentage
    health_percentage = player_health / 100
    if health_percentage > 0.65:
        health_bar_color = (0, 255, 0)  # Green
    elif health_percentage > 0.3:
        health_bar_color = (255, 255, 0)  # Yellow
    else:
        health_bar_color = (255, 0, 0)  # Red

    # Draw the health bar
    current_health_bar_width = health_percentage * 200  # Assuming 200 is the full width of the health bar
    pygame.draw.rect(game_window, health_bar_color, (10, 50, current_health_bar_width, 5))

    # Draw the health bar
    pygame.draw.rect(game_window, health_bar_color, (health_bar_x, health_bar_y, current_health_bar_width, health_bar_height))



# gameover screen
def show_game_over_screen():
    game_window.fill((0, 0, 0))  # Optional: Fill the screen with black or another color
    font = pygame.font.SysFont(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press any key to restart", True, (255, 255, 255))

    game_window.blit(game_over_text, (window_width / 2 - game_over_text.get_width() / 2, window_height / 2 - game_over_text.get_height()))
    game_window.blit(restart_text, (window_width / 2 - restart_text.get_width() / 2, window_height / 2 + restart_text.get_height()))

    pygame.display.update()
    wait_for_player_action()

def wait_for_player_action():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Example: Quit if the ESC key is pressed
                    pygame.quit()
                    exit()
                else:
                    return  # Any other key restarts the game





def main_game_loop():
    global game_window, background_image, move_left, move_right, move_up, move_down, window_width, window_height, player_health
    last_enemy_spawn_time = 0  # Initialize last_enemy_spawn_time before the loop
    enemy_spawn_interval = 1000  # Time in milliseconds
    running = True
    while running:
        clock.tick(60)  # Control the frame rate to be 60 FPS
                # Draw the background image
        game_window.blit(background_image, (0, 0))

        # Event handling and player movement updates
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



          # Call add_enemy function to spawn enemies
        last_enemy_spawn_time = add_enemy(enemy_spawn_interval, last_enemy_spawn_time)




        #bounces enemies off walls
        for enemy in list(enemies):
            enemy['rect'].y += enemy['speed_y']
            enemy['rect'].x += enemy['speed_x']
            
            # Check for collision with the player
            if player_rect.colliderect(enemy['rect']):
                player_health -= 10  # Decrease player health by 10 (adjust as needed)
                print(player_health)
                player_health = max(player_health, 0)  # Ensure health doesn't go below 0
                enemies.remove(enemy)  # Remove the enemy that collided with the player
            
            if enemy['rect'].y > window_height or enemy['rect'].right < 0 or enemy['rect'].left > window_width:
                enemies.remove(enemy)  # Remove the enemy if it goes off the bottom or sides of the screen
            else:
                game_window.blit(enemy['image'], enemy['rect'])
        
        if player_health <= 0:
            show_game_over_screen()
            player_health = 100  # Reset health for a new game


        # Draw the HUD
        draw_hud()

        # Draw the player ship
        game_window.blit(player_image, player_rect)


        draw_hud()
        # Update the display
        pygame.display.update()


# Call the main game loop function
main_game_loop()

# Quit Pygame
pygame.quit()