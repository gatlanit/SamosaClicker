import pygame as pg
import sys

# Setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("SAMOSA CLICKER")
FPS = pg.time.Clock()

# counter variable
samosa_count = 0
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

# Mini Powerup costs (unlock after first AutoClicker)
auto_speed_cost = 300
auto_power_cost = 500
auto_interval = 1000  # ms per auto clicker tick
auto_power = 1        # how many samosas each auto clicker produces

# Load image
samosa_original = pg.image.load("assets/samosa.png").convert_alpha()
samosa = samosa_original
samosa_rect = samosa.get_rect(center=(1280 // 2 - 100, 720 // 2))  # shift left for sidebar

# Setup font
font = pg.font.Font(None, 40)

# Predefine text position
text_pos = (samosa_rect.centerx, samosa_rect.top - 40)

# Scale effect
scale_up = False
scale_timer = 0
SCALE_DURATION = 150
SCALE_FACTOR = 1.1

# Timers for auto clicker
AUTO_CLICK_EVENT = pg.USEREVENT + 1
pg.time.set_timer(AUTO_CLICK_EVENT, auto_interval)

# Game Loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Click samosa
        if event.type == pg.MOUSEBUTTONDOWN:
            if samosa_rect.collidepoint(event.pos):
                samosa_count += click_multiplier
                scale_up = True
                scale_timer = pg.time.get_ticks()

            # Sidebar clicks
            mx, my = event.pos
            if mx > 950:  # inside sidebar
                if "double" in upgrade_buttons and upgrade_buttons["double"].collidepoint(event.pos):
                    if samosa_count >= double_click_cost:
                        samosa_count -= double_click_cost
                        click_multiplier = 2
                        double_unlocked = True

                elif "triple" in upgrade_buttons and upgrade_buttons["triple"].collidepoint(event.pos):
                    if samosa_count >= triple_click_cost:
                        samosa_count -= triple_click_cost
                        click_multiplier = 3
                        triple_unlocked = True

                elif "quad" in upgrade_buttons and upgrade_buttons["quad"].collidepoint(event.pos):
                    if samosa_count >= quad_click_cost:
                        samosa_count -= quad_click_cost
                        click_multiplier = 4
                        quad_unlocked = True

                elif "auto" in upgrade_buttons and upgrade_buttons["auto"].collidepoint(event.pos):
                    if samosa_count >= auto_clicker_cost:
                        samosa_count -= auto_clicker_cost
                        auto_clickers += 1
                        auto_clicker_cost = int(auto_clicker_cost * 1.5)

                elif "faster" in upgrade_buttons and upgrade_buttons["faster"].collidepoint(event.pos):
                    if samosa_count >= auto_speed_cost:
                        samosa_count -= auto_speed_cost
                        auto_interval = max(200, auto_interval - 200)
                        pg.time.set_timer(AUTO_CLICK_EVENT, auto_interval)
                        auto_speed_cost = int(auto_speed_cost * 1.8)

                elif "stronger" in upgrade_buttons and upgrade_buttons["stronger"].collidepoint(event.pos):
                    if samosa_count >= auto_power_cost:
                        samosa_count -= auto_power_cost
                        auto_power += 1
                        auto_power_cost = int(auto_power_cost * 2)

        # Auto clicker event
        if event.type == AUTO_CLICK_EVENT:
            samosa_count += auto_clickers * auto_power

    # Handle scaling
    if scale_up:
        elapsed = pg.time.get_ticks() - scale_timer
        if elapsed < SCALE_DURATION:
            new_size = (int(samosa_original.get_width() * SCALE_FACTOR),
                        int(samosa_original.get_height() * SCALE_FACTOR))
            samosa = pg.transform.smoothscale(samosa_original, new_size)
        else:
            samosa = samosa_original
            scale_up = False

    # Keep samosa centered (shift left for sidebar space)
    samosa_rect = samosa.get_rect(center=(1280 // 2 - 100, 720 // 2))

    # Fill background
    screen.fill((30, 30, 30))

    # Render samosa count
    text_surface = font.render(f"Samosa Count: {samosa_count}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, text_rect)

    # Draw samosa
    screen.blit(samosa, samosa_rect)

    # --- Sidebar Drawing ---
    pg.draw.rect(screen, (50, 50, 50), (950, 0, 330, 720))
    sidebar_title = font.render("Powerups", True, (255, 215, 0))
    screen.blit(sidebar_title, (1000, 40))

    upgrade_buttons = {}  # reset buttons each frame
    y = 100
    if not double_unlocked:
        text = font.render(f"Double Clicks - {double_click_cost}", True, (200, 200, 50))
        rect = text.get_rect(topleft=(960, y))
        screen.blit(text, rect)
        upgrade_buttons["double"] = rect
        y += 60

    if not triple_unlocked:
        text = font.render(f"Triple Clicks - {triple_click_cost}", True, (200, 200, 50))
        rect = text.get_rect(topleft=(960, y))
        screen.blit(text, rect)
        upgrade_buttons["triple"] = rect
        y += 60

    if not quad_unlocked:
        text = font.render(f"Quad Clicks - {quad_click_cost}", True, (200, 200, 50))
        rect = text.get_rect(topleft=(960, y))
        screen.blit(text, rect)
        upgrade_buttons["quad"] = rect
        y += 60

    # Auto clicker (always shown)
    text = font.render(f"Auto Clicker - {auto_clicker_cost}", True, (200, 200, 50))
    rect = text.get_rect(topleft=(960, y))
    screen.blit(text, rect)
    upgrade_buttons["auto"] = rect
    y += 60

    # Mini Powerups (only show if auto_clickers > 0)
    if auto_clickers > 0:
        text = font.render(f"Faster AutoClickers - {auto_speed_cost}", True, (150, 255, 150))
        rect = text.get_rect(topleft=(960, y))
        screen.blit(text, rect)
        upgrade_buttons["faster"] = rect
        y += 60

        text = font.render(f"Stronger AutoClickers - {auto_power_cost}", True, (150, 255, 150))
        rect = text.get_rect(topleft=(960, y))
        screen.blit(text, rect)
        upgrade_buttons["stronger"] = rect
        y += 60

    # Show current stats
    info_surface = font.render(
        f"Multiplier: x{click_multiplier} | Auto: {auto_clickers} (x{auto_power})", True, (100, 255, 100)
    )
    screen.blit(info_surface, (50, 650))

    # Update display
    pg.display.flip()
    FPS.tick(60)
