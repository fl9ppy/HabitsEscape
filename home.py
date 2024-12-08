import pygame
import os

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLAYER_SIZE = 140
PLAYER_START_POS = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
COMPUTER_POS = (200, 150)  # Position of the computer
COMPUTER_HITBOX = (150, 150)  # Larger hitbox for the computer
PORTAL_POS = (WINDOW_WIDTH - 500, WINDOW_HEIGHT - 600)  # Position of the portal
PORTAL_HITBOX = (100, 100)  # Smaller hitbox for the portal
PORTAL_SIZE = 200  # Size of the portal (image)
NEW_CHARACTER_POS = (500, WINDOW_HEIGHT - 200)  # Position of the new character
NEW_CHARACTER_SIZE = (180, 180)  # Size of the new character
BACKGROUND_IMAGE_PATH = "assets/scene/home.jpg"
PORTAL_IMAGES = ["assets/others/portaljos.png", "assets/others/portalsus.png"]  # Portal animation frames
PLAYER_MOVE_IMAGES = ["assets/modi/modi_mers_dreapra.png", "assets/modi/modi_mers_stanga.png"]
PLAYER_IDLE_IMAGE = "assets/modi/ial2.png"
NEW_CHARACTER_IMAGE_PATH = "assets/tibi/tiberiu.png"  # New character image
TEXT_BUBBLE_IMAGE = "assets/others/text_bubble.png"  # Text bubble PNG path
CUSTOM_FONT_PATH = "assets/others/8bit_font.ttf"  # Path to the custom font
TEXT_COLOR = (0, 0, 0)

def draw_text_bubble(screen, text, position, size1, size2, delta1, delta2):
    """Draws a text bubble using a PNG image and renders multiline text on it."""
    # Load the text bubble PNG
    text_bubble_image = pygame.image.load(TEXT_BUBBLE_IMAGE)
    text_bubble_image = pygame.transform.scale(text_bubble_image, (size1, size2))  # Scale the bubble
    font = pygame.font.Font(CUSTOM_FONT_PATH, 9)  # Adjust the font size if needed

    # Split the text into lines
    lines = text.split("\n")

    bubble_x, bubble_y = position
    screen.blit(text_bubble_image, (bubble_x, bubble_y))

    # Render each line of text
    for i, line in enumerate(lines):
        text_surface = font.render(line.strip(), True, TEXT_COLOR)
        text_x = bubble_x + delta1
        text_y = bubble_y + delta2 + i * 20  # Adjust line spacing with i * 20
        screen.blit(text_surface, (text_x, text_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Home Scene")
    clock = pygame.time.Clock()

    # Load assets
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    portal_frames = [pygame.transform.scale(pygame.image.load(img), (PORTAL_SIZE, PORTAL_SIZE)) for img in PORTAL_IMAGES]
    player_move_frames = [pygame.transform.scale(pygame.image.load(img), (PLAYER_SIZE, PLAYER_SIZE)) for img in PLAYER_MOVE_IMAGES]
    player_idle_image = pygame.transform.scale(pygame.image.load(PLAYER_IDLE_IMAGE), (PLAYER_SIZE, PLAYER_SIZE))
    new_character_image = pygame.transform.scale(pygame.image.load(NEW_CHARACTER_IMAGE_PATH), NEW_CHARACTER_SIZE)

    # Positions and hitboxes
    player_pos = list(PLAYER_START_POS)
    portal_hitbox_rect = pygame.Rect(PORTAL_POS[0] + 50, PORTAL_POS[1] + 50, PORTAL_HITBOX[0], PORTAL_HITBOX[1])
    computer_hitbox_rect = pygame.Rect(COMPUTER_POS[0] - 25, COMPUTER_POS[1] - 25, COMPUTER_HITBOX[0], COMPUTER_HITBOX[1])
    new_character_hitbox_rect = pygame.Rect(NEW_CHARACTER_POS[0], NEW_CHARACTER_POS[1], NEW_CHARACTER_SIZE[0], NEW_CHARACTER_SIZE[1])

    # Animation and state variables
    portal_animation_index = 0
    portal_animation_timer = pygame.time.get_ticks()
    portal_animation_delay = 1000  # Milliseconds between portal frames
    player_animation_index = 0
    player_animation_timer = pygame.time.get_ticks()
    player_animation_delay = 500
    player_facing_left = False

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
            player_facing_left = True
            moving = True
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 5
            player_facing_left = False
            moving = True
        if keys[pygame.K_UP]:
            player_pos[1] -= 5
            moving = True
        if keys[pygame.K_DOWN]:
            player_pos[1] += 5
            moving = True

        # Update animations
        if moving and current_time - player_animation_timer > player_animation_delay:
            player_animation_index = (player_animation_index + 1) % len(player_move_frames)
            player_animation_timer = current_time

        if current_time - portal_animation_timer > portal_animation_delay:
            portal_animation_index = (portal_animation_index + 1) % len(portal_frames)
            portal_animation_timer = current_time

        # Check for collisions
        player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
        near_computer = player_rect.colliderect(computer_hitbox_rect)
        near_new_character = player_rect.colliderect(new_character_hitbox_rect)

        # Check for portal collision
        if player_rect.colliderect(portal_hitbox_rect):
            pygame.quit()
            os.system("python main.py")  # Adjust the command if needed
            return

        # Draw the room
        screen.blit(background_image, (0, 0))
        screen.blit(portal_frames[portal_animation_index], (PORTAL_POS[0], PORTAL_POS[1]))
        screen.blit(new_character_image, NEW_CHARACTER_POS)

        # Render the player with animation and flipping
        if moving:
            player_image = player_move_frames[player_animation_index]
        else:
            player_image = player_idle_image

        if not player_facing_left:  # Flip the image when facing right
            player_image = pygame.transform.flip(player_image, True, False)

        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Show text bubble interactions
        if near_computer:
            draw_text_bubble(screen, "Fumatul iti poate irita ochii, nasul si gatul.", (COMPUTER_POS[0] - 200, COMPUTER_POS[1] - 80), 650, 300, 120, 105)
        if near_new_character:
            draw_text_bubble(screen,
                             """Buna dimineata baiete! Ia de aci 25 de lei sa mergi pana la Mega sa imi iei o placinta. 
        Dar nu uita, drumul este plin de vicii si pericole, nu pica in acele capcane. 
        De asemenea ma dor genunchii ceea ce inseamna ca va veni ploaia. 
        Ia de aici o umbrela baiete. 
        Drum bun!""",
                             (NEW_CHARACTER_POS[0] - 400, NEW_CHARACTER_POS[1] - 350),
                             1200, 600, 220, 185)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
