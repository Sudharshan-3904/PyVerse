import numpy as np
import torch
import json
import sys
import os

def initialize_particles(config):
    # Always start with a blank simulation (no objects)
    device = torch.device("cuda" if config.get("gpu_mode", False) and torch.cuda.is_available() else "cpu")
    pos = torch.empty((0, 3), dtype=torch.float32, device=device)
    vel = torch.empty((0, 3), dtype=torch.float32, device=device)
    mass = torch.empty((0, 1), dtype=torch.float32, device=device)
    return {"pos": pos, "vel": vel, "mass": mass}