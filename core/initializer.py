import numpy as np
import torch
import json
import sys
import os

def initialize_particles(config):
    device = torch.device("cuda" if config.get("gpu_mode", False) and torch.cuda.is_available() else "cpu")
    
    preset = config.get("preset")
    if preset and preset != "random":
        # Load from preset
        preset_dir = os.path.join(os.path.dirname(sys.argv[0]), "assets", "presets")
        preset_path = None
        for folder in os.listdir(preset_dir):
            folder_path = os.path.join(preset_dir, folder)
            if os.path.isdir(folder_path):
                json_path = os.path.join(folder_path, f"{preset}.json")
                if os.path.exists(json_path):
                    preset_path = json_path
                    break
        if preset_path:
            with open(preset_path, 'r') as f:
                data = json.load(f)
            bodies = data.get("bodies", [])
            n = len(bodies)
            pos = torch.zeros((n, 3), dtype=torch.float32, device=device)
            vel = torch.zeros((n, 3), dtype=torch.float32, device=device)
            mass = torch.zeros((n, 1), dtype=torch.float32, device=device)
            color = torch.zeros((n, 3), dtype=torch.uint8, device=device)
            for i, body in enumerate(bodies):
                pos[i] = torch.tensor(body["position"], dtype=torch.float32, device=device)
                vel[i] = torch.tensor(body["velocity"], dtype=torch.float32, device=device)
                mass[i, 0] = body["mass"]
                color[i] = torch.tensor(body["color"], dtype=torch.uint8, device=device)
            charge = torch.ones((n, 1), dtype=torch.float32, device=device)  # Default charge
            return {"pos": pos, "vel": vel, "mass": mass, "color": color, "charge": charge}
    
    # Default: random particles or based on particle_count
    particle_count = config.get("particle_count", 100)
    if particle_count == 0:
        pos = torch.empty((0, 3), dtype=torch.float32, device=device)
        vel = torch.empty((0, 3), dtype=torch.float32, device=device)
        mass = torch.empty((0, 1), dtype=torch.float32, device=device)
        charge = torch.empty((0, 1), dtype=torch.float32, device=device)
        return {"pos": pos, "vel": vel, "mass": mass, "charge": charge}
    
    pos = torch.randn((particle_count, 3), dtype=torch.float32, device=device) * 1e10
    vel = torch.randn((particle_count, 3), dtype=torch.float32, device=device) * 1e4
    mass = torch.ones((particle_count, 1), dtype=torch.float32, device=device) * 1e24  # Solar masses approx
    color = torch.randint(100, 256, (particle_count, 3), dtype=torch.uint8, device=device)
    charge = torch.ones((particle_count, 1), dtype=torch.float32, device=device)  # Default charge
    return {"pos": pos, "vel": vel, "mass": mass, "color": color, "charge": charge}