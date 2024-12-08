import pygame
import sys
import os
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# Fonts
TITLE_FONT = pygame.font.Font("assets/others/8bit_font.ttf", 40)
QUESTION_FONT = pygame.font.Font("assets/others/8bit_font.ttf", 25)
BUTTON_FONT = pygame.font.Font("assets/others/8bit_font.ttf", 20)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HabitsEscape")

# Outside files
DATA_FILE = "player_data.txt"
fire_icon = pygame.image.load("assets/others/fire.png") # Fire image for streak
fire_icon = pygame.transform.scale(fire_icon, (40, 40))  # Resize as needed
BACKGROUND = pygame.image.load("assets/others/menu_background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to screen size
LOGO = pygame.image.load("assets/others/logo.png")

# Set game icon
pygame.display.set_icon(LOGO)

def draw_text(text, font, color, x, y, centered=True):
    """Helper function to render text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def ensure_data_file_exists():
    """Ensure the player data file exists, and create it if missing."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            file.write("Addiction: None\n")
            file.write("LastAnswered: None\n")
            file.write("Streak: 0\n")
            file.write("Amount: 0\n")
            print("Generated player_data.txt with default values.")

def read_player_data():
    """Read player data from the file."""
    ensure_data_file_exists()
    with open(DATA_FILE, "r") as file:
        data = file.readlines()
        return {line.split(":")[0].strip(): line.split(":")[1].strip() for line in data if ":" in line}

def write_player_data(key, value):
    """Write a key-value pair to the player data file."""
    data = read_player_data()
    data[key] = value
    with open(DATA_FILE, "w") as file:
        for k, v in data.items():
            file.write(f"{k}: {v}\n")

def check_and_update_streak():
    """Check if the streak should be reset or updated."""
    data = read_player_data()
    last_answered = data.get("LastAnswered", "None")
    streak = int(data.get("Streak", 0))
    
    if last_answered == "None":
        return streak  # First time running, no changes needed
    
    # Compare dates
    try:
        last_date = datetime.strptime(last_answered, "%Y-%m-%d").date()  # Convert to date object
    except ValueError:
        last_date = datetime.now().date() - timedelta(days=2)  # Fallback to force reset streak
    
    today = datetime.now().date()  # Get today's date as a date object
    
    # If the difference is more than 1 day, reset the streak to 1
    if today > last_date + timedelta(days=1):  # More than a day passed
        write_player_data("Streak", "1")  # Reset streak to 1
        streak = 1
    return streak

def choose_addiction():
    """Prompt the player to choose their addiction."""
    addiction = None
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Choose your addiction:", QUESTION_FONT, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        # Addiction options as buttons
        smoking_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 50)
        drinking_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 50)

        pygame.draw.rect(screen, DARK_GRAY, smoking_button, border_radius=20)
        pygame.draw.rect(screen, DARK_GRAY, drinking_button, border_radius=20)

        draw_text("Smoking", BUTTON_FONT, WHITE, smoking_button.centerx, smoking_button.centery)
        draw_text("Drinking", BUTTON_FONT, WHITE, drinking_button.centerx, drinking_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if smoking_button.collidepoint(event.pos):
                    addiction = "Smoking"
                elif drinking_button.collidepoint(event.pos):
                    addiction = "Drinking"
                if addiction:
                    write_player_data("Addiction", addiction)
                    running = False

        pygame.display.flip()

    return addiction

def ask_question(addiction):
    """Ask a context-specific question based on the addiction."""
    running = True
    answered_yes = False
    input_active = False
    input_text = ""

    while running:
        screen.fill(DARK_GRAY)

        if not answered_yes:
            question = f"Have you {'smoked' if addiction == 'Smoking' else 'had any drinks'} today?"
            draw_text(question, QUESTION_FONT, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            
            yes_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 100, 50)
            no_button = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, 100, 50)
            pygame.draw.rect(screen, GRAY, yes_button, border_radius=20)
            pygame.draw.rect(screen, GRAY, no_button, border_radius=20)
            draw_text("Yes", BUTTON_FONT, WHITE, yes_button.centerx, yes_button.centery)
            draw_text("No", BUTTON_FONT, WHITE, no_button.centerx, no_button.centery)
        else:
            draw_text("How many?", QUESTION_FONT, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
            pygame.draw.rect(screen, GRAY, input_box, border_radius=20)
            draw_text(input_text, BUTTON_FONT, WHITE, input_box.centerx, input_box.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not answered_yes:
                    if yes_button.collidepoint(event.pos):
                        answered_yes = True
                        input_active = True
                        write_player_data("Streak", "0")
                        write_player_data("LastAnswered", datetime.now().strftime("%Y-%m-%d"))
                    elif no_button.collidepoint(event.pos):
                        last_answered = read_player_data().get("LastAnswered", "None")
                        today = datetime.now().date().strftime("%Y-%m-%d")
                        if last_answered != today:
                            streak = int(read_player_data().get("Streak", 0)) + 1
                            write_player_data("Streak", str(streak))
                        write_player_data("LastAnswered", today)
                        write_player_data("Amount", "0")
                        return
                elif input_active and input_box.collidepoint(event.pos):
                    input_active = True
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        amount = int(input_text)
                        write_player_data("Amount", str(amount))
                        return
                    else:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

        pygame.display.flip()

def fade_to_black(duration=1000):
    """Fade to black effect."""
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(DARK_GRAY)
    fade_surface.set_alpha(0)  # Start fully transparent
    for alpha in range(0, 256, int(255 / (duration / 16))):  # Update alpha gradually
        fade_surface.set_alpha(min(alpha, 255))  # Ensure alpha doesn't go over 255
        screen.fill(WHITE)  # Fill screen with white (background color)
        screen.blit(fade_surface, (0, 0))  # Apply the fade effect
        pygame.display.update()  # Update the display
        pygame.time.delay(16)  # Delay to create smooth transition

def fade_from_black(duration=1000):
    """Fade from black effect."""
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(DARK_GRAY)
    fade_surface.set_alpha(255)  # Start fully opaque
    for alpha in range(255, -1, -int(255 / (duration / 16))):  # Update alpha gradually
        fade_surface.set_alpha(max(alpha, 0))  # Ensure alpha doesn't go below 0
        screen.fill(WHITE)  # Fill screen with white (background color)
        screen.blit(fade_surface, (0, 0))  # Apply the fade effect
        pygame.display.update()  # Update the display
        pygame.time.delay(16)  # Delay to create smooth transition

def main_menu():
    """Main menu loop."""
    data = read_player_data()
    streak = data.get("Streak", "0")
    running = True
    while running:
        # screen.fill(DARK_GRAY)
        screen.blit(BACKGROUND, (0, 0))

        draw_text("HabitsEscape", TITLE_FONT, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        streak_y = SCREEN_HEIGHT // 4 + 80
        draw_text(f"Streak: {streak}", QUESTION_FONT, WHITE, SCREEN_WIDTH // 2, streak_y)

        # Draw the streak text first
        streak_text = f"Streak: {streak}"
        streak_text_surface = QUESTION_FONT.render(streak_text, True, WHITE)
        streak_text_rect = streak_text_surface.get_rect(center=(SCREEN_WIDTH // 2, streak_y))
        screen.blit(streak_text_surface, streak_text_rect)

        # Now position the fire icon right next to the text
        fire_icon_rect = fire_icon.get_rect()
        fire_icon_rect.midleft = streak_text_rect.right, streak_y - 10  # Align fire icon to the right of the streak text

        # Blit the fire icon to the screen
        screen.blit(fire_icon, fire_icon_rect)

        play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40, 200, 60)
        quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 60)

        pygame.draw.rect(screen, GRAY, play_button_rect, border_radius=20)
        pygame.draw.rect(screen, GRAY, quit_button_rect, border_radius=20)

        draw_text("Play", BUTTON_FONT, WHITE, play_button_rect.centerx, play_button_rect.centery)
        draw_text("Quit", BUTTON_FONT, WHITE, quit_button_rect.centerx, quit_button_rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    fade_from_black()# Fade out before transitioning
                    os.system("python home.py")
                    pygame.quit()
                    return
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    return

        pygame.display.flip()

if __name__ == "__main__":
    ensure_data_file_exists()
    check_and_update_streak()
    player_data = read_player_data()
    if player_data.get("Addiction") == "None":
        addiction = choose_addiction()
    else:
        addiction = player_data["Addiction"]
    fade_to_black() 
    ask_question(addiction)
    fade_to_black()  
    main_menu()
