import random
import pygame
from collections import deque

def generate_building_obstacles(count, tile_size, spacing, window_width, window_height, edge_buffer):
    obstacles = []
    grid_width = (window_width - 2 * edge_buffer) // spacing
    grid_height = (window_height - 2 * edge_buffer) // spacing

    for _ in range(count):
        grid_x = random.randint(0, grid_width - 1)
        grid_y = random.randint(0, grid_height - 1)
        x = edge_buffer + grid_x * spacing
        y = edge_buffer + grid_y * spacing
        obstacles.append((x, y))
    return obstacles

def check_collision_with_obstacles(rect, obstacles, tile_size):
    for x, y in obstacles:
        obstacle_rect = pygame.Rect(x, y, tile_size, tile_size)
        if rect.colliderect(obstacle_rect):
            return True
    return False

def generate_door_position_on_edge(obstacles, window_width, window_height, player_size, safe_zone):
    while True:
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(safe_zone, window_width - safe_zone - player_size), 0
        elif edge == "bottom":
            x, y = random.randint(safe_zone, window_width - safe_zone - player_size), window_height - player_size
        elif edge == "left":
            x, y = 0, random.randint(safe_zone, window_height - safe_zone - player_size)
        elif edge == "right":
            x, y = window_width - player_size, random.randint(safe_zone, window_height - safe_zone - player_size)

        door_rect = pygame.Rect(x, y, player_size, player_size)
        if not check_collision_with_obstacles(door_rect, obstacles, player_size):
            return [x, y]

def get_valid_starting_position(obstacles, player_size, window_width, window_height, edge_buffer, tile_size):
    while True:
        x = random.randint(edge_buffer, window_width - edge_buffer - player_size)
        y = random.randint(edge_buffer, window_height - edge_buffer - player_size)
        player_rect = pygame.Rect(x, y, player_size, player_size)
        collision = False
        for ox, oy in obstacles:
            obstacle_rect = pygame.Rect(ox, oy, tile_size, tile_size)
            if player_rect.colliderect(obstacle_rect):
                collision = True
                break
        if not collision:
            return [x, y]

def flood_fill_check_path(player_pos, door_pos, obstacles, tile_size, window_width, window_height):
    queue = deque([player_pos])
    visited = set()
    visited.add((player_pos[0] // tile_size, player_pos[1] // tile_size))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while queue:
        current_x, current_y = queue.popleft()

        if pygame.Rect(current_x, current_y, tile_size, tile_size).colliderect(
            pygame.Rect(*door_pos, tile_size, tile_size)
        ):
            return True

        for dx, dy in directions:
            nx, ny = current_x + dx * tile_size, current_y + dy * tile_size
            cell = (nx // tile_size, ny // tile_size)

            if (
                0 <= nx < window_width
                and 0 <= ny < window_height
                and cell not in visited
                and not check_collision_with_obstacles(
                    pygame.Rect(nx, ny, tile_size, tile_size), obstacles, tile_size
                )
            ):
                visited.add(cell)
                queue.append((nx, ny))

    return False

def ensure_path(player_pos, door_pos, obstacles, tile_size, window_width, window_height, player_size):
    """Ensure there's a valid path between player and door."""
    while not flood_fill_check_path(player_pos, door_pos, obstacles, tile_size, window_width, window_height):
        obstacles = generate_building_obstacles(len(obstacles), tile_size, tile_size + 20, window_width, window_height, 100)
        player_pos = get_valid_starting_position(obstacles, player_size, window_width, window_height, 100, tile_size)
    return obstacles
