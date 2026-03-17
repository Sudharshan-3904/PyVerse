# pygame_ui.py
# Main Pygame UI for PyVerse: handles menus, overlays, settings, and simulation launch.
# Provides user interaction, preset management, and simulation control.

import math

import pygame
import sys
import json
import os
import glob
from config import CONFIG
from graphics.vispy_renderer import render_scene
from utils.system_monitor import get_system_stats

def draw_overlay(screen, font, stats, fps):
    """
    Draw system stats and FPS overlay on the screen.
    Args:
        screen: Pygame display surface.
        font: Pygame font object.
        stats (dict): System stats (cpu, ram, gpu, etc).
        fps (float): Current frames per second.
    """
    info_lines = [
        f"CPU: {stats.get('cpu', 0):.1f}%",
        f"RAM: {stats.get('ram', 0):.1f}%",
        f"GPU: {stats.get('gpu', 0):.1f}%",
        f"CPU Temp: {stats.get('cpu_temp', 0):.1f}°C",
        f"GPU Temp: {stats.get('gpu_temp', 0):.1f}°C",
        f"FPS: {fps:.2f}"
    ]
    for i, line in enumerate(info_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * 20))

def show_help_screen(screen, font):
    """
    Display the help screen with key bindings and controls.
    Args:
        screen: Pygame display surface.
        font: Pygame font object.
    """
    help_lines = [
        "Help - Key Bindings:",
        "F1: Toggle Settings Menu",
        "ESC: Quit Simulation",
        "S: Save Current Config as Preset (in settings)",
        "P: Pause/Resume Simulation",
        "N: Step Simulation (when paused)",
        "A: Add Particle",
        "D: Delete Particle",
        "H: Show/Hide Help Screen",
        "ENTER: Confirm Action (in dialogs)",
        "BACKSPACE: Cancel Action (in dialogs)",
    ]
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    for i, line in enumerate(help_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        overlay.blit(text_surface, (40, 40 + i * 32))
    screen.blit(overlay, (0, 0))

def show_confirmation_dialog(screen, font, message):
    """
    Show a confirmation dialog with a message and wait for user input.
    Args:
        screen: Pygame display surface.
        font: Pygame font object.
        message (str): Message to display.
    Returns:
        bool: True if confirmed, False if cancelled.
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    text_surface = font.render(message, True, (255, 100, 100))
    overlay.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 2 - 40))
    confirm_surface = font.render("ENTER: Confirm | BACKSPACE: Cancel", True, (255, 255, 255))
    overlay.blit(confirm_surface, (screen.get_width() // 2 - confirm_surface.get_width() // 2, screen.get_height() // 2 + 10))
    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    confirming = True
    while confirming:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    return False

def show_settings_menu(screen, font, config, settings_options, settings_idx):
    """
    Display the settings menu overlay.
    Args:
        screen: Pygame display surface.
        font: Pygame font object.
        config (dict): Current configuration.
        settings_options (dict): Settings options and values.
        settings_idx (int): Index of the selected option.
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((10, 10, 30, 220))
    title = font.render("Settings", True, (255, 255, 0))
    overlay.blit(title, (40, 40))
    for i, (option, value) in enumerate(settings_options.items()):
        color = (255, 255, 255) if i == settings_idx else (180, 180, 180)
        text = font.render(f"{option}: {value}", True, color)
        overlay.blit(text, (60, 100 + i * 32))
    screen.blit(overlay, (0, 0))

def show_preset_management(screen, font, presets, selected_idx):
    """
    Display the preset management overlay for selecting presets.
    Args:
        screen: Pygame display surface.
        font: Pygame font object.
        presets (list): List of preset names.
        selected_idx (int): Index of the selected preset.
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((20, 20, 40, 220))
    title = font.render("Preset Management", True, (255, 255, 0))
    overlay.blit(title, (40, 40))
    for i, preset in enumerate(presets):
        color = (255, 255, 255) if i == selected_idx else (180, 180, 180)
        text = font.render(preset, True, color)
        overlay.blit(text, (60, 100 + i * 32))
    screen.blit(overlay, (0, 0))

def get_all_presets():
    """
    Retrieve all available preset names from default and user directories.
    Returns:
        list: List of preset names (str).
    """
    preset_paths = glob.glob(os.path.join('assets', 'presets', 'Default', '*.json'))
    user_paths = glob.glob(os.path.join('assets', 'presets', 'user', '*.json'))
    preset_names = [os.path.splitext(os.path.basename(p))[0] for p in preset_paths]
    user_names = [os.path.splitext(os.path.basename(p))[0] for p in user_paths]
    return preset_names + user_names

def prompt_for_preset_name(screen, font):
    """
    Prompt the user to enter a name for a new preset.
    Args:
        screen: Pygame display surface.
        font: Pygame font object.
    Returns:
        str or None: Entered preset name, or None if cancelled.
    """
    input_box = pygame.Rect(200, 250, 400, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text.strip() if text.strip() else None
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                else:
                    text += event.unicode
        screen.fill((30, 30, 30))
        txt_surface = font.render('Enter preset name:', True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x, input_box.y - 40))
        box_surface = font.render(text, True, (255, 255, 0))
        width = max(400, box_surface.get_width()+10)
        input_box.w = width
        screen.blit(box_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
    return None

def draw_gradient_bg(screen):
    w, h = screen.get_size()
    for y in range(h):
        c = int(25 - (y / h) * 15)
        pygame.draw.line(screen, (c, c, c + 15), (0, y), (w, y))

def draw_button(screen, rect, text, font, hovered=False, selected=False):
    import pygame.gfxdraw
    color = (60, 100, 200) if hovered else (40, 60, 100)
    if selected:
        color = (100, 150, 255)
    
    border_radius = 12
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, (200, 200, 255), rect, width=2, border_radius=border_radius)
    
    label = font.render(text, True, (255, 255, 255))
    text_rect = label.get_rect(center=rect.center)
    screen.blit(label, text_rect)

def show_main_menu(config=None, create_mode=False):
    """
    Main simulation execution window. Can start in 'create_mode' or standard.
    Now utilizes the object-oriented SimulationSystem backend.
    """
    os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("PyVerse Explorer")
    
    font = pygame.font.SysFont("Segoe UI", 18)
    title_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
    
    clock = pygame.time.Clock()
    
    from core.simulation_loop import SimulationSystem
    sim_config = config if config is not None else CONFIG.copy()
    if create_mode:
        sim_config["preset"] = "random" # start empty or random if needed
        # Or you can zero out particles
        sim_config["particle_count"] = 0
        
    system = SimulationSystem(sim_config)
    
    running = True
    paused = create_mode
    step_requested = False
    
    import torch
    
    overlay_enabled = True
    
    while running:
        w, h = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RIGHT and paused:
                    step_requested = True
                elif event.key == pygame.K_a:
                    if w // 2 > 0:
                        sim_x = (mouse_pos[0] - w // 2) * 1e9 / (w // 2)
                        sim_y = (mouse_pos[1] - h // 2) * 1e9 / (h // 2)
                        vel = [torch.randn(1).item() * 0.1 for _ in range(3)]
                        system.add_object([sim_x, sim_y, 0.0], vel)
                elif event.key == pygame.K_s and create_mode:
                    # 'S' shortcut to add a massive star
                    if w // 2 > 0:
                        sim_x = (mouse_pos[0] - w // 2) * 1e9 / (w // 2)
                        sim_y = (mouse_pos[1] - h // 2) * 1e9 / (h // 2)
                        system.add_object([sim_x, sim_y, 0.0], [0.0, 0.0, 0.0], mass=10000.0, color=(255, 200, 50))
                elif event.key == pygame.K_d:
                    if w // 2 > 0:
                        sim_x = (mouse_pos[0] - w // 2) * 1e9 / (w // 2)
                        sim_y = (mouse_pos[1] - h // 2) * 1e9 / (h // 2)
                        system.remove_closest_object([sim_x, sim_y])
                elif event.key == pygame.K_h:
                    overlay_enabled = not overlay_enabled
            elif event.type == pygame.MOUSEBUTTONDOWN and create_mode:
                if event.button == 1: # Left click add planet
                    if w // 2 > 0:
                        sim_x = (mouse_pos[0] - w // 2) * 1e9 / (w // 2)
                        sim_y = (mouse_pos[1] - h // 2) * 1e9 / (h // 2)
                        vel = [torch.randn(1).item() * 0.1 for _ in range(3)]
                        system.add_object([sim_x, sim_y, 0.0], vel, mass=1.0)

        # Simulation Tick
        if not paused or step_requested:
            try:
                system.update()
                step_requested = False
            except Exception as e:
                print(f"Simulation Error: {e}")
                paused = True
                
        # Pure Renderer bypass for pygame fallback since vispy handles it elsewhere!
        # Assuming render_scene uses VisPy and takes foreground, Pygame provides just text overlay.
        # But if VisPy is intercepting, we fallback to drawing physically here for generic visualization
        screen.fill((5, 5, 12))
        
        if system.particles["pos"].shape[0] > 0:
            pos = system.particles["pos"].cpu().numpy()
            mass = system.particles["mass"].cpu().numpy().flatten()
            if "color" in system.particles:
                color = system.particles["color"].cpu().numpy()
            else:
                color = [(200, 200, 255)] * pos.shape[0]

            for i, p in enumerate(pos):
                nx = int(w // 2 + p[0] / 1e9 * (w // 2))
                ny = int(h // 2 + p[1] / 1e9 * (h // 2))
                if 0 <= nx <= w and 0 <= ny <= h:
                    m = float(mass[i]) if i < len(mass) else 1.0
                    # Size based on mass (log scale), clamped for visibility
                    radius = int(min(max((math.log10(m + 1e-12) - 22) * 0.8 + 2, 2), 12))
                    if m > 1e28:
                        # Render a soft glow for stars
                        glow = radius * 3
                        glow_surf = pygame.Surface((glow * 2, glow * 2), pygame.SRCALPHA)
                        glow_color = tuple(list(color[i])[:3]) + [45]
                        pygame.draw.circle(glow_surf, glow_color, (glow, glow), glow)
                        screen.blit(glow_surf, (nx - glow, ny - glow))
                        pygame.draw.circle(screen, tuple(color[i]), (nx, ny), radius + 1)
                    else:
                        pygame.draw.circle(screen, tuple(color[i]), (nx, ny), radius)

        if overlay_enabled:
            # Stats backdrop HUD
            hud_rect = pygame.Rect(10, 10, 320, 160)
            pygame.draw.rect(screen, (15, 20, 35, 200), hud_rect, border_radius=10)
            pygame.draw.rect(screen, (50, 70, 120), hud_rect, width=2, border_radius=10)

            title = title_font.render("PyVerse Engine", True, (255, 200, 100))
            screen.blit(title, (20, 20))

            fps = clock.get_fps()

            lines = [
                f"Status: {'PAUSED' if paused else 'RUNNING'}",
                f"Tick: {system.step_count} | FPS: {fps:.1f}",
                f"Objects: {system.particles['pos'].shape[0]}",
                f"CPU: {system.stats.get('cpu',0):.1f}% | RAM: {system.stats.get('ram',0):.1f}%"
            ]

            for i, line in enumerate(lines):
                txt = font.render(line, True, (230, 240, 255))
                screen.blit(txt, (20, 60 + i * 25))

            # Controls/Commands (bottom-right)
            controls = [
                "SPACE: Play/Pause",
                "ESC: Quit",
                "A: Add object",
                "D: Remove closest",
                "H: Toggle HUD",
            ]
            if create_mode:
                controls.append("L-Click: Add planet | S: Add star")

            line_height = 22
            for i, ctrl in enumerate(reversed(controls)):
                txt = font.render(ctrl, True, (200, 255, 200))
                rect = txt.get_rect()
                rect.bottomright = (w - 20, h - 20 - i * line_height)
                screen.blit(txt, rect)
        
        pygame.display.flip()
        clock.tick(60 if not sim_config.get("benchmark_mode") else 0)
        
    pygame.quit()

def launch_menu(config):
    """Refined and visually appealing entry lobby menu."""
    pygame.init()
    screen = pygame.display.set_mode((900, 550))
    pygame.display.set_caption("Welcome to PyVerse")
    
    title_font = pygame.font.SysFont("Segoe UI", 56, bold=True)
    subtitle_font = pygame.font.SysFont("Segoe UI", 20, italic=True)
    btn_font = pygame.font.SysFont("Segoe UI", 22, bold=True)
    
    clock = pygame.time.Clock()
    
    from core.simulation_loop import SimulationSystem
    
    menu_items = [
        {"id": "start", "label": "Start Default Simulation"},
        {"id": "create", "label": "Create Custom System"},
        {"id": "benchmark", "label": "Run Benchmark"},
        {"id": "stress", "label": "Run Stress Test"},
        {"id": "exit", "label": "Exit"}
    ]
    
    running = True
    hovered_idx = -1
    
    while running:
        draw_gradient_bg(screen)
        
        # Draw floating stars or simple accent points
        for _ in range(30):
            import random
            x = random.randint(0, 900)
            y = random.randint(0, 550)
            pygame.draw.circle(screen, (255, 255, 255, 50), (x, y), 1 if random.random() > 0.5 else 2)
            
        mouse_pos = pygame.mouse.get_pos()
        hovered_idx = -1
        
        title = title_font.render("P Y V E R S E", True, (255, 255, 255))
        sub = subtitle_font.render("Galaxy-Scale Physics Sandbox", True, (180, 200, 255))
        
        screen.blit(title, (900 // 2 - title.get_width() // 2, 60))
        screen.blit(sub, (900 // 2 - sub.get_width() // 2, 130))
        
        start_y = 220
        buttons = []
        for i, item in enumerate(menu_items):
            rect = pygame.Rect(900 // 2 - 150, start_y + i * 55, 300, 45)
            buttons.append((rect, item))
            is_hovered = rect.collidepoint(mouse_pos)
            if is_hovered:
                hovered_idx = i
            draw_button(screen, rect, item["label"], btn_font, hovered=is_hovered)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered_idx != -1:
                    action = menu_items[hovered_idx]["id"]
                    
                    if action == "exit":
                        pygame.quit()
                        return
                    elif action == "start":
                        pygame.quit()
                        show_main_menu(config, create_mode=False)
                        return
                    elif action == "create":
                        pygame.quit()
                        show_main_menu(config, create_mode=True)
                        return
                    elif action == "benchmark":
                        from utils.benchmark import run_benchmarks
                        pygame.quit()
                        run_benchmarks(SimulationSystem, ["solar_system", "binary_star", "three_body"])
                        return
                    elif action == "stress":
                        from utils.stress_tester import run_stress_test
                        pygame.quit()
                        run_stress_test(SimulationSystem, config)
                        return
                        
        pygame.display.flip()
        clock.tick(60)

