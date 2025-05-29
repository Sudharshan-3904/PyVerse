import numpy as np
import torch
import json
import sys
import os

def initialize_particles(config):
    if config.get("preset") == "solar_system":
        preset_path = os.path.join(os.path.dirname(sys.argv[0]), "assets", "presets", "solar_system", "solar_system.json")
        with open(preset_path, "r") as f:
            data = json.load(f)
        bodies = data["bodies"]
        count = len(bodies)
        device = torch.device("cuda" if config.get("gpu_mode", False) and torch.cuda.is_available() else "cpu")
        pos = torch.tensor([b["position"] for b in bodies], dtype=torch.float64, device=device)
        vel = torch.tensor([b["velocity"] for b in bodies], dtype=torch.float64, device=device)
        mass = torch.tensor([[b["mass"]] for b in bodies], dtype=torch.float64, device=device)
        color = torch.tensor([b["color"] for b in bodies], dtype=torch.uint8, device="cpu")
        names = [b["name"] for b in bodies]
        return {"pos": pos, "vel": vel, "mass": mass, "color": color, "names": names}
    else:
        count = config.get("particle_count", 1000)
        device = torch.device("cuda" if config.get("gpu_mode", False) and torch.cuda.is_available() else "cpu")
        pos = torch.rand((count, 3), dtype=torch.float32, device=device) * 100.0
        vel = torch.randn((count, 3), dtype=torch.float32, device=device) * 0.1
        mass = torch.ones((count, 1), dtype=torch.float32, device=device)
        return {"pos": pos, "vel": vel, "mass": mass}