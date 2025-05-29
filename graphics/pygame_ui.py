import pygame
import sys
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

def show_main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Universe Simulator")

    font = pygame.font.SysFont("Consolas", 16)
    clock = pygame.time.Clock()

    sim = run_simulation(CONFIG)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Simulation step
        try:
            particles = next(sim)
        except StopIteration:
            break

        # Render placeholder (VisPy for future)
        render_scene(particles, CONFIG)

        # Overlay stats
        stats = get_system_stats()
        fps = clock.get_fps()
        draw_overlay(screen, font, stats, fps)

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
        ("Exit", "exit")
    ]
    selected = 0
    running = True
    while running:
        screen.fill((10, 10, 30))
        for i, (text, _) in enumerate(menu_items):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            label = font.render(text, True, color)
            screen.blit(label, (60, 100 + i * 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
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
        pygame.display.flip()
        clock.tick(30)
