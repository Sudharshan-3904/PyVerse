# pygame_ui.py
# Main Pygame UI for PyVerse: handles menus, overlays, settings, and simulation launch.
# Provides user interaction, preset management, and simulation control.

import pygame
import sys
import json
import os
import glob
from config import CONFIG
from core.simulation_loop import run_simulation
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

def show_main_menu(config=None):
    """
    Main simulation menu loop. Handles simulation, overlays, and user input.
    Accepts a config dict to allow launching with a selected preset.
    """
    pygame.init()
    import os
    os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'
    screen = pygame.display.set_mode((800, 600), pygame.NOFRAME | pygame.RESIZABLE)
    pygame.display.set_caption("Universe Simulator")
    font = pygame.font.SysFont("Consolas", 16)
    clock = pygame.time.Clock()
    # Use provided config or default CONFIG
    sim_config = config if config is not None else CONFIG
    sim_generator = run_simulation(sim_config)
    running = True
    paused = False
    step_requested = False
    show_help = False
    show_presets = False
    show_settings = False
    presets = get_all_presets() + ["random"]
    preset_idx = 0
    while running:
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
                    # Add a particle at the cursor position with random velocity and mass
                    pos = pygame.mouse.get_pos()
                    width, height = screen.get_size()
                    sim_x = (pos[0] - width // 2) * 1e9 / (width // 2)
                    sim_y = (pos[1] - height // 2) * 1e9 / (height // 2)
                    sim_z = 0.0
                    import torch
                    vel = [torch.randn(1).item() * 0.1 for _ in range(3)]
                    mass = torch.rand(1).item() * 10.0
                    color = (
                        int(torch.rand(1).item() * 255),
                        int(torch.rand(1).item() * 255),
                        int(torch.rand(1).item() * 255)
                    )
                    # Add the particle to the simulation (handled in simulation_loop)
                    # Set a flag or call a callback if needed
                    # Here, we just pass as the actual addition is handled in simulation_loop
                    pass
                elif event.key == pygame.K_d:
                    # Remove the particle closest to the cursor
                    # Actual removal is handled in simulation_loop
                    pass
                elif event.key == pygame.K_h:
                    show_help = not show_help
                elif event.key == pygame.K_f or event.key == pygame.K_F1:
                    show_settings = not show_settings
                elif event.key == pygame.K_s:
                    # Save preset: prompt for name, only save if user confirms
                    preset_name = prompt_for_preset_name(screen, font)
                    if preset_name:
                        user_dir = os.path.join('assets', 'presets', 'user')
                        if not os.path.exists(user_dir):
                            os.makedirs(user_dir)
                        preset_path = os.path.join(user_dir, preset_name + '.json')
                        # Save current config (minimal example, expand as needed)
                        with open(preset_path, 'w') as f:
                            json.dump(CONFIG, f, indent=2)
                        # Update preset list
                        presets = get_all_presets() + ["random"]
                elif event.key == pygame.K_n:
                    step_requested = True
                elif event.key == pygame.K_UP and show_presets:
                    preset_idx = (preset_idx - 1) % len(presets)
                elif event.key == pygame.K_DOWN and show_presets:
                    preset_idx = (preset_idx + 1) % len(presets)
                elif event.key == pygame.K_RETURN and show_presets:
                    sim_config["preset"] = presets[preset_idx]
                    # Restart simulation with new preset
                    sim_generator = run_simulation(sim_config)
                    show_presets = False
                elif event.key == pygame.K_BACKSPACE and show_presets:
                    show_presets = False
        screen.fill((0, 0, 0))
        try:
            if not paused or step_requested:
                sim_state = next(sim_generator)
                step_requested = False
            particles = sim_state["particles"]
            stats = sim_state["stats"]
            step = sim_state["step"]
            paused = sim_state["paused"]
        except StopIteration:
            # Instead of break, just pause simulation and show message
            paused = True
            step = 0
            stats = {"cpu": 0, "ram": 0, "gpu": 0, "cpu_temp": 0, "gpu_temp": 0}
            particles = {"pos": [], "vel": [], "mass": []}
        render_scene(particles, sim_config)
        fps = clock.get_fps()
        # Only show the control_lines overlay (small font, blue color)
        control_lines = [
            f"Step: {step}",
            f"Status: {'PAUSED' if paused else 'RUNNING'}",
            "SPACE: Pause/Resume",
            "RIGHT: Step (when paused)",
            "A: Add particle at cursor",
            "D: Delete particle at cursor",
            "ESC: Quit"
        ]
        for i, line in enumerate(control_lines):
            text_surface = font.render(line, True, (200, 200, 255))
            screen.blit(text_surface, (10, 150 + i * 20))
        if show_help:
            show_help_screen(screen, font)
        if show_presets:
            show_preset_management(screen, font, presets, preset_idx)
        if show_settings:
            show_settings_menu(screen, font, CONFIG, {}, 0)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def launch_menu(config):
    """
    Launch the main menu for PyVerse. Handles user selection for simulation, benchmark, stress test, presets, and help.
    Args:
        config (dict): Initial configuration dictionary.
    Returns:
        dict or None: Updated config or None if exited.
    """
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("PyVerse - Galaxy Simulator Menu")
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    menu_items = [
        ("Start Simulation", "start"),
        ("Run Benchmark", "benchmark"),
        ("Run Stress Test", "stress"),
        ("Presets", "presets"),
        ("Help", "help"),
        ("Exit", "exit")
    ]
    selected = 0
    running = True
    show_help = False
    show_presets = False
    presets = get_all_presets() + ["random"]
    preset_idx = 0
    while running:
        screen.fill((10, 10, 30))
        for i, (text, _) in enumerate(menu_items):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            label = font.render(text, True, color)
            screen.blit(label, (60, 100 + i * 50))
        if show_help:
            show_help_screen(screen, font)
        if show_presets:
            show_preset_management(screen, font, presets, preset_idx)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if show_help:
                    if event.key == pygame.K_h:
                        show_help = False
                elif show_presets:
                    if event.key == pygame.K_UP:
                        preset_idx = (preset_idx - 1) % len(presets)
                    elif event.key == pygame.K_DOWN:
                        preset_idx = (preset_idx + 1) % len(presets)
                    elif event.key == pygame.K_RETURN:
                        config["preset"] = presets[preset_idx]
                        show_presets = False
                    elif event.key == pygame.K_BACKSPACE:
                        show_presets = False
                else:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        action = menu_items[selected][1]
                        print(f"Selected action: {action}")
                        if action == "exit":
                            pygame.quit()
                            return None
                        elif action == "start":
                            config["preset"] = presets[preset_idx] if presets else "random"
                            pygame.quit()
                            show_main_menu(config)  # Pass config to show_main_menu
                            return None
                        elif action == "benchmark":
                            config_bench = config.copy()
                            config_bench["benchmark_mode"] = True
                            pygame.quit()
                            # Run simulation in benchmark mode
                            sim_generator = run_simulation(config_bench)
                            for _ in sim_generator:
                                pass  # Run to completion
                            print("Benchmark completed.")
                            return None
                        elif action == "stress":
                            config_stress = config.copy()
                            config_stress["stress_test"] = True
                            pygame.quit()
                            # Run simulation in stress test mode
                            sim_generator = run_simulation(config_stress)
                            for _ in sim_generator:
                                pass  # Run to completion
                            print("Stress test completed.")
                            return None
                        elif action == "help":
                            show_help = True
                            while show_help:
                                screen.fill((10, 10, 30))
                                show_help_screen(screen, font)
                                pygame.display.flip()
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_h or event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                                        show_help = False
                        elif action == "presets":
                            show_presets = True
                            while show_presets:
                                screen.fill((10, 10, 30))
                                show_preset_management(screen, font, presets, preset_idx)
                                pygame.display.flip()
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_UP:
                                            preset_idx = (preset_idx - 1) % len(presets)
                                        elif event.key == pygame.K_DOWN:
                                            preset_idx = (preset_idx + 1) % len(presets)
                                        elif event.key == pygame.K_RETURN:
                                            config["preset"] = presets[preset_idx]
                                            show_presets = False
                                        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                                            show_presets = False
        pygame.display.flip()
        clock.tick(30)
