import pygame as pg
import sys

# --- Setup ---
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("SAMOSA CLICKER")
FPS = pg.time.Clock()

# --- Fonts ---
font = pg.font.Font(None, 36)
title_font = pg.font.Font(None, 72)

# --- Game variables ---
samosa_count = 0
click_multiplier = 1

double_click_cost = 50
triple_click_cost = 150
quad_click_cost = 400
auto_clicker_cost = 200

auto_clickers = 0
double_unlocked = False
triple_unlocked = False
quad_unlocked = False
auto_unlocked = False

auto_speed_cost = 300
auto_power_cost = 500
auto_interval = 1000
auto_power = 1

milestones = [100, 500, 2000, 5000, 10000]
reached_milestones = []

milestone_width = 250
sidebar_width = 330
middle_width = 1280 - milestone_width - sidebar_width

# Load Samosa image
samosa_original = pg.image.load("assets/samosa.png").convert_alpha()
samosa = samosa_original
samosa_rect = samosa.get_rect(center=(milestone_width + middle_width // 2, 720 // 2))

# Scale effect
scale_up = False
scale_timer = 0
SCALE_DURATION = 150
SCALE_FACTOR = 1.1

# AutoClicker timer
AUTO_CLICK_EVENT = pg.USEREVENT + 1
pg.time.set_timer(AUTO_CLICK_EVENT, auto_interval)

# Username
username = ""
active_input = True
game_started = False

# --- Helper function ---
def get_color(cost):
    return (200, 200, 50) if samosa_count >= cost else (100, 100, 100)

# --- Start Page Loop ---
while not game_started:
    screen.fill((30, 30, 30))

    # Title
    title_surf = title_font.render("SAMOSA CLICKER", True, (255, 215, 0))
    screen.blit(title_surf, (640 - title_surf.get_width() // 2, 100))

    # Instruction text
    instruction_surf = font.render("Enter your username:", True, (200, 200, 200))
    screen.blit(instruction_surf, (640 - instruction_surf.get_width() // 2, 250))

    # Username input box
    input_box = pg.Rect(540, 300, 200, 50)
    pg.draw.rect(screen, (255, 255, 255), input_box, 2)

    if username == "":
        # Placeholder when box is empty
        placeholder = font.render("Type here...", True, (150, 150, 150))
        screen.blit(placeholder, (input_box.x + 5, input_box.y + 10))
    else:
        username_surf = font.render(username, True, (255, 255, 255))
        screen.blit(username_surf, (input_box.x + 5, input_box.y + 10))

    # Start button
    start_button = pg.Rect(540, 400, 200, 50)
    pg.draw.rect(screen, (0, 200, 0), start_button)
    start_text = font.render("Start Game", True, (255, 255, 255))
    screen.blit(start_text, (start_button.x + 30, start_button.y + 10))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN and active_input:
            if event.key == pg.K_BACKSPACE:
                username = username[:-1]
            elif event.key == pg.K_RETURN:
                if username.strip() != "":
                    game_started = True
            else:
                if len(username) < 12:  # limit username length
                    username += event.unicode
        if event.type == pg.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos) and username.strip() != "":
                game_started = True

    pg.display.flip()
    FPS.tick(60)


# --- Main Game Loop ---
while True:
    screen.fill((30, 30, 30))

    # --- Milestone section (left) ---
    milestone_x = 0
    pg.draw.rect(screen, (40, 40, 60), (milestone_x, 0, milestone_width, 720))
    milestone_title = font.render("Milestones", True, (255, 215, 0))
    screen.blit(milestone_title, (milestone_x + 20, 40))
    y_m = 100
    for m in milestones:
        if samosa_count >= m and m not in reached_milestones:
            reached_milestones.append(m)
        text_color = (100, 255, 100) if m in reached_milestones else (180, 180, 180)
        text = font.render(f"{m} Samosas", True, text_color)
        screen.blit(text, (milestone_x + 20, y_m))
        y_m += 60

    # --- Samosa centered in middle area ---
    samosa_rect = samosa.get_rect(center=(milestone_width + middle_width // 2, 720 // 2))
    screen.blit(samosa, samosa_rect)

    # Samosa count above
    text_surface = font.render(f"{username}'s Samosas: {samosa_count}", True, (255, 255, 255))
    screen.blit(text_surface, (samosa_rect.centerx - text_surface.get_width() // 2, samosa_rect.top - 40))

    # --- Sidebar (right) ---
    sidebar_x = 1280 - sidebar_width
    pg.draw.rect(screen, (50, 50, 50), (sidebar_x, 0, sidebar_width, 720))
    sidebar_title = font.render("Powerups", True, (255, 215, 0))
    screen.blit(sidebar_title, (sidebar_x + 30, 40))

    upgrade_buttons = {}
    y = 100
    text_padding = 10

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

    # AutoClicker
    if not auto_unlocked:
        text = font.render(f"Auto - {auto_clicker_cost}", True, get_color(auto_clicker_cost))
        rect = text.get_rect(topleft=(sidebar_x + text_padding, y))
        screen.blit(text, rect)
        upgrade_buttons["auto"] = rect
        y += 60

    # Mini upgrades
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

    # Stats
    info_surface = font.render(f"Multiplier: x{click_multiplier} | Auto: {auto_clickers} (x{auto_power})", True, (100, 255, 100))
    screen.blit(info_surface, (milestone_width + 20, 650))

    # --- Events ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if samosa_rect.collidepoint(event.pos):
                samosa_count += click_multiplier
                scale_up = True
                scale_timer = pg.time.get_ticks()

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
                        auto_unlocked = True
                    elif key == "faster" and samosa_count >= auto_speed_cost:
                        samosa_count -= auto_speed_cost
                        auto_interval = max(200, auto_interval - 200)
                        pg.time.set_timer(AUTO_CLICK_EVENT, auto_interval)
                        auto_speed_cost = int(auto_speed_cost * 1.8)
                    elif key == "stronger" and samosa_count >= auto_power_cost:
                        samosa_count -= auto_power_cost
                        auto_power += 1
                        auto_power_cost = int(auto_power_cost * 2)

        if event.type == AUTO_CLICK_EVENT:
            samosa_count += auto_clickers * auto_power

    # --- Scale effect ---
    if scale_up:
        elapsed = pg.time.get_ticks() - scale_timer
        if elapsed < SCALE_DURATION:
            new_size = (
                int(samosa_original.get_width() * SCALE_FACTOR),
                int(samosa_original.get_height() * SCALE_FACTOR)
            )
            samosa = pg.transform.scale(samosa_original, new_size)
        else:
            samosa = samosa_original
            scale_up = False

    # --- Update display ---
    pg.display.flip()
    FPS.tick(60)