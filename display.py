import pygame

TEXT_COLOR = (255, 255, 255)

def draw_obstacles(screen, obstacles, tile_size):
    for x, y in obstacles:
        pygame.draw.rect(screen, (255, 255, 255), (x, y, tile_size, tile_size))

def display_room_count(screen, count, font):
    text = font.render(f"Rooms: {count}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

def display_high_score(screen, high_score, font):
    text = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))
