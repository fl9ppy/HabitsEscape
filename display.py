import pygame

TEXT_COLOR = (255, 255, 255)

def draw_obstacles(screen, obstacles):
    """Draw obstacles with their assigned dimensions and images."""
    for x, y, width, height, image in obstacles:
        screen.blit(pygame.transform.scale(image, (width, height)), (x, y))

def draw_enemies(screen, enemies, enemy_size, enemy_image):
    """Draw all enemies using the enemy image."""
    for enemy in enemies:
        screen.blit(enemy_image, (enemy["pos"][0], enemy["pos"][1]))

def display_room_count(screen, count, font):
    """Display the room count."""
    text = font.render(f"Rooms: {count}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

def display_high_score(screen, high_score, font):
    """Display the high score."""
    text = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))