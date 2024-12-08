import heapq
import random
import pygame

global room_count, player_health, enemies, obstacles, door_pos, player_pos, enemy_level_multiplier

def generate_building_obstacles(count, tile_size, spacing, window_width, window_height, edge_buffer, building_images):
    """Generate building obstacles with random images and dimensions."""
    obstacles = []

    for _ in range(count):
        while True:
            # Randomly position the obstacle
            x = random.randint(edge_buffer, window_width - edge_buffer - tile_size)
            y = random.randint(edge_buffer, window_height - edge_buffer - tile_size)

            # Assign a random image
            image = random.choice(building_images)

            # Determine size based on the chosen skin
            if image == building_images[0]:  # Example: First skin becomes a rectangle
                width, height = tile_size, tile_size * 1.5  # Rectangular dimensions
            else:
                width, height = tile_size, tile_size  # Default square

            # Check if this obstacle overlaps any existing obstacles
            rect = pygame.Rect(x, y, width, height)
            if not any(rect.colliderect(pygame.Rect(ox, oy, ow, oh)) for ox, oy, ow, oh, _ in obstacles):
                obstacles.append((x, y, width, height, image))
                break

    return obstacles

def is_on_building(player_rect, obstacles, _):
    """Check if the player is on any building."""
    for ox, oy, width, height, _ in obstacles:
        building_rect = pygame.Rect(ox, oy, width, height)
        if player_rect.colliderect(building_rect):
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
    # Define restricted areas (health bar and sign positions)
    health_bar_area = pygame.Rect(10, 10, 280, 80)  # Adjust based on actual health bar position and size
    sign_area = pygame.Rect(5, window_height - 145, 200, 150)  # Adjust based on actual sign position and size

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

        # Ensure the door does not overlap restricted areas or obstacles
        if (
            not any(door_rect.colliderect(pygame.Rect(ox, oy, ow, oh)) for ox, oy, ow, oh, _ in obstacles)
            and not door_rect.colliderect(health_bar_area)
            and not door_rect.colliderect(sign_area)
        ):
            return [x, y]

def ensure_path(player_pos, door_pos, obstacles, tile_size, window_width, window_height, player_size, building_images):
    """Ensure there is a valid path between the player and the door."""
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    door_rect = pygame.Rect(door_pos[0], door_pos[1], player_size, player_size)

    # Regenerate obstacles until there is a clear path between player and door
    while True:
        valid_path = True
        for obstacle in obstacles:
            ox, oy, width, height, _ = obstacle
            obstacle_rect = pygame.Rect(ox, oy, width, height)
            if player_rect.colliderect(obstacle_rect) or door_rect.colliderect(obstacle_rect):
                valid_path = False
                break
        if valid_path:
            break
        obstacles = generate_building_obstacles(
            len(obstacles), tile_size, tile_size + 20, window_width, window_height, 100, building_images
        )

    return obstacles

def restart_game(WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_HEALTH, DOOR_SIZE, PLAYER_SIZE,
                 OBSTACLE_COUNT, TILE_SIZE, SPACING, EDGE_BUFFER, ENEMY_COUNT, ENEMY_SIZE, building_images):
    """
    Reset the game to its initial state, regenerating level, enemies, and player position.
    """
    # Reset room count and player health
    room_count = 0
    player_health = PLAYER_HEALTH

    # Reset enemy level multiplier
    enemy_level_multiplier = 1

    # Regenerate room obstacles
    obstacles = generate_building_obstacles(
        OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images
    )

    # Reset player position
    player_pos = get_valid_starting_position(
        obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE
    )

    # Generate a new door position
    door_pos = generate_door_position_on_edge(
        obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE
    )

    # Generate a new set of enemies
    enemies = generate_enemy_positions(
        obstacles, ENEMY_COUNT, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,
        EDGE_BUFFER, TILE_SIZE, 100, enemy_level_multiplier
    )

    # Ensure a valid path between player and door
    obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, building_images)

    # Return the updated state
    return room_count, player_health, obstacles, player_pos, door_pos, enemies, enemy_level_multiplier





def generate_enemy_positions(obstacles, enemy_count, enemy_size, window_width, window_height, edge_buffer, tile_size, enemy_health, enemy_level_multiplier):
    """Generate initial enemy positions avoiding obstacles."""
    enemies = []

    for _ in range(enemy_count):
        while True:
            x = random.randint(edge_buffer, window_width - edge_buffer - enemy_size)
            y = random.randint(edge_buffer, window_height - edge_buffer - enemy_size)

            enemy_rect = pygame.Rect(x, y, enemy_size, enemy_size)

            # Check if the enemy overlaps with any obstacle or other enemy
            if not any(enemy_rect.colliderect(pygame.Rect(ox, oy, ow, oh)) for ox, oy, ow, oh, _ in obstacles) and \
               not any(enemy_rect.colliderect(pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy_size, enemy_size)) for enemy in enemies):
                enemies.append({
                    "pos": (x, y),
                    "health": enemy_health,  # Set health dynamically based on room count
                    "last_hit_time": 0,  # Initialize hit cooldown
                    "speed": random.uniform(1.0, 3.0) * enemy_level_multiplier  # Random speed slower than player
                })
                break

    return enemies

def move_enemies_toward_player(enemies, player_pos, obstacles, tile_size, grid_width, grid_height):
    """Move enemies toward the player, avoiding obstacles."""
    for enemy in enemies:
        enemy_x, enemy_y = enemy["pos"]
        player_x, player_y = player_pos

        # Calculate direction vector
        dx = player_x - enemy_x
        dy = player_y - enemy_y

        # Normalize direction vector to get unit step
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            continue  # Skip if already at the player's position
        step_x = (dx / distance) * enemy["speed"]
        step_y = (dy / distance) * enemy["speed"]

        # Calculate new position
        new_x = enemy_x + step_x
        new_y = enemy_y + step_y

        # Check for collisions with obstacles
        enemy_rect = pygame.Rect(new_x, new_y, tile_size, tile_size)
        if not any(enemy_rect.colliderect(pygame.Rect(ox, oy, ow, oh)) for ox, oy, ow, oh, _ in obstacles):
            enemy["pos"] = (new_x, new_y)  # Update position as a new tuple




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