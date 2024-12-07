import pygame
from game_logic import (
    generate_building_obstacles,
    generate_door_position_on_edge,
    get_valid_starting_position,
    check_collision_with_obstacles,
    ensure_path,
)
from display import draw_obstacles, display_room_count, display_high_score

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLAYER_SIZE = 50
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)
DOOR_COLOR = (0, 255, 0)
TILE_SIZE = 100
SPACING = 120
OBSTACLE_COUNT = 25
EDGE_BUFFER = 100
ROOM_COUNT_FILE = "room_count.txt"

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Room Counter Game")
    font = pygame.font.Font(None, 36)

    # Reset the room count to 0 for this session
    room_count = 0

    # Load the high score from file
    high_score = load_high_score(ROOM_COUNT_FILE)

    # Generate obstacles, player, and door positions
    obstacles = generate_building_obstacles(OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER)
    player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
    door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, EDGE_BUFFER)

    # Ensure there's a path between player and door
    obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE)

    clock = pygame.time.Clock()
    move_speed = 7
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        new_player_pos = player_pos[:]

        # Handle movement with edge collision
        if keys[pygame.K_LEFT] and player_pos[0] > 0:  # Check left edge
            new_player_pos[0] -= move_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WINDOW_WIDTH - PLAYER_SIZE:  # Check right edge
            new_player_pos[0] += move_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:  # Check top edge
            new_player_pos[1] -= move_speed
        if keys[pygame.K_DOWN] and player_pos[1] < WINDOW_HEIGHT - PLAYER_SIZE:  # Check bottom edge
            new_player_pos[1] += move_speed

        # Check collision with obstacles
        player_rect = pygame.Rect(*new_player_pos, PLAYER_SIZE, PLAYER_SIZE)
        if not check_collision_with_obstacles(player_rect, obstacles, TILE_SIZE):
            player_pos = new_player_pos

        # Check if player touches the door
        door_rect = pygame.Rect(*door_pos, PLAYER_SIZE, PLAYER_SIZE)
        if player_rect.colliderect(door_rect):
            room_count += 1
            if room_count > high_score:
                high_score = room_count  # Update high score
                save_high_score(ROOM_COUNT_FILE, high_score)  # Save only the high score

            # Generate new room
            obstacles = generate_building_obstacles(OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER)
            player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
            door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, EDGE_BUFFER)
            obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE)

            # Revalidate player position
            player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)

        # Rendering
        screen.fill(BACKGROUND_COLOR)
        draw_obstacles(screen, obstacles, TILE_SIZE)
        pygame.draw.rect(screen, DOOR_COLOR, (*door_pos, PLAYER_SIZE, PLAYER_SIZE))
        pygame.draw.rect(screen, PLAYER_COLOR, (*player_pos, PLAYER_SIZE, PLAYER_SIZE))
        display_room_count(screen, room_count, font)
        display_high_score(screen, high_score, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
