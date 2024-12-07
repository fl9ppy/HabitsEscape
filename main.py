import pygame
from game_logic import (
    generate_building_obstacles,
    generate_door_position_on_edge,
    get_valid_starting_position,
    generate_enemy_positions,
    move_enemies_toward_player,
    ensure_path,
)
from display import draw_obstacles, draw_enemies, display_room_count, display_high_score

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLAYER_SIZE = 50  # Logical size for player (collision box)
ENEMY_SIZE = 40
TILE_SIZE = 100
DOOR_SIZE = 100
SPACING = 120
OBSTACLE_COUNT = 25
EDGE_BUFFER = 100
ENEMY_COUNT = 5
PLAYER_HEALTH = 100
ROOM_COUNT_FILE = "room_count.txt"
DAMAGE_COOLDOWN = 1000  # 1000 milliseconds (1 second)
HEALTH_COLOR = (255, 255, 255)

def load_high_score(file_path):
    """Load only the high score from the file."""
    try:
        with open(file_path, "r") as file:
            data = file.read().strip().split()
            high_score = int(data[1]) if len(data) > 1 else 0
            return high_score
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(file_path, high_score):
    """Save only the high score to the file."""
    with open(file_path, "w") as file:
        file.write(f"0 {high_score}")  # Room count resets to 0, but high score persists

def display_health(screen, health, font):
    """Display the player's health on the screen."""
    health_text = font.render(f"Health: {health}", True, HEALTH_COLOR)
    screen.blit(health_text, (10, 50))  # Moved down to avoid overlap

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Room Counter Game")
    font = pygame.font.Font(None, 36)

    # Load images
    background_image = pygame.image.load("assets/background.jpg")
    player_image = pygame.image.load("assets/ford.png")
    enemy_image = pygame.image.load("assets/beer.png")
    door_image = pygame.image.load("assets/cigs.png")
    building_image = pygame.image.load("assets/building1.png")

    # Scale images
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Fit the window
    scaled_player_image = pygame.transform.scale(player_image, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))  # Larger player image
    enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))
    door_image = pygame.transform.scale(door_image, (DOOR_SIZE, DOOR_SIZE))
    building_image = pygame.transform.scale(building_image, (TILE_SIZE, TILE_SIZE))

    # Reset the room count to 0 for this session
    room_count = 0

    # Load the high score from file
    high_score = load_high_score(ROOM_COUNT_FILE)

    clock = pygame.time.Clock()
    move_speed = 7
    running = True

    # Player health and damage cooldown
    player_health = PLAYER_HEALTH
    last_damage_time = 0

    # Generate initial layout
    obstacles = generate_building_obstacles(OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER)
    player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
    door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE)
    enemies = generate_enemy_positions(obstacles, ENEMY_COUNT, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
    obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        new_player_pos = player_pos[:]

        # Handle player movement
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            new_player_pos[0] -= move_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WINDOW_WIDTH - PLAYER_SIZE:
            new_player_pos[0] += move_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            new_player_pos[1] -= move_speed
        if keys[pygame.K_DOWN] and player_pos[1] < WINDOW_HEIGHT - PLAYER_SIZE:
            new_player_pos[1] += move_speed

        player_rect = pygame.Rect(*new_player_pos, PLAYER_SIZE, PLAYER_SIZE)
        if not player_rect.collidelist([pygame.Rect(*obstacle, TILE_SIZE, TILE_SIZE) for obstacle in obstacles]) != -1:
            player_pos = new_player_pos

        # Player attack logic
        is_attacking = keys[pygame.K_SPACE]
        if is_attacking:
            attack_range = pygame.Rect(
                player_pos[0] - 20, player_pos[1] - 20,
                PLAYER_SIZE + 40, PLAYER_SIZE + 40
            )
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(*enemy["pos"], ENEMY_SIZE, ENEMY_SIZE)
                if attack_range.colliderect(enemy_rect):
                    enemy["health"] -= 10
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)

        # Move enemies using A* pathfinding
        move_enemies_toward_player(
            enemies, player_pos, obstacles, TILE_SIZE, WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE
        )

        # Check for enemy collisions and apply damage
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            enemy_rect = pygame.Rect(*enemy["pos"], ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                if current_time - last_damage_time > DAMAGE_COOLDOWN:
                    player_health -= 10
                    last_damage_time = current_time

        # Check if the player touches the door
        door_rect = pygame.Rect(*door_pos, DOOR_SIZE, DOOR_SIZE)
        if player_rect.colliderect(door_rect) and not enemies:
            # Transport to a new room
            room_count += 1
            obstacles = generate_building_obstacles(OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER)
            player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
            door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE)
            enemies = generate_enemy_positions(obstacles, ENEMY_COUNT, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
            obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE)

        # Check for game over
        if player_health <= 0:
            print("Game Over!")
            running = False

        # Rendering
        screen.blit(background_image, (0, 0))  # Draw the background image
        draw_obstacles(screen, obstacles, building_image)  # Use images for buildings
        draw_enemies(screen, enemies, ENEMY_SIZE, enemy_image)  # Use images for enemies
        # Render the player (center the larger image on the logical hitbox)
        scaled_image_offset = (PLAYER_SIZE // 2)
        screen.blit(scaled_player_image, (player_pos[0] - scaled_image_offset, player_pos[1] - scaled_image_offset))
        if not enemies:
            screen.blit(door_image, (door_pos[0], door_pos[1]))  # Door image
        display_room_count(screen, room_count, font)
        display_high_score(screen, high_score, font)
        display_health(screen, player_health, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
