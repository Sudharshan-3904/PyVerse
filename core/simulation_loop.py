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
    if "names" not in particles:
        particles["names"] = [f"Particle_{i}" for i in range(particles["pos"].shape[0] - 1)]
    new_name = f"Particle_{len(particles['names'])}"
    particles["names"].append(new_name)
    
    from utils.logger import log_object_event
    log_object_event("ADDED", new_name, {
        "position": position, 
        "velocity": velocity, 
        "mass": mass, 
        "color": color
    })
    
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
    if "names" not in particles:
        particles["names"] = [f"Particle_{i}" for i in range(particles["pos"].shape[0] + 1)]
    
    removed_name = particles["names"][index]
    
    from utils.logger import log_object_event
    log_object_event("REMOVED", removed_name, {"index": index})
    
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
    
    # Log property / positional changes for tracking objects
    from utils.logger import log_all_particles_state
    log_all_particles_state(step, particles)
    
    return particles, stats

class SimulationSystem:
    def __init__(self, config):
        """Object-based simulation system."""
        self.config = config
        self.particles = initialize_particles(config)
        self.model_fn = select_model(config.get("interaction_model", "direct"))
        self.integrator = get_integrator(config.get("integration_method", "verlet"))
        self.step_count = 0
        self.stats = {"cpu": 0, "ram": 0, "gpu": 0}
        self.stats_update_interval = 60  # Update stats every 60 frames

    def update(self):
        """Perform a single iteration step of the simulation."""
        forces = self.model_fn(self.particles)
        self.particles = self.integrator(self.particles, forces, self.config)
        if self.step_count % self.stats_update_interval == 0:
            self.stats = get_system_stats()
        log_simulation_step(self.step_count, self.particles, self.stats)
        if self.step_count % 100 == 0:  # Log particles every 100 steps
            from utils.logger import log_all_particles_state
            log_all_particles_state(self.step_count, self.particles)
        self.step_count += 1

    def add_object(self, position, velocity, mass=1.0, color=(255, 255, 255)):
        """Add a custom object to the system."""
        self.particles = add_particle(self.particles, position, velocity, mass, color)

    def remove_closest_object(self, target_pos):
        """Remove the particle closest to a physical target position."""
        if self.particles["pos"].shape[0] > 1:
            p_pos = self.particles["pos"].cpu().numpy()
            distances = ((p_pos[:, 0] - target_pos[0]) ** 2 + 
                         (p_pos[:, 1] - target_pos[1]) ** 2) ** 0.5
            closest_idx = distances.argmin()
            self.particles = remove_particle(self.particles, closest_idx)

