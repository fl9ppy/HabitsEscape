import pygame
from game_logic import (
    generate_building_obstacles,
    generate_door_position_on_edge,
    get_valid_starting_position,
    check_collision_with_obstacles,
    ensure_path,
)
from display import draw_obstacles, display_room_count, display_high_score
from menu import main_menu
from config import (  # Import shared constants
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_SIZE,
    BACKGROUND_COLOR,
    DOOR_COLOR,
    TILE_SIZE,
    SPACING,
    OBSTACLE_COUNT,
    EDGE_BUFFER,
)

# (Keep the rest of your constants and functions as-is)

if __name__ == "__main__":
    main_menu()  # Show the menu first
    main()       # Start the game after exiting the menu
