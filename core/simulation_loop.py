import pygame
import sys
import json
import torch
from core.initializer import initialize_particles
from core.interaction_model import select_model
from core.time_stepper import get_integrator
from utils.logger import log_simulation_step
from utils.system_monitor import get_system_stats
import time
import os
import glob

SETTINGS_LIST = [
    ("fps", int),
    ("particle_count", int),
    ("gpu_mode", bool),
    ("integration_method", str),
    ("interaction_model", str),
    ("preset", str),
]

SETTINGS_OPTIONS = {
    "fps": [30, 60, 120],
    "particle_count": [9, 100, 1000, 10000],
    "gpu_mode": [True, False],
    "integration_method": ["euler", "verlet", "rk4"],
    "interaction_model": ["direct", "barnes_hut"],
    "preset": []  # Will be filled dynamically
}

PRESET_DIR = os.path.join(os.path.dirname(sys.argv[0]), "assets", "presets")
USER_PRESET_DIR = os.path.join(PRESET_DIR, "user")

def get_all_presets():
    preset_names = []
    for folder in os.listdir(PRESET_DIR):
        folder_path = os.path.join(PRESET_DIR, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    preset_names.append(file[:-5])
    return preset_names

def save_config_to_file(config, config_path):
    # Only save relevant keys
    lines = ["CONFIG = {\n"]
    for k, v in config.items():
        if isinstance(v, str):
            lines.append(f'    "{k}": "{v}",\n')
        else:
            lines.append(f'    "{k}": {repr(v)},\n')
    lines.append("}\n")
    with open(config_path, "w") as f:
        f.writelines(lines)

def add_particle(particles, position, velocity, mass=1.0, color=(255, 255, 255)):
    """Add a new particle to the simulation."""
    device = particles["pos"].device
    dtype = particles["pos"].dtype
    
    # Convert inputs to tensors with matching device and dtype
    pos_tensor = torch.tensor([position], dtype=dtype, device=device)
    vel_tensor = torch.tensor([velocity], dtype=dtype, device=device)
    mass_tensor = torch.tensor([[mass]], dtype=dtype, device=device)
    
    # Concatenate with existing particles
    particles["pos"] = torch.cat([particles["pos"], pos_tensor], dim=0)
    particles["vel"] = torch.cat([particles["vel"], vel_tensor], dim=0)
    particles["mass"] = torch.cat([particles["mass"], mass_tensor], dim=0)
    
    # Handle color if present
    if "color" in particles:
        color_tensor = torch.tensor([color], dtype=torch.uint8, device="cpu")
        particles["color"] = torch.cat([particles["color"], color_tensor], dim=0)
    
    # Handle names if present
    if "names" in particles:
        particles["names"].append(f"Particle_{len(particles['names'])}")
    
    return particles

def remove_particle(particles, index):
    """Remove a particle from the simulation by index."""
    if index < 0 or index >= particles["pos"].shape[0]:
        return particles  # Invalid index
    
    # Remove the particle at the specified index
    particles["pos"] = torch.cat([particles["pos"][:index], particles["pos"][index+1:]], dim=0)
    particles["vel"] = torch.cat([particles["vel"][:index], particles["vel"][index+1:]], dim=0)
    particles["mass"] = torch.cat([particles["mass"][:index], particles["mass"][index+1:]], dim=0)
    
    # Handle color if present
    if "color" in particles:
        particles["color"] = torch.cat([particles["color"][:index], particles["color"][index+1:]], dim=0)
    
    # Handle names if present
    if "names" in particles:
        particles["names"] = particles["names"][:index] + particles["names"][index+1:]
    
    return particles

def simulation_step(particles, model_fn, integrator, config, step):
    """Perform a single simulation step."""
    # Compute forces
    forces = model_fn(particles)
    # Integrate
    particles = integrator(particles, forces, config)
    # Log and monitor
    stats = get_system_stats()
    log_simulation_step(step, particles, stats)
    return particles, stats

def run_simulation(config):
    """Generator-based simulation loop that yields after each step."""
    import torch  # Import here to ensure it's available
    
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption("PyVerse - Simulation")
    font = pygame.font.SysFont("Consolas", 20)
    clock = pygame.time.Clock()
    settings_idx = 0
    editing = False
    edit_buffer = ""
    running = True
    step = 0
    stats = {}
    particles = initialize_particles(config)
    model_fn = select_model(config.get("interaction_model", "direct"))
    integrator = get_integrator(config.get("integration_method", "verlet"))
    # Update preset list dynamically
    SETTINGS_OPTIONS["preset"] = get_all_presets() + ["random"]
    
    # Simulation state
    paused = False
    single_step = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    editing = not editing
                elif event.key == pygame.K_SPACE:
                    # Toggle pause
                    paused = not paused
                elif event.key == pygame.K_RIGHT and paused:
                    # Single step when paused
                    single_step = True
                elif event.key == pygame.K_a:
                    # Add random particle at cursor position
                    pos = pygame.mouse.get_pos()
                    # Convert screen coordinates to simulation coordinates
                    sim_x = (pos[0] - width // 2) * 1e9 / (width // 2)
                    sim_y = (pos[1] - height // 2) * 1e9 / (height // 2)
                    sim_z = 0.0  # Default to z=0 plane
                    # Random velocity
                    vel = [torch.randn(1).item() * 0.1 for _ in range(3)]
                    particles = add_particle(
                        particles, 
                        [sim_x, sim_y, sim_z], 
                        vel,
                        mass=torch.rand(1).item() * 10.0,
                        color=(
                            int(torch.rand(1).item() * 255),
                            int(torch.rand(1).item() * 255),
                            int(torch.rand(1).item() * 255)
                        )
                    )
                elif event.key == pygame.K_d:
                    # Remove particle closest to cursor
                    if particles["pos"].shape[0] > 1:  # Ensure at least one particle remains
                        pos = pygame.mouse.get_pos()
                        sim_x = (pos[0] - width // 2) * 1e9 / (width // 2)
                        sim_y = (pos[1] - height // 2) * 1e9 / (height // 2)
                        
                        # Find closest particle
                        particle_pos = particles["pos"].cpu().numpy()
                        distances = ((particle_pos[:, 0] - sim_x) ** 2 + 
                                    (particle_pos[:, 1] - sim_y) ** 2) ** 0.5
                        closest_idx = distances.argmin()
                        particles = remove_particle(particles, closest_idx)
                elif editing:
                    if event.key == pygame.K_UP:
                        settings_idx = (settings_idx - 1) % len(SETTINGS_LIST)
                    elif event.key == pygame.K_DOWN:
                        settings_idx = (settings_idx + 1) % len(SETTINGS_LIST)
                    elif event.key == pygame.K_LEFT:
                        key, typ = SETTINGS_LIST[settings_idx]
                        options = SETTINGS_OPTIONS[key]
                        idx = options.index(config.get(key, options[0]))
                        config[key] = options[(idx - 1) % len(options)]
                        if key == "preset":
                            particles = initialize_particles(config)
                    elif event.key == pygame.K_RIGHT:
                        key, typ = SETTINGS_LIST[settings_idx]
                        options = SETTINGS_OPTIONS[key]
                        idx = options.index(config.get(key, options[0]))
                        config[key] = options[(idx + 1) % len(options)]
                        if key == "preset":
                            particles = initialize_particles(config)
                    elif event.key == pygame.K_s:
                        # Save current config as a user preset
                        if not os.path.exists(USER_PRESET_DIR):
                            os.makedirs(USER_PRESET_DIR)
                        preset_name = f"user_preset_{int(time.time())}.json"
                        preset_path = os.path.join(USER_PRESET_DIR, preset_name)
                        # Save only relevant config keys
                        preset_data = {
                            "config": {k: config[k] for k in config if k in dict(SETTINGS_LIST)}
                        }
                        with open(preset_path, "w") as f:
                            json.dump(preset_data, f, indent=2)
        
        # Update simulation if not paused or if single step requested
        if not paused or single_step:
            particles, stats = simulation_step(particles, model_fn, integrator, config, step)
            step += 1
            single_step = False  # Reset single step flag
        
        # Render (draw particles)
        screen.fill((0, 0, 0))
        pos = particles["pos"].cpu().numpy()
        if "color" in particles:
            color = particles["color"].numpy()
        else:
            color = [(255, 255, 255)] * pos.shape[0]
        for i, p in enumerate(pos):
            x = int(width // 2 + p[0] / 1e9 * (width // 2))
            y = int(height // 2 + p[1] / 1e9 * (height // 2))
            pygame.draw.circle(screen, tuple(color[i]), (x, y), 6 if config.get("preset") == "solar_system" else 2)
        
        # Overlay stats
        overlay_lines = [
            f"Step: {step}",
            f"FPS: {clock.get_fps():.2f}",
            f"Particles: {particles['pos'].shape[0]}",
            f"CPU: {stats.get('cpu', 0):.1f}% RAM: {stats.get('ram', 0):.1f}% GPU: {stats.get('gpu', 0):.1f}%",
            f"Status: {'PAUSED' if paused else 'RUNNING'}",
            "F1: Settings | SPACE: Pause/Resume | RIGHT: Step | A: Add | D: Delete | ESC: Quit"
        ]
        for i, line in enumerate(overlay_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (20, 20 + i * 28))
        
        # Settings menu
        if editing:
            pygame.draw.rect(screen, (30, 30, 60), (width - 400, 0, 400, height))
            for i, (key, typ) in enumerate(SETTINGS_LIST):
                val = config.get(key, "")
                color = (255, 255, 0) if i == settings_idx else (200, 200, 200)
                text = f"{key}: {val}"
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (width - 380, 40 + i * 40))
            # Show available presets
            preset_list = SETTINGS_OPTIONS["preset"]
            preset_title = font.render("Available Presets:", True, (180, 220, 255))
            screen.blit(preset_title, (width - 380, 320))
            for j, preset in enumerate(preset_list):
                pcolor = (255, 255, 255) if preset == config.get("preset") else (180, 180, 180)
                ptext = font.render(preset, True, pcolor)
                screen.blit(ptext, (width - 380, 350 + j * 28))
            # Show save instructions
            save_text = font.render("S: Save as user preset", True, (200, 255, 200))
            screen.blit(save_text, (width - 380, height - 60))
        
        pygame.display.flip()
        clock.tick(config.get("fps", 60))
        
        # Yield current state to allow external control
        yield {
            "particles": particles,
            "stats": stats,
            "step": step,
            "paused": paused
        }
    
    # Save config on quit
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.py")
    save_config_to_file(config, config_path)
    pygame.quit()
