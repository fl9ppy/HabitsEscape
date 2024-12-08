import pygame
from game_logic import restart_game
import os

TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW_COLOR = (0, 0, 0)

def load_health_bar_assets():
    """Load the health bar background image."""
    health_bar_base = pygame.image.load("assets/others/health_bar_background.png")
    scaled_health_bar = pygame.transform.scale(health_bar_base, (280, 80))
    return scaled_health_bar

def display_health_bar(screen, health, max_health, health_bar_base, position, player_level):
    """Display the health bar with the red fill behind the bar."""
    # Calculate health percentage
    health_percentage = max(health / max_health, 0)  # Ensure no negative scaling

    # Get dimensions of the scaled health bar
    bar_width = health_bar_base.get_width() - 45
    bar_height = health_bar_base.get_height() - 25

    # Define padding and rectangle dimensions
    padding_x = 35  # Adjust as needed
    padding_y = 13  # Adjust as needed
    fill_width = int((bar_width * health_percentage) / player_level)  # Scale the red fill
    fill_height = bar_height  # Match the bar's height
    fill_position = (position[0] + padding_x, position[1] + padding_y)

    # Draw the red fill (health level)
    pygame.draw.rect(screen, (255, 0, 0), (fill_position[0], fill_position[1], fill_width, fill_height))

    # Draw the health bar background (overlay on top of the fill)
    screen.blit(health_bar_base, position)

def display_sign(screen, room_count, high_score, font, sign_image, position):
    """Display the wooden sign with room count and high score."""
    # Render the sign image
    screen.blit(sign_image, position)

    # Define text positions for the two planks
    plank1_center = (position[0] + 100, position[1] + 51)  # Adjust for first plank
    plank2_center = (position[0] + 95, position[1] + 90)  # Adjust for second plank

    # Render "LVL" and "PB" text
    lvl_text = font.render(f"LVL: {room_count}", True, (0, 0, 0))
    pb_text = font.render(f"PB: {high_score}", True, (0, 0, 0))

    # Center the text on each plank
    lvl_text_rect = lvl_text.get_rect(center=plank1_center)
    pb_text_rect = pb_text.get_rect(center=plank2_center)

    # Blit the text onto the screen
    screen.blit(lvl_text, lvl_text_rect)
    screen.blit(pb_text, pb_text_rect)

def load_font():
    """Load the 8-bit font."""
    return pygame.font.Font("assets/others/8bit_font.ttf", 20)  # Adjust font size as needed

def draw_obstacles(screen, obstacles):
    """Draw obstacles with their assigned dimensions and images."""
    for x, y, width, height, image in obstacles:
        screen.blit(pygame.transform.scale(image, (width, height)), (x, y))

def draw_enemies(screen, enemies, enemy_size, enemy_image):
    """Draw all enemies using the enemy image."""
    for enemy in enemies:
        screen.blit(enemy_image, (enemy["pos"][0], enemy["pos"][1]))

def render_text_with_shadow(screen, text, font, color, shadow_color, pos):
    """Render text with a shadow effect."""
    shadow = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, color)

    # Render shadow slightly offset
    screen.blit(shadow, (pos[0] + 2, pos[1] + 2))
    # Render main text
    screen.blit(text_surface, pos)

def display_room_count(screen, count, font):
    """Display the room count with a shadow."""
    render_text_with_shadow(screen, f"Rooms: {count}", font, TEXT_COLOR, TEXT_SHADOW_COLOR, (500, 10))  # Move to the right

def display_high_score(screen, high_score, font):
    """Display the high score with a shadow."""
    render_text_with_shadow(
        screen, f"High Score: {high_score}", font, TEXT_COLOR, TEXT_SHADOW_COLOR,
        (screen.get_width() - 200, 10)  # Adjust position
    )

def display_health(screen, health, font):
    """Display the player health with a shadow."""
    render_text_with_shadow(screen, f"Health: {health}", font, TEXT_COLOR, TEXT_SHADOW_COLOR, (10, 50))

def blur_surface(surface, amount):
    """Applies a blur effect to the given surface."""
    scale = max(1, int(amount))
    small_surface = pygame.transform.scale(surface,
                   (surface.get_width() // scale, surface.get_height() // scale))
    return pygame.transform.scale(small_surface, surface.get_size())



def show_death_screen(screen, font, sign_image, window_width, window_height, PLAYER_HEALTH, DOOR_SIZE, PLAYER_SIZE,
                      OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images,
                      ENEMY_COUNT, ENEMY_SIZE):
    """
    Displays the death screen and handles restart logic.
    """
    running = True
    clock = pygame.time.Clock()

    # Center the sign
    sign_rect = sign_image.get_rect(center=(window_width // 2, window_height // 2))

    # Calculate the button positions relative to the sign
    button_width = 150
    button_height = 50
    button_spacing = 20  # Space between buttons

    button1_rect = pygame.Rect(
        sign_rect.centerx - button_width // 2,
        sign_rect.bottom - button_height * 2 - 100,  # Positioned above the bottom edge
        button_width,
        button_height,
    )

    button2_rect = pygame.Rect(
        sign_rect.centerx - button_width // 2,
        sign_rect.bottom - button_height - 90,  # Just above the bottom edge
        button_width,
        button_height,
    )

    # Blur background
    blurred_bg = blur_surface(screen.copy(), 10)

    while running:
        # Render the blurred background
        screen.blit(blurred_bg, (0, 0))

        # Draw the sign
        screen.blit(sign_image, sign_rect.topleft)

        # Draw "Game Over" text
        game_over_text = font.render("GAME OVER", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(sign_rect.centerx, sign_rect.top + 30))
        screen.blit(game_over_text, game_over_rect)

        # Draw buttons
        pygame.draw.rect(screen, (255, 0, 0), button1_rect)  # Restart button
        pygame.draw.rect(screen, (0, 255, 0), button2_rect)  # Button 2

        # Draw button text
        button1_text = font.render("Restart", True, (255, 255, 255))
        button1_text_rect = button1_text.get_rect(center=button1_rect.center)
        screen.blit(button1_text, button1_text_rect)

        button2_text = font.render("Home", True, (255, 255, 255))
        button2_text_rect = button2_text.get_rect(center=button2_rect.center)
        screen.blit(button2_text, button2_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    # Call restart_game and get the updated state
                    updated_state = restart_game(
                        WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_HEALTH, DOOR_SIZE, PLAYER_SIZE,
                        OBSTACLE_COUNT, TILE_SIZE, SPACING, EDGE_BUFFER, ENEMY_COUNT, ENEMY_SIZE, building_images
                    )
                    return updated_state  # Return to main loop


                elif button2_rect.collidepoint(event.pos):
                    os.system("python home.py")
                    pygame.quit()
                    exit()

        clock.tick(30)

    # Once the loop exits, return control to the main game
    return

