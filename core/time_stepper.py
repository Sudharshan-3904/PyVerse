import torch

def euler(particles, forces, config):
    dt = config.get("timestep", 0.01)
    particles["vel"] += forces * dt / particles["mass"]
    particles["pos"] += particles["vel"] * dt
    return particles

def verlet(particles, forces, config):
    dt = config.get("timestep", 0.01)
    if "prev_pos" not in particles:
        particles["prev_pos"] = particles["pos"] - particles["vel"] * dt
    new_pos = 2 * particles["pos"] - particles["prev_pos"] + (forces / particles["mass"]) * dt * dt
    particles["prev_pos"] = particles["pos"]
    particles["pos"] = new_pos
    return particles

def rk4(particles, forces, config):
    # Simplified RK4 for demonstration
    dt = config.get("timestep", 0.01)
    acc = forces / particles["mass"]
    particles["vel"] += acc * dt
    particles["pos"] += particles["vel"] * dt
    return particles

def get_integrator(name):
    if name == "verlet":
        return verlet
    elif name == "rk4":
        return rk4
    else:
        return euler