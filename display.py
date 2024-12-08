import pygame

TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW_COLOR = (0, 0, 0)

def load_health_bar_assets():
    """Load the health bar background image."""
    health_bar_base = pygame.image.load("assets/health_bar_background.png")
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
    return pygame.font.Font("assets/8bit_font.ttf", 20)  # Adjust font size as needed

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
