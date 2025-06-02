import torch

def compute_dark_matter_forces(particles, v0=200e3, G=6.67430e-11):
    """
    Simple dark matter model: flat rotation curve (heuristic).
    Applies a centripetal force to mimic dark matter halo.
    """
    pos = particles["pos"]
    n = pos.shape[0]
    forces = torch.zeros_like(pos)
    for i in range(n):
        r = torch.norm(pos[i]) + 1e-5
        # F = m v0^2 / r, direction is toward center
        f = -particles["mass"][i] * v0**2 * pos[i] / (r**2)
        forces[i] = f
    return forces