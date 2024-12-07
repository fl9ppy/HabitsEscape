import pygame

TEXT_COLOR = (255, 255, 255)

def draw_obstacles(screen, obstacles, tile_size):
    """Draw obstacles."""
    for x, y in obstacles:
        pygame.draw.rect(screen, (255, 255, 255), (x, y, tile_size, tile_size))

def draw_enemies(screen, enemies, enemy_size, color):
    """Draw all enemies on the screen."""
    for enemy in enemies:
        x, y = enemy["pos"]  # Access the position stored in the "pos" field
        pygame.draw.rect(screen, color, (x, y, enemy_size, enemy_size))

def display_room_count(screen, count, font):
    """Display the room count."""
    text = font.render(f"Rooms: {count}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

def display_high_score(screen, high_score, font):
    """Display the high score."""
    text = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))
