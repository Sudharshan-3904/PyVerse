import torch

def apply_relativity_corrections(particles, forces):
    """
    Post-Newtonian correction (1st order) for general relativity.
    Reduces force as velocity approaches speed of light.
    """
    c = 3e8  # Speed of light (m/s)
    vel = particles["vel"]
    v2 = torch.sum(vel**2, dim=1, keepdim=True)
    v2_over_c2 = torch.clamp(v2 / c**2, 0, 0.99)  # Prevent FTL
    gamma = 1.0 / torch.sqrt(1 - v2_over_c2 + 1e-10)
    # Correction: F' = F / gamma^3
    forces = forces / (gamma ** 3)
    return forces
