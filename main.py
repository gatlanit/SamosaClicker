import pygame as pg
import sys

# Setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("SAMOSA CLICKER")
FPS = pg.time.Clock()

# Counter and multipliers
samosa_count = 100000
click_multiplier = 1

# Upgrade costs
double_click_cost = 50
triple_click_cost = 150
quad_click_cost = 400
auto_clicker_cost = 200

# Upgrade states
auto_clickers = 0
double_unlocked = False
triple_unlocked = False
quad_unlocked = False
auto_unlocked = False  # New flag to track Auto purchase

# Mini Powerups (unlock after AutoClicker)
auto_speed_cost = 300
auto_power_cost = 500
auto_interval = 1000  # ms per tick
auto_power = 1         # samosas per auto click

# Load image
samosa_original = pg.image.load("assets/samosa.png").convert_alpha()
samosa = samosa_original
samosa_rect = samosa.get_rect(center=(1280 // 2 - 100, 720 // 2))

# Font
font = pg.font.Font(None, 36)  # slightly smaller font
text_pos = (samosa_rect.centerx, samosa_rect.top - 40)

# Scale effect
scale_up = False
scale_timer = 0
SCALE_DURATION = 150
SCALE_FACTOR = 1.1

# AutoClicker timer
AUTO_CLICK_EVENT = pg.USEREVENT + 1
pg.time.set_timer(AUTO_CLICK_EVENT, auto_interval)

# Helper for affordable color
def get_color(cost):
    return (200, 200, 50) if samosa_count >= cost else (100, 100, 100)

# Game loop
while True:
    # Fill background and draw samosa
    screen.fill((30, 30, 30))
    samosa_rect = samosa.get_rect(center=(1280 // 2 - 100, 720 // 2))
    screen.blit(samosa, samosa_rect)
    text_surface = font.render(f"Samosa Count: {samosa_count}", True, (255, 255, 255))
    screen.blit(text_surface, (samosa_rect.centerx - text_surface.get_width() // 2, samosa_rect.top - 40))

    # --- Sidebar ---
    sidebar_x = 950
    sidebar_width = 330
    pg.draw.rect(screen, (50, 50, 50), (sidebar_x, 0, sidebar_width, 720))
    sidebar_title = font.render("Powerups", True, (255, 215, 0))
    screen.blit(sidebar_title, (sidebar_x + 30, 40))  # left padding

    upgrade_buttons = {}
    y = 100
    text_padding = 10  # left padding inside sidebar

    # Multipliers
    if not double_unlocked:
        text = font.render(f"Double - {double_click_cost}", True, get_color(double_click_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["double"] = rect
        y += 60

    if not triple_unlocked:
        text = font.render(f"Triple - {triple_click_cost}", True, get_color(triple_click_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["triple"] = rect
        y += 60

    if not quad_unlocked:
        text = font.render(f"Quad - {quad_click_cost}", True, get_color(quad_click_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["quad"] = rect
        y += 60

    # AutoClicker - only show if not purchased
    if not auto_unlocked:
        text = font.render(f"Auto - {auto_clicker_cost}", True, get_color(auto_clicker_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["auto"] = rect
        y += 60

    # Mini Powerups - only if Auto purchased
    if auto_unlocked:
        text = font.render(f"Faster Auto - {auto_speed_cost}", True, get_color(auto_speed_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["faster"] = rect
        y += 60

        text = font.render(f"Stronger Auto - {auto_power_cost}", True, get_color(auto_power_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["stronger"] = rect
        y += 60

    # Show stats
    info_surface = font.render(f"Multiplier: x{click_multiplier} | Auto: {auto_clickers} (x{auto_power})", True, (100, 255, 100))
    screen.blit(info_surface, (50, 650))

    # --- Event handling ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            # Click samosa
            if samosa_rect.collidepoint(event.pos):
                samosa_count += click_multiplier
                scale_up = True
                scale_timer = pg.time.get_ticks()

            # Click upgrades
            for key, rect in upgrade_buttons.items():
                if rect.collidepoint(event.pos):
                    if key == "double" and samosa_count >= double_click_cost:
                        samosa_count -= double_click_cost
                        click_multiplier = 2
                        double_unlocked = True
                    elif key == "triple" and samosa_count >= triple_click_cost:
                        samosa_count -= triple_click_cost
                        click_multiplier = 3
                        triple_unlocked = True
                    elif key == "quad" and samosa_count >= quad_click_cost:
                        samosa_count -= quad_click_cost
                        click_multiplier = 4
                        quad_unlocked = True
                    elif key == "auto" and samosa_count >= auto_clicker_cost:
                        samosa_count -= auto_clicker_cost
                        auto_clickers += 1
                        auto_clicker_cost = int(auto_clicker_cost * 1.5)
                        auto_unlocked = True  # now purchased, remove "Auto" button
                    elif key == "faster" and samosa_count >= auto_speed_cost:
                        samosa_count -= auto_speed_cost
                        auto_interval = max(200, auto_interval - 200)
                        pg.time.set_timer(AUTO_CLICK_EVENT, auto_interval)
                        auto_speed_cost = int(auto_speed_cost * 1.8)
                    elif key == "stronger" and samosa_count >= auto_power_cost:
                        samosa_count -= auto_power_cost
                        auto_power += 1
                        auto_power_cost = int(auto_power_cost * 2)

        # AutoClicker event
        if event.type == AUTO_CLICK_EVENT:
            samosa_count += auto_clickers * auto_power

    # --- Scale effect ---
    if scale_up:
        elapsed = pg.time.get_ticks() - scale_timer
        if elapsed < SCALE_DURATION:
            new_size = (int(samosa_original.get_width() * SCALE_FACTOR),
                        int(samosa_original.get_height() * SCALE_FACTOR))
            samosa = pg.transform.smoothscale(samosa_original, new_size)
        else:
            samosa = samosa_original
            scale_up = False

    # Draw samosa again (keep centered)
    samosa_rect = samosa.get_rect(center=(1280 // 2 - 100, 720 // 2))
    screen.blit(samosa, samosa_rect)

    # Update display
    pg.display.flip()
    FPS.tick(60)
