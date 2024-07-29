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
background_image = pygame.image.load('Shooter_game/player/space.jpeg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Load the bullet image
bullet_image = pygame.image.load("Shooter_game/player/Bullet.jpg").convert_alpha()
enemy_bullet = pygame.image.load('Shooter_game/enemies/Enemy_bullet.jpg').convert_alpha()
bullet_speed = -10  # Negative value for moving up. Adjust the speed as needed.

cherry_image = pygame.image.load("Shooter_game/player/Cherry.jpg").convert_alpha()

cherries = []

# List to keep track of bullets
bullets = []
enemy_bullets = []
mini_boss_bullets = []
final_boss_bullets = []

# Mini-boss pictures
mini_boss1 = pygame.image.load("Shooter_game/enemies/mini_bosses/Mini_boss.png").convert_alpha()
mini_boss2 = pygame.image.load("Shooter_game/enemies/mini_bosses/Mini_boss_2.png").convert_alpha()
mini_boss3 = pygame.image.load("Shooter_game/enemies/mini_bosses/Mini_boss_3.png").convert_alpha()
mini_boss4 = pygame.image.load("Shooter_game/enemies/mini_bosses/Mini_boss_4.png").convert_alpha()

mini_boss_list = [mini_boss1, mini_boss2, mini_boss3, mini_boss4]

# Load the player ship image
player_image = pygame.image.load("Shooter_game/player/Player_ship.jpg").convert_alpha()
player_rect = player_image.get_rect(center=(window_width // 2, window_height - 50))

# Player movement variables
player_speed = 7.5
move_left = move_right = move_up = move_down = False

mini_boss_list_index = 0

def get_next_mini_boss():
    global mini_boss_list_index
    # Get the current mini-boss
    mini_boss_image = mini_boss_list[mini_boss_list_index]
    # Update the index to the next mini-boss
    mini_boss_list_index = (mini_boss_list_index + 1) % len(mini_boss_list)
    return mini_boss_image

mini_boss_image = get_next_mini_boss()

# Mini Boss attributes
mini_boss = {
    "image": mini_boss_image,
    "rect": mini_boss_image.get_rect(center=(window_width // 2, 100)),  # Starting position
    "health": 500,  # Example health value
    "speed": 2,  # Example speed, adjust based on your game's design
    "alive": False  # Track if the boss is currently in the game
}

# Mini Boss Health Bar attributes
mini_boss_health_bar_width = 200  # Adjust as needed
mini_boss_health_bar_height = 10  # Adjust as needed
mini_boss_health_bar_x = window_width // 2 - mini_boss_health_bar_width // 2
mini_boss_health_bar_y = 20  # Position above the mini boss or wherever fits best

# Final Boss
final_boss_image = pygame.image.load("Shooter_game/enemies/final_boss/final_boss.png").convert_alpha()

final_boss = {
    "image": final_boss_image,
    "rect": final_boss_image.get_rect(center=(window_width // 2, 100)),  # Starting position
    "health": 1000,  # Example health value
    "speed": 3,  # Example speed, adjust based on your game's design
    "alive": False  # Track if the boss is currently in the game
}

# Final Boss Health Bar attributes
final_boss_health_bar_width = 200  # Adjust as needed
final_boss_health_bar_height = 10  # Adjust as needed
final_boss_health_bar_x = window_width // 2 - mini_boss_health_bar_width // 2
final_boss_health_bar_y = 20  # Position above the mini boss or wherever fits best

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ROYAL_BLUE = (65, 105, 225)

# Set up the font for the HUD
font = pygame.font.SysFont(None, 36)

# Initialize score and level & player health
score = 0
level = 1
player_health = 100

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load enemy images into a list
enemy_images = []
enemy_folder_path = 'Shooter_game/enemies'  # Note the double backslashes for Windows paths

for filename in os.listdir(enemy_folder_path):
    full_path = os.path.join(enemy_folder_path, filename)
    if filename.endswith('.png'):  # Assuming your enemy images are .png
        try:
            enemy_image = pygame.image.load(full_path).convert_alpha()
            enemy_images.append(enemy_image)
        except Exception as e:
            print(f"Failed to load {filename}: {e}")

# List to keep track of enemy instances
enemies = []

def draw_final_boss_health_bar():
    global RED, GREEN
    # Draw background bar (full health)
    pygame.draw.rect(game_window, RED, (final_boss_health_bar_x, final_boss_health_bar_y, final_boss_health_bar_width, final_boss_health_bar_height))

    # Calculate current health bar width based on mini boss's health
    current_health_bar_width = (final_boss["health"] / 1000) * final_boss_health_bar_width  # Assuming 1000 is max health

    # Draw foreground bar (current health)
    pygame.draw.rect(game_window, GREEN, (final_boss_health_bar_x, final_boss_health_bar_y, current_health_bar_width, final_boss_health_bar_height))

def draw_mini_boss_health_bar():
    global RED, GREEN
    # Draw background bar (full health)
    pygame.draw.rect(game_window, RED, (mini_boss_health_bar_x, mini_boss_health_bar_y, mini_boss_health_bar_width, mini_boss_health_bar_height))

    # Calculate current health bar width based on mini boss's health
    current_health_bar_width = (mini_boss["health"] / 500) * mini_boss_health_bar_width  # Assuming 500 is max health

    # Draw foreground bar (current health)
    pygame.draw.rect(game_window, GREEN, (mini_boss_health_bar_x, mini_boss_health_bar_y, current_health_bar_width, mini_boss_health_bar_height))

def mini_boss_shoot():
    if mini_boss["alive"]:
        # Define the starting positions of the bullets relative to the mini boss
        bullet1_pos = (mini_boss["rect"].centerx - 20, mini_boss["rect"].bottom)
        bullet2_pos = (mini_boss["rect"].centerx + 20, mini_boss["rect"].bottom)
        
        # Create bullets with their positions and speeds
        random_bullet_speed_one = random.randint(10, 25)
        random_bullet_speed_two = random.randint(10, 25)
        mini_boss_bullets.append({"rect": pygame.Rect(bullet1_pos[0], bullet1_pos[1], 10, 20), "speed": random_bullet_speed_one})
        mini_boss_bullets.append({"rect": pygame.Rect(bullet2_pos[0], bullet2_pos[1], 10, 20), "speed": random_bullet_speed_two})

def final_boss_shoot():
    if final_boss["alive"]:
        # Define the starting positions of the bullets relative to the mini boss
        bullet1_pos = (final_boss["rect"].centerx - 20, final_boss["rect"].bottom)
        bullet2_pos = (final_boss["rect"].centerx + 20, final_boss["rect"].bottom)
        
        # Create bullets with their positions and speeds
        random_bullet_speed_one = random.randint(10, 25)
        random_bullet_speed_two = random.randint(10, 25)
        final_boss_bullets.append({"rect": pygame.Rect(bullet1_pos[0], bullet1_pos[1], 10, 20), "speed": random_bullet_speed_one})
        final_boss_bullets.append({"rect": pygame.Rect(bullet2_pos[0], bullet2_pos[1], 10, 20), "speed": random_bullet_speed_two})

def create_enemy():
    base_speed_y = 2  # Base vertical speed
    speed_increase_per_level = 0.5  # Increase speed by 0.5 for each level
    speed_y = base_speed_y + (level - 1) * speed_increase_per_level
    
    # Horizontal speed adjustment remains the same or can also be level-dependent
    speed_x = random.choice([-3, -2, -1, 1, 2, 3])
    
    image = random.choice(enemy_images)
    rect = image.get_rect(center=(random.randint(0, window_width), -50))
    
    return {'image': image, 'rect': rect, 'speed_y': speed_y, 'speed_x': speed_x}

def spawn_cherry():
    rect = cherry_image.get_rect(center=(random.randint(0, window_width), -50))
    cherries.append({'rect': rect, 'speed': 2})  # Adjust speed as needed

def shoot():
    bullet_rect = bullet_image.get_rect(center=(player_rect.centerx, player_rect.top))
    bullets.append({'rect': bullet_rect, 'speed': bullet_speed})

def enemy_shoot(enemy_rect):
    bullet_rect = enemy_bullet.get_rect(center=(enemy_rect.centerx, enemy_rect.bottom))
    enemy_bullets.append({'rect': bullet_rect, 'speed': 10})  # Positive speed for moving down

def add_enemy(interval, last_time):
    if not mini_boss['alive']:  # Only spawn enemies if the mini boss is not alive
        current_time = pygame.time.get_ticks()
        if current_time - last_time > interval:
            enemies.append(create_enemy())
            return current_time
    return last_time

def draw_hud():
    global YELLOW, GREEN, RED, WHITE
    # Render the score and level text
    score_text = font.render(f'Score: {score}', True, WHITE)
    level_text = font.render(f'Level: {level}', True, WHITE)

    # Draw the score and level on the game window
    game_window.blit(score_text, (10, 10))
    game_window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

    # Health bar parameters
    health_bar_height = 5
    health_bar_x = 10
    health_bar_y = 50  # Position the health bar a little below the score

    # Determine health bar color based on current health percentage
    health_percentage = player_health / 100
    if health_percentage > 0.65:
        health_bar_color = GREEN  # Green
    elif health_percentage > 0.3:
        health_bar_color = YELLOW  # Yellow
    else:
        health_bar_color = RED  # Red

    # Draw the health bar
    current_health_bar_width = health_percentage * 200  # Assuming 200 is the full width of the health bar
    pygame.draw.rect(game_window, health_bar_color, (10, 50, current_health_bar_width, 5))

    # Draw the health bar
    pygame.draw.rect(game_window, health_bar_color, (health_bar_x, health_bar_y, current_health_bar_width, health_bar_height))

def show_game_over_screen():
    # Show the game over screen and wait for player action
    global level, score, player_health, player_rect, RED, WHITE, BLACK
    game_window.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    game_over_text = font.render("Game Over", True, RED)
    restart_text = font.render("Press any key to restart", True, WHITE)
    game_window.blit(game_over_text, (window_width / 2 - game_over_text.get_width() / 2, window_height / 2 - game_over_text.get_height()))
    game_window.blit(restart_text, (window_width / 2 - restart_text.get_width() / 2, window_height / 2 + restart_text.get_height()))
    player_rect = player_image.get_rect(center=(window_width // 2, window_height - 50))
    pygame.display.update()
    pygame.time.delay(1900)  # Short delay to prevent immediate restart

def show_game_finished_screen():
    # Show the game over screen and wait for player action
    global level, score, player_health, player_rect, RED, WHITE, BLACK, ROYAL_BLUE
    game_window.fill(ROYAL_BLUE)
    font = pygame.font.SysFont(None, 74)
    game_finished_text = font.render("YOU HAVE BEAT THE GAME!", True, WHITE)
    game_window.blit(game_finished_text, (window_width / 2 - game_finished_text.get_width() / 2, window_height / 2 - game_finished_text.get_height()))
    player_rect = player_image.get_rect(center=(window_width // 2, window_height - 50))
    pygame.display.update()
    pygame.time.delay(3500)  # Short delay to prevent immediate restart

def restart_game():
    global score, player_health, enemies, cherries, level
    global move_left, move_right, move_up, move_down
    move_left = move_right = move_up = move_down = False
    
    score = 0
    player_health = 100
    enemies.clear()
    cherries.clear()
    
    level = 1  # Reset level to 1
    mini_boss["alive"] = False  # Reset mini boss to not being alive
    final_boss["alive"] = False # Reset final boss to not being alive. 

def wait_for_player_action():
    # This function waits for the player to press any key to restart the game
     waiting = True
     while waiting:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
             if event.type == pygame.KEYDOWN:
                 restart_game()  # Reset game state before restarting
                 return  # Exit this function to proceed to restart the game

def show_title_screen():
    global WHITE, BLACK
    title_font = pygame.font.SysFont(None, 96)
    instruction_font = pygame.font.SysFont(None, 36)

    title_text = title_font.render("Space Shooter", True, WHITE)
    instruction_text = instruction_font.render("Press any key to start", True, WHITE)

    while True:
        game_window.fill(BLACK)  # Fill the screen with black
        game_window.blit(title_text, (window_width / 2 - title_text.get_width() / 2, window_height / 3))
        game_window.blit(instruction_text, (window_width / 2 - instruction_text.get_width() / 2, window_height / 2))

        pygame.display.update()

        # Wait for player action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return  # Exit the function and proceed to the game

def show_mini_boss_defeat_screen():
    global WHITE, BLACK, mini_boss_image
    game_window.fill(BLACK)  # Fill the screen with black or another background color
    font = pygame.font.SysFont(None, 74)  # Adjust the font size as needed
    level_up_text = font.render(f"Mini Boss DEFEATED!", True, WHITE)
    continue_text = font.render("Continue...", True, WHITE)
    mini_boss_image = get_next_mini_boss()  # Update the mini_boss_image
    
    # Position the text in the center of the screen
    text_rect = level_up_text.get_rect(center=(window_width / 2, window_height / 2 - 50))
    continue_text_rect = continue_text.get_rect(center=(window_width / 2, window_height / 2 + 50))
    
    game_window.blit(level_up_text, text_rect)
    game_window.blit(continue_text, continue_text_rect)
    
    pygame.display.update()  # Update the display to show the text
    
    # Pause the game for a few seconds
    pygame.time.delay(2000)  # 3000 milliseconds = 3 seconds

def show_mini_boss_start_screen():
    global WHITE, BLACK, mini_boss_image, mini_boss
    game_window.fill(BLACK)  # Fill the screen with black or another background color
    font = pygame.font.SysFont(None, 74)  # Adjust the font size as needed
    level_up_text = font.render(f"Mini Boss activated!", True, WHITE)
    mini_boss["image"] = mini_boss_image
    mini_boss["rect"] = mini_boss_image.get_rect(center=(window_width // 2, 100))
    continue_text = font.render("Continue...", True, WHITE)
    
    # Position the text in the center of the screen
    text_rect = level_up_text.get_rect(center=(window_width / 2, window_height / 2 - 50))
    continue_text_rect = continue_text.get_rect(center=(window_width / 2, window_height / 2 + 50))
    
    game_window.blit(level_up_text, text_rect)
    game_window.blit(continue_text, continue_text_rect)
    
    pygame.display.update()  # Update the display to show the text
    
    # Pause the game for a few seconds
    pygame.time.delay(3000)  # 3000 milliseconds = 3 seconds

def final_boss_activation_screen():
    global WHITE, BLACK
    game_window.fill(BLACK)  # Fill the screen with black or another background color
    font = pygame.font.SysFont(None, 74)  # Adjust the font size as needed
    level_up_text = font.render(f"FINAL BOSS!", True, WHITE)
    continue_text = font.render("Continue...", True, WHITE)
    
    # Position the text in the center of the screen
    text_rect = level_up_text.get_rect(center=(window_width / 2, window_height / 2 - 50))
    continue_text_rect = continue_text.get_rect(center=(window_width / 2, window_height / 2 + 50))
    
    game_window.blit(level_up_text, text_rect)
    game_window.blit(continue_text, continue_text_rect)
    
    pygame.display.update()  # Update the display to show the text
    
    # Pause the game for a few seconds
    pygame.time.delay(3000)  # 3000 milliseconds = 3 seconds

def main_game_loop():
    global game_window, background_image, move_left, move_right, move_up
    global move_down, window_width, window_height, player_health, score, level 
    global level_text, mini_boss_list, mini_boss_image, RED, GREEN
    last_enemy_spawn_time = 0  # Initialize last_enemy_spawn_time before the loop
    enemy_spawn_interval = 750  # Time in milliseconds
    enemy_shoot_interval = 1200  # Milliseconds
    mini_boss_shoot_interval = 1200  # Milliseconds between shots
    final_boss_shoot_interval = 1000
    last_mini_boss_shoot_time = pygame.time.get_ticks()  # Initialize the timer
    last_final_boss_shoot_time = pygame.time.get_ticks()  # Initialize the timer
    last_enemy_shoot_time = pygame.time.get_ticks()
    cherry_spawn_interval = random.randint(10000, 15000)  # milliseconds
    last_cherry_spawn_time = pygame.time.get_ticks()
    running = True
    while running:
        clock.tick(60)  # Control the frame rate to be 60 FPS
        game_window.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.w, event.h
                game_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                background_image = pygame.transform.scale(background_image, (window_width, window_height))
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot()

        for bullet in bullets[:]:  # Iterate over a copy of the bullets list
            bullet['rect'].y += bullet['speed']
            if bullet['rect'].bottom < 0:
                bullets.remove(bullet)
            else:
                bullet_hit = False  # Flag to track if the bullet hit an enemy
                for enemy in enemies[:]:  # Also iterate over a copy of the enemies list
                    if bullet['rect'].colliderect(enemy['rect']):
                        enemies.remove(enemy)
                        bullet_hit = True
                        score += random.randint(5, 15)  # Increase score by a random amount
                        break  # Exit the inner loop since the bullet hit an enemy
                if bullet_hit:
                    bullets.remove(bullet)  # Remove the bullet here, outside the inner loop
        for bullet in enemy_bullets[:]:  # Iterate over a copy of the list
            bullet['rect'].y += bullet['speed']
            if bullet['rect'].top > window_height:
                enemy_bullets.remove(bullet)
            elif player_rect.colliderect(bullet['rect']):
                player_health -= 10
                enemy_bullets.remove(bullet)
                game_window.fill(RED)
                pygame.display.update()
                pygame.time.delay(25) 
            else:
                game_window.blit(enemy_bullet, bullet['rect'])
        for cherry in cherries[:]:  # Iterate over a copy of the list
            cherry['rect'].y += cherry['speed']
            if cherry['rect'].top > window_height:
                cherries.remove(cherry)
            elif player_rect.colliderect(cherry['rect']):
                player_health += 10  # Increase health, adjust value as desired
                player_health = min(player_health, 100)  # Cap health at 100
                cherries.remove(cherry)
                game_window.fill(GREEN)
                pygame.display.update()
                pygame.time.delay(25) 
            else:
                game_window.blit(cherry_image, cherry['rect'])
        current_time = pygame.time.get_ticks()
        if current_time - last_cherry_spawn_time > cherry_spawn_interval:
            spawn_cherry()
            last_cherry_spawn_time = current_time
        if mini_boss["alive"] and current_time - last_mini_boss_shoot_time > mini_boss_shoot_interval:
            mini_boss_shoot()
            last_mini_boss_shoot_time = current_time
        if mini_boss["alive"] and player_rect.colliderect(mini_boss["rect"]):
            player_health -= 15
            game_window.fill(RED)
            pygame.display.update()
            pygame.time.delay(25)  # 25 milliseconds delay for the red flash visibility
        for bullet in mini_boss_bullets[:]:  # Use a copy of the list for safe removal
            bullet["rect"].y += bullet["speed"]
            if player_rect.colliderect(bullet["rect"]):
                player_health -= 15  # Example damage to player
                mini_boss_bullets.remove(bullet)  # Remove the bullet
                game_window.fill(RED)
                pygame.display.update()
                pygame.time.delay(25)  # Delay to allow the red flash to be visible
            elif bullet["rect"].top > window_height:
                mini_boss_bullets.remove(bullet)
            else:
                pygame.draw.rect(game_window, RED, bullet["rect"])  # Example bullet color
        if final_boss["alive"] and current_time - last_final_boss_shoot_time > final_boss_shoot_interval:
            final_boss_shoot()
            last_final_boss_shoot_time = current_time
        if final_boss["alive"] and player_rect.colliderect(final_boss["rect"]):
            player_health -= 20
            game_window.fill(RED)
            pygame.display.update()
            pygame.time.delay(25)  # 25 milliseconds delay for the red flash visibility
        for bullet in final_boss_bullets[:]:  # Use a copy of the list for safe removal
            bullet["rect"].y += bullet["speed"]
            if player_rect.colliderect(bullet["rect"]):
                player_health -= 15  # Example damage to player
                final_boss_bullets.remove(bullet)  # Remove the bullet
                game_window.fill(RED)
                pygame.display.update()
                pygame.time.delay(25)  # Delay to allow the red flash to be visible
            elif bullet["rect"].top > window_height:
                final_boss_bullets.remove(bullet)
            else:
                pygame.draw.rect(game_window, RED, bullet["rect"])  # Example bullet color
        if score >= 100 * level:
            level += 1
        if level > 15:
            show_game_finished_screen()
        if level == 15 and not final_boss["alive"]:
            enemies.clear()  # Clear other enemies
            bullets.clear()  # Optionally clear bullets
            final_boss["alive"] = True
            final_boss_activation_screen()
        if final_boss["alive"]:
            draw_final_boss_health_bar()
            if player_health <= 0:
                level -= 1
                score = 1299
                final_boss["alive"] = False
                enemies.clear()  # Clear other enemies
                bullets.clear()  # Optionally clear bullets
            final_boss["rect"].x += final_boss["speed"]
            if final_boss["rect"].left <= 0 or final_boss["rect"].right >= window_width:
                final_boss["speed"] = -final_boss["speed"]
            for bullet in bullets[:]:
                if final_boss["rect"].colliderect(bullet["rect"]):
                    final_boss["health"] -= 15  # mini boss damage
                    bullets.remove(bullet)
                    if final_boss["health"] <= 0:
                        final_boss["alive"] = False
                        level += 1
                        score += 100
                        final_boss["health"] = 1000
            game_window.blit(final_boss["image"], final_boss["rect"])
        if level % 3 == 0 and level < 13 and not mini_boss["alive"]:
            enemies.clear()  # Clear existing enemies
            bullets.clear()
            mini_boss_bullets.clear()
            mini_boss["alive"] = True  # Mark the mini boss as active
            show_mini_boss_start_screen()
        if mini_boss["alive"]:
            draw_mini_boss_health_bar()
            mini_boss["rect"].x += mini_boss["speed"]
            if mini_boss["rect"].left <= 0 or mini_boss["rect"].right >= window_width:
                mini_boss["speed"] = -mini_boss["speed"]
            for bullet in bullets[:]:
                if mini_boss["rect"].colliderect(bullet["rect"]):
                    mini_boss["health"] -= 15  # mini boss damage
                    bullets.remove(bullet)
                    if mini_boss["health"] <= 0:
                        mini_boss["alive"] = False
                        show_mini_boss_defeat_screen()
                        level += 1
                        score += 100
                        mini_boss["health"] = 500
            game_window.blit(mini_boss["image"], mini_boss["rect"])
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_shoot_time > enemy_shoot_interval:
            for enemy in enemies:
                enemy_shoot(enemy['rect'])
            last_enemy_shoot_time = current_time
        for bullet in bullets:
            game_window.blit(bullet_image, bullet['rect'])
        if move_left and player_rect.left > 0:
            player_rect.x -= player_speed
        if move_right and player_rect.right < window_width:
            player_rect.x += player_speed
        if move_up and player_rect.top > 0:
            player_rect.y -= player_speed
        if move_down and player_rect.bottom < window_height:
            player_rect.y += player_speed
        last_enemy_spawn_time = add_enemy(enemy_spawn_interval, last_enemy_spawn_time)
        for enemy in list(enemies):
            enemy['rect'].y += enemy['speed_y']
            enemy['rect'].x += enemy['speed_x']
            if player_rect.colliderect(enemy['rect']):
                player_health -= 10  # Decrease player health by 10 (adjust as needed)
                player_health = max(player_health, 0)  # Ensure health doesn't go below 0
                enemies.remove(enemy)  # Remove the enemy that collided with the player
                game_window.fill(RED)
                pygame.display.update()
                pygame.time.delay(25)  # Delay to allow the red flash to be visible
            if enemy['rect'].y > window_height or enemy['rect'].right < 0 or enemy['rect'].left > window_width:
                enemies.remove(enemy)  # Remove the enemy if it goes off the bottom or sides of the screen
            else:
                game_window.blit(enemy['image'], enemy['rect'])
        if player_health <= 0:
            show_game_over_screen()
            player_health = 100  # Reset health for a new game
        draw_hud()
        game_window.blit(player_image, player_rect)
        pygame.display.update()

show_title_screen()
main_game_loop()

def main():
    while True:
        show_title_screen()  # Show the title screen
        game_over = main_game_loop()  # Start the main game loop

        if game_over:
            should_restart = show_game_over_screen()
            if not should_restart:
                break  # Exit the loop and end the game if not restarting
        else:
            break  # If the game loop ended for reasons other than a game over, exit

if __name__ == "__main__":
    main()

# Quit Pygame
pygame.quit()
