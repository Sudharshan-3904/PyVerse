import torch

def compute_gravity_forces(particles, G=6.67430e-11):
    pos = particles["pos"]
    mass = particles["mass"]
    n = pos.shape[0]
    forces = torch.zeros_like(pos)
    for i in range(n):
        diff = pos - pos[i]
        dist = torch.norm(diff, dim=1).unsqueeze(1) + 1e-5
        f = G * mass[i] * mass * diff / (dist ** 3)
        forces[i] = torch.sum(f, dim=0)
    return forces
