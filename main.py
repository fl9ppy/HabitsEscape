import pygame
from game_logic import (
    generate_building_obstacles,
    generate_door_position_on_edge,
    get_valid_starting_position,
    generate_enemy_positions,
    move_enemies_toward_player,
    ensure_path,
)
from display import draw_obstacles, display_room_count, display_high_score

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLAYER_SIZE = 50
ENEMY_SIZE = 50
TILE_SIZE = 125
DOOR_SIZE = 100
SPACING = 150
OBSTACLE_COUNT = 12
EDGE_BUFFER = 100
ENEMY_COUNT = 5
PLAYER_HEALTH = 100
ROOM_COUNT_FILE = "room_count.txt"
DAMAGE_COOLDOWN = 1000  # Milliseconds
HIT_ANIMATION_DURATION = 200  # Duration for player hit animation in milliseconds

HEALTH_COLOR = (255, 255, 255)

def load_high_score(file_path):
    try:
        with open(file_path, "r") as file:
            data = file.read().strip().split()
            high_score = int(data[1]) if len(data) > 1 else 0
            return high_score
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(file_path, high_score):
    with open(file_path, "w") as file:
        file.write(f"0 {high_score}")

def display_health(screen, health, font):
    health_text = font.render(f"Health: {health}", True, HEALTH_COLOR)
    screen.blit(health_text, (10, 50))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Room Counter Game")
    font = pygame.font.Font(None, 36)

    # Load images
    background_image = pygame.image.load("assets/background.jpg")
    player_image = pygame.image.load("assets/raul.png")
    player_image_hit = pygame.image.load("assets/raulsabie.png")
    enemy_image = pygame.image.load("assets/beer.png")
    enemy_image_hit = pygame.image.load("assets/beer_hit.png")
    door_image = pygame.image.load("assets/cigs.png")
    building_images = [
        pygame.image.load("assets/building1.png"),
        pygame.image.load("assets/building2.png"),
        pygame.image.load("assets/building3.png")
    ]

    # Create mirrored versions of the player images
    player_image_mirror = pygame.transform.flip(player_image, True, False)
    player_image_mirror_hit = pygame.transform.flip(player_image_hit, True, False)

    # Scale images
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    player_image = pygame.transform.scale(player_image, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_hit = pygame.transform.scale(player_image_hit, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_mirror = pygame.transform.scale(player_image_mirror, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_mirror_hit = pygame.transform.scale(player_image_mirror_hit, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))
    enemy_image_hit = pygame.transform.scale(enemy_image_hit, (ENEMY_SIZE, ENEMY_SIZE))
    door_image = pygame.transform.scale(door_image, (DOOR_SIZE, DOOR_SIZE))
    building_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in building_images]

    room_count = 0
    high_score = load_high_score(ROOM_COUNT_FILE)

    clock = pygame.time.Clock()
    move_speed = 7
    running = True

    player_level_multiplier = 1
    player_health = 100 * player_level_multiplier
    player_damage = 50 * player_level_multiplier
    last_damage_time = 0
    player_last_hit_time = 0  # Initialize player hit time
    player_facing = "right"  # Default facing direction

    obstacles = generate_building_obstacles(
        OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images
    )
    player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE)
    enemies = generate_enemy_positions(
        obstacles, ENEMY_COUNT, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE, 100  # Initial health
    )
    enemy_level_multiplier = 1
    obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, building_images)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        new_player_pos = player_pos[:]

        # Player movement logic
        if keys[pygame.K_LEFT]:
            new_player_pos[0] -= move_speed
            player_facing = "left"
        if keys[pygame.K_RIGHT]:
            new_player_pos[0] += move_speed
            player_facing = "right"
        if keys[pygame.K_UP]:
            new_player_pos[1] -= move_speed
        if keys[pygame.K_DOWN]:
            new_player_pos[1] += move_speed

        collisions = [pygame.Rect(o[0], o[1], o[2], o[3]) for o in obstacles]
        if pygame.Rect(new_player_pos[0], new_player_pos[1], PLAYER_SIZE, PLAYER_SIZE).collidelist(collisions) == -1:
            player_pos = new_player_pos
            player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)

        # Player attack logic
        is_attacking = keys[pygame.K_SPACE]
        if is_attacking and pygame.time.get_ticks() - player_last_hit_time > HIT_ANIMATION_DURATION:
            player_last_hit_time = pygame.time.get_ticks()  # Record the time of the attack
            attack_range = pygame.Rect(
                player_pos[0] - 20, player_pos[1] - 20,
                PLAYER_SIZE + 40, PLAYER_SIZE + 40
            )
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], ENEMY_SIZE, ENEMY_SIZE)
                if attack_range.colliderect(enemy_rect):
                    enemy["health"] -= player_damage
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)

        # Enemy movement logic
        move_enemies_toward_player(
            enemies, player_pos, obstacles, TILE_SIZE, WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE
        )

        # Check for enemy collisions and apply damage
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                if current_time - last_damage_time > DAMAGE_COOLDOWN:
                    scaled_enemy_damage = 10 * enemy_level_multiplier  # Increase damage by 2 per room
                    player_health -= scaled_enemy_damage
                    last_damage_time = current_time
                    enemy["last_hit_time"] = current_time  # Update last hit time
                    print(f"Enemy hit! Damage dealt: {scaled_enemy_damage}, Player Health: {player_health}")

        # Check for game over
        if player_health <= 0:
            print("Game Over!")
            running = False

        # Door collision and room transition
        door_rect = pygame.Rect(door_pos[0], door_pos[1], DOOR_SIZE, DOOR_SIZE)
        if player_rect.colliderect(door_rect) and not enemies:
            room_count += 1
            enemy_level_multiplier += 0.2
            if room_count > high_score:
                high_score = room_count
                save_high_score(ROOM_COUNT_FILE, high_score)

            # Scale enemy stats
            scaled_enemy_count = ENEMY_COUNT + (room_count // 3)  # Increase enemies every 3 rooms
            scaled_enemy_health = 100 * enemy_level_multiplier   # Increase health by 10 per room

            print(f"Entering Room {room_count}")
            print(f"Enemy Count: {scaled_enemy_count}, Enemy Health: {scaled_enemy_health}")

            # Regenerate the room
            obstacles = generate_building_obstacles(
                OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images
            )
            player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
            player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
            door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE)
            enemies = generate_enemy_positions(
                obstacles, scaled_enemy_count, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE, scaled_enemy_health
            )
            obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, building_images)

        # Rendering
        screen.blit(background_image, (0, 0))
        draw_obstacles(screen, obstacles)
        for enemy in enemies:
            if current_time - enemy["last_hit_time"] <= DAMAGE_COOLDOWN:
                screen.blit(enemy_image_hit, (enemy["pos"][0], enemy["pos"][1]))  # Hitting skin
            else:
                screen.blit(enemy_image, (enemy["pos"][0], enemy["pos"][1]))  # Normal skin
        if current_time - player_last_hit_time <= HIT_ANIMATION_DURATION:
            # Render hitting skin
            if player_facing == "left":
                screen.blit(player_image_hit, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
            else:
                screen.blit(player_image_mirror_hit, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
        else:
            # Render idle skin
            if player_facing == "left":
                screen.blit(player_image, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
            else:
                screen.blit(player_image_mirror, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
        if not enemies:
            screen.blit(door_image, (door_pos[0], door_pos[1]))  # Door image
        display_health(screen, player_health, font)
        display_room_count(screen, room_count, font)
        display_high_score(screen, high_score, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
