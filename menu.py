import pygame
import sys

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (50, 50, 50)
BUTTON_COLOR = (100, 200, 100)
HOVER_COLOR = (150, 250, 150)
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 50
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
BUTTON_SPACING = 20

def draw_button(screen, text, rect, color, font):
    """Draw a button with text."""
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def main_menu():
    """Display the main menu and handle user input."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Main Menu")
    font = pygame.font.Font(None, FONT_SIZE)

    # Button positions
    start_button_rect = pygame.Rect(
        (WINDOW_WIDTH - BUTTON_WIDTH) // 2,
        (WINDOW_HEIGHT - BUTTON_HEIGHT - BUTTON_SPACING) // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    quit_button_rect = pygame.Rect(
        (WINDOW_WIDTH - BUTTON_WIDTH) // 2,
        (WINDOW_HEIGHT + BUTTON_SPACING) // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check for hover
        start_button_color = HOVER_COLOR if start_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        quit_button_color = HOVER_COLOR if quit_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR

        # Draw buttons
        draw_button(screen, "Start", start_button_rect, start_button_color, font)
        draw_button(screen, "Quit", quit_button_rect, quit_button_color, font)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if start_button_rect.collidepoint(mouse_pos):
                    running = False  # Exit menu to start the game
                if quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.flip()
        pygame.time.Clock().tick(30)
