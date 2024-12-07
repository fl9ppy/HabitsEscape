import random
import pygame
import heapq

def generate_building_obstacles(count, tile_size, spacing, window_width, window_height, edge_buffer):
    """Generate obstacles."""
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

def is_on_building(rect, obstacles, tile_size):
    """Check if a given rect collides with any obstacles."""
    for ox, oy in obstacles:
        obstacle_rect = pygame.Rect(ox, oy, tile_size, tile_size)
        if rect.colliderect(obstacle_rect):
            return True
    return False

def get_valid_starting_position(obstacles, player_size, window_width, window_height, edge_buffer, tile_size):
    """Generate a valid starting position for the player."""
    while True:
        x = random.randint(edge_buffer, window_width - edge_buffer - player_size)
        y = random.randint(edge_buffer, window_height - edge_buffer - player_size)
        player_rect = pygame.Rect(x, y, player_size, player_size)
        if not is_on_building(player_rect, obstacles, tile_size):
            return [x, y]

def generate_door_position_on_edge(obstacles, window_width, window_height, door_size, edge_buffer, tile_size):
    """Generate a valid door position on the edge of the screen."""
    while True:
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(edge_buffer, window_width - edge_buffer - door_size), 0
        elif edge == "bottom":
            x, y = random.randint(edge_buffer, window_width - edge_buffer - door_size), window_height - door_size
        elif edge == "left":
            x, y = 0, random.randint(edge_buffer, window_height - edge_buffer - door_size)
        elif edge == "right":
            x, y = window_width - door_size, random.randint(edge_buffer, window_height - edge_buffer - door_size)

        door_rect = pygame.Rect(x, y, door_size, door_size)
        if not is_on_building(door_rect, obstacles, tile_size):
            return [x, y]

def ensure_path(player_pos, door_pos, obstacles, tile_size, window_width, window_height, player_size):
    """Ensure there's a valid path between the player and the door."""
    while not a_star_path(player_pos, door_pos, obstacles, tile_size, window_width // tile_size, window_height // tile_size):
        obstacles = generate_building_obstacles(len(obstacles), tile_size, tile_size + 20, window_width, window_height, 100)
        player_pos = get_valid_starting_position(obstacles, player_size, window_width, window_height, 100, tile_size)
    return obstacles

def generate_enemy_positions(obstacles, count, enemy_size, window_width, window_height, edge_buffer, tile_size):
    """Generate random enemy positions avoiding obstacles, with random speeds and health."""
    enemies = []
    for _ in range(count):
        while True:
            x = random.randint(edge_buffer, window_width - edge_buffer - enemy_size)
            y = random.randint(edge_buffer, window_height - edge_buffer - enemy_size)
            enemy_rect = pygame.Rect(x, y, enemy_size, enemy_size)
            if not is_on_building(enemy_rect, obstacles, tile_size):
                speed = random.uniform(1, 3)  # Random speed (slower than the player)
                health = 20  # Default health for enemies
                enemies.append({"pos": [x, y], "speed": speed, "health": health})
                break
    return enemies


def move_enemies_toward_player(enemies, player_pos, obstacles, tile_size, grid_width, grid_height):
    """Move enemies toward the player using A* pathfinding."""
    for enemy in enemies:
        start = (enemy["pos"][0], enemy["pos"][1])
        goal = (player_pos[0], player_pos[1])

        # Calculate a path to the player using A*
        path = a_star_path(start, goal, obstacles, tile_size, grid_width, grid_height)

        if path:
            next_pos = path[0]
            dx = next_pos[0] - enemy["pos"][0]
            dy = next_pos[1] - enemy["pos"][1]

            # Move the enemy toward the next path position
            speed = enemy["speed"]
            step_x = min(speed, abs(dx)) * (1 if dx > 0 else -1) if dx != 0 else 0
            step_y = min(speed, abs(dy)) * (1 if dy > 0 else -1) if dy != 0 else 0

            # Update enemy position
            enemy["pos"][0] += step_x
            enemy["pos"][1] += step_y



def a_star_path(start, goal, obstacles, tile_size, grid_width, grid_height):
    """Find the shortest path from start to goal using A*."""
    start_cell = (start[0] // tile_size, start[1] // tile_size)
    goal_cell = (goal[0] // tile_size, goal[1] // tile_size)

    open_set = []
    heapq.heappush(open_set, (0, start_cell))
    came_from = {}
    g_score = {start_cell: 0}
    f_score = {start_cell: heuristic(start_cell, goal_cell)}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal_cell:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return [(p[0] * tile_size, p[1] * tile_size) for p in path]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                0 <= neighbor[0] < grid_width
                and 0 <= neighbor[1] < grid_height
                and not is_on_building(pygame.Rect(neighbor[0] * tile_size, neighbor[1] * tile_size, tile_size, tile_size), obstacles, tile_size)
            ):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal_cell)
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

def heuristic(cell, goal):
    """Heuristic function: Manhattan distance."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])