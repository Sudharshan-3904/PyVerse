import torch

def compute_electromagnetic_forces(particles, k=8.9875517923e9):
    """
    Compute electromagnetic (Coulomb) forces between charged particles.
    Assumes 'charge' field in particles dict.
    """
    pos = particles["pos"]
    charge = particles.get("charge", None)
    if charge is None:
        return torch.zeros_like(pos)
    n = pos.shape[0]
    forces = torch.zeros_like(pos)
    for i in range(n):
        diff = pos - pos[i]
        dist = torch.norm(diff, dim=1).unsqueeze(1) + 1e-5
        f = k * charge[i] * charge * diff / (dist ** 3)
        f[i] = 0  # No self-force
        forces[i] = torch.sum(f, dim=0)
    return forces
