import pygame
from game_logic import (
    generate_building_obstacles,
    generate_door_position_on_edge,
    get_valid_starting_position,
    generate_enemy_positions,
    move_enemies_toward_player,
    ensure_path,
)
from display import load_health_bar_assets, display_health_bar, draw_obstacles, display_room_count, display_high_score, \
    display_health, load_font, display_sign, show_death_screen

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLAYER_SIZE = 50
ENEMY_SIZE = 50
TILE_SIZE = 115
DOOR_SIZE = 100
SPACING = 250
OBSTACLE_COUNT = 8
EDGE_BUFFER = 150
ENEMY_COUNT = 5
PLAYER_HEALTH = 100
ROOM_COUNT_FILE = "room_count.txt"
DAMAGE_COOLDOWN = 1000  # Milliseconds
HIT_ANIMATION_DURATION = 200  # Duration for player hit animation in milliseconds

HEALTH_COLOR = (255, 255, 255)

def load_addiction_data(file_path):
    """Loads addiction data from a file and returns the addiction type."""
    try:
        with open(file_path, "r") as file:
            data = file.readlines()
            addiction_data = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in data}
            return addiction_data.get("Addiction", "Default")
    except FileNotFoundError:
        return "Default"  # Fallback if file doesn't exist

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Room Counter Game")
    font = load_font()
    health_bar_base = load_health_bar_assets()
    sign_image = pygame.image.load("assets/others/sign.png")
    sign_image = pygame.transform.scale(sign_image, (200, 150))

    # Load images
    background_image = pygame.image.load("assets/scene/better_background.png")
    player_image1 = pygame.image.load("assets/modi/modi_mers_dreapra.png")  # Primary idle skin
    player_image2 = pygame.image.load("assets/modi/modi_mers_stanga.png")
    player_image_hit = pygame.image.load("assets/modi/raulsabie.png")
    player_image_idle = pygame.image.load("assets/modi/ial2.png")
    enemy_image = pygame.image.load("assets/enemies/beer.png")
    enemy_image_hit = pygame.image.load("assets/enemies/beer_hit.png")
    door_image1 = pygame.image.load("assets/others/portaljos.png")
    door_image2 = pygame.image.load("assets/others/portalsus.png")
    building_images = [
        pygame.image.load("assets/others/building1.png"),
        pygame.image.load("assets/others/building2.png"),
        pygame.image.load("assets/others/building3.png")
    ]

    # Create mirrored versions of the player images
    player_image1_mirror = pygame.transform.flip(player_image1, True, False)
    player_image2_mirror = pygame.transform.flip(player_image2, True, False)
    player_image_mirror_hit = pygame.transform.flip(player_image_hit, True, False)
    player_image_idle_mirror = pygame.transform.flip(player_image_idle, True, False)

    # Scale images
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    player_image1 = pygame.transform.scale(player_image1, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image2 = pygame.transform.scale(player_image2, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_idle = pygame.transform.scale(player_image_idle, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_hit = pygame.transform.scale(player_image_hit, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image1_mirror = pygame.transform.scale(player_image1_mirror, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image2_mirror = pygame.transform.scale(player_image2_mirror, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_idle_mirror = pygame.transform.scale(player_image_idle_mirror, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    player_image_mirror_hit = pygame.transform.scale(player_image_mirror_hit, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
    enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))
    enemy_image_hit = pygame.transform.scale(enemy_image_hit, (ENEMY_SIZE, ENEMY_SIZE))
    door_image1 = pygame.transform.scale(door_image1, (DOOR_SIZE, DOOR_SIZE))
    door_image2 = pygame.transform.scale(door_image2, (DOOR_SIZE, DOOR_SIZE))
    building_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in building_images]

    room_count = 0
    high_score = load_high_score(ROOM_COUNT_FILE)

    clock = pygame.time.Clock()

    running = True

    player_skin_toggle = True  # Toggle state for player skin
    last_player_skin_toggle_time = pygame.time.get_ticks()
    last_input_time = pygame.time.get_ticks()
    idle_threshold = 5000

    door_image_toggle = True  # Toggle state
    last_toggle_time = pygame.time.get_ticks()

    player_level_multiplier = 1
    move_speed = 7 * player_level_multiplier
    player_health = 100 * player_level_multiplier
    player_damage = 50 * player_level_multiplier
    last_damage_time = 0
    player_last_hit_time = 0  # Initialize player hit time
    player_facing = "right"  # Default facing direction

    obstacles = generate_building_obstacles(
        OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images
    )
    enemy_level_multiplier = 1
    player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE)
    enemies = generate_enemy_positions(
        obstacles, ENEMY_COUNT, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE, 100, enemy_level_multiplier  # Initial health
    )

    obstacles = ensure_path(player_pos, door_pos, obstacles, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_SIZE, building_images)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        new_player_pos = player_pos[:]

        current_time = pygame.time.get_ticks()
        idle = current_time - last_input_time > idle_threshold  # Check for idle state

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            last_input_time = current_time

        if current_time - last_player_skin_toggle_time >= 500:  # Toggle every 0.5 seconds
            player_skin_toggle = not player_skin_toggle
            last_player_skin_toggle_time = current_time

        # Player skin toggle logic
        if current_time - last_player_skin_toggle_time >= 500:  # Toggle every 0.5 seconds
            player_skin_toggle = not player_skin_toggle
            last_player_skin_toggle_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Door skin toggle logic
        if current_time - last_toggle_time >= 1000:  # Toggle every 1 second
            door_image_toggle = not door_image_toggle
            last_toggle_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                if current_time - last_damage_time > DAMAGE_COOLDOWN:
                    scaled_enemy_damage = 10 * enemy_level_multiplier  # Increase damage by 2 per room
                    player_health -= scaled_enemy_damage
                    last_damage_time = current_time
                    enemy["last_hit_time"] = current_time  # Update last hit time

        # Check for game over
        if player_health <= 0:
            # Call death screen and reset game
            updated_state = show_death_screen(
                screen, font, pygame.image.load("assets/others/death_menu.png"), WINDOW_WIDTH, WINDOW_HEIGHT,
                PLAYER_HEALTH, DOOR_SIZE, PLAYER_SIZE, OBSTACLE_COUNT, TILE_SIZE, SPACING,
                WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images, ENEMY_COUNT, ENEMY_SIZE
            )

            # Unpack the updated state
            room_count, player_health, obstacles, player_pos, door_pos, enemies, enemy_level_multiplier = updated_state

            print("Game restarted, resuming with reset state.")
            continue

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

            # Regenerate the room
            obstacles = generate_building_obstacles(
                OBSTACLE_COUNT, TILE_SIZE, SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, building_images
            )
            player_pos = get_valid_starting_position(obstacles, PLAYER_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE)
            player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
            door_pos = generate_door_position_on_edge(obstacles, WINDOW_WIDTH, WINDOW_HEIGHT, DOOR_SIZE, EDGE_BUFFER, TILE_SIZE)
            enemies = generate_enemy_positions(
                obstacles, scaled_enemy_count, ENEMY_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, EDGE_BUFFER, TILE_SIZE, scaled_enemy_health, enemy_level_multiplier
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
        if idle:
            # Render special idle skin
            if player_facing == "left":
                screen.blit(player_image_idle, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
            else:
                screen.blit(player_image_idle_mirror, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
        else:
            if current_time - player_last_hit_time <= HIT_ANIMATION_DURATION:
                if player_facing == "left":
                    screen.blit(player_image_hit, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
                else:
                    screen.blit(player_image_mirror_hit, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
            else:
                # Render idle skin
                if player_facing == "left":
                    if player_skin_toggle:
                        screen.blit(player_image1, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
                    else:
                        screen.blit(player_image2, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
                else:
                    if player_skin_toggle:
                        screen.blit(player_image1_mirror, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))
                    else:
                        screen.blit(player_image2_mirror, (player_pos[0] - PLAYER_SIZE, player_pos[1] - PLAYER_SIZE))

        if not enemies:
            if door_image_toggle:
                screen.blit(door_image1, (door_pos[0], door_pos[1]))
            else:
                screen.blit(door_image2, (door_pos[0], door_pos[1]))
        display_health_bar(screen, player_health, PLAYER_HEALTH, health_bar_base, (10, 10), player_level_multiplier)
        display_sign(screen, room_count, high_score, font, sign_image, (5, WINDOW_HEIGHT - 145))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
