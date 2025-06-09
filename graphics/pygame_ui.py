import pygame
import sys
import json
import os
from config import CONFIG
from core.simulation_loop import run_simulation
from graphics.vispy_renderer import render_scene
from utils.system_monitor import get_system_stats

def draw_overlay(screen, font, stats, fps):
    # Display system stats and FPS on the screen
    info_lines = [
        f"CPU: {stats['cpu']:.1f}%",
        f"RAM: {stats['ram']:.1f}%",
        f"GPU: {stats['gpu']:.1f}%",
        f"CPU Temp: {stats['cpu_temp']:.1f}°C",
        f"GPU Temp: {stats['gpu_temp']:.1f}°C",
        f"FPS: {fps:.2f}"
    ]
    for i, line in enumerate(info_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * 20))

def show_help_screen(screen, font):
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
    # Settings menu implementation
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
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((20, 20, 40, 220))
    title = font.render("Preset Management", True, (255, 255, 0))
    overlay.blit(title, (40, 40))
    for i, preset in enumerate(presets):
        color = (255, 255, 255) if i == selected_idx else (180, 180, 180)
        text = font.render(preset, True, color)
        overlay.blit(text, (60, 100 + i * 32))
    screen.blit(overlay, (0, 0))

def show_main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Universe Simulator")

    font = pygame.font.SysFont("Consolas", 16)
    clock = pygame.time.Clock()

    # Initialize the simulation generator
    sim_generator = run_simulation(CONFIG)

    # Control variables
    running = True
    paused = False
    step_requested = False
    show_help = False
    show_presets = False
    presets = ["solar_system", "random"]  # Example, should be loaded dynamically
    preset_idx = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Toggle pause
                    paused = not paused
                elif event.key == pygame.K_RIGHT and paused:
                    # Single step when paused
                    step_requested = True
                elif event.key == pygame.K_a:
                    # Add particle functionality is handled in simulation_loop.py
                    pass
                elif event.key == pygame.K_d:
                    # Remove particle functionality is handled in simulation_loop.py
                    pass
                elif event.key == pygame.K_h:
                    show_help = not show_help
                elif event.key == pygame.K_f:
                    # Toggle settings menu
                    pass  # Implement settings menu toggle
                elif event.key == pygame.K_s:
                    # Save preset functionality
                    pass  # Implement save preset
                elif event.key == pygame.K_n:
                    # Step simulation (when paused)
                    step_requested = True
                elif event.key == pygame.K_UP and show_presets:
                    preset_idx = (preset_idx - 1) % len(presets)
                elif event.key == pygame.K_DOWN and show_presets:
                    preset_idx = (preset_idx + 1) % len(presets)
                elif event.key == pygame.K_RETURN and show_presets:
                    CONFIG["preset"] = presets[preset_idx]
                    show_presets = False
                elif event.key == pygame.K_BACKSPACE and show_presets:
                    show_presets = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Get next simulation state from generator
        try:
            sim_state = next(sim_generator)
            particles = sim_state["particles"]
            stats = sim_state["stats"]
            step = sim_state["step"]
            # Update paused state from simulation
            paused = sim_state["paused"]
        except StopIteration:
            break

        # Render placeholder (VisPy for future)
        render_scene(particles, CONFIG)

        # Overlay stats and controls
        fps = clock.get_fps()
        draw_overlay(screen, font, stats, fps)
        
        # Display simulation controls
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

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def launch_menu(config):
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
    presets = ["solar_system", "random"]  # Example, should be loaded dynamically
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
                        if action == "exit":
                            pygame.quit()
                            return None
                        elif action == "start":
                            pygame.quit()
                            return config
                        elif action == "benchmark":
                            pygame.quit()
                            config_bench = config.copy()
                            config_bench["benchmark_mode"] = True
                            return config_bench
                        elif action == "stress":
                            pygame.quit()
                            config_stress = config.copy()
                            config_stress["stress_test"] = True
                            return config_stress
                        elif action == "help":
                            show_help = True
                        elif action == "presets":
                            show_presets = True
        pygame.display.flip()
        clock.tick(30)
