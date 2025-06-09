import torch
import numpy as np
from numba import njit, prange

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

def compute_direct_gravity(particles, G=6.67430e-11):
    """
    Direct N^2 gravity using Numba for CPU parallelism.
    Accepts particles as a dict with 'pos' and 'mass' as numpy arrays.
    Returns force as numpy array.
    """
    pos = particles["pos"].cpu().numpy()
    mass = particles["mass"].cpu().numpy().flatten()
    n = pos.shape[0]
    forces = np.zeros_like(pos)
    forces = _direct_gravity_numba(pos, mass, G)
    return torch.tensor(forces, dtype=particles["pos"].dtype, device=particles["pos"].device)

@njit(parallel=True)
def _direct_gravity_numba(pos, mass, G):
    n = pos.shape[0]
    forces = np.zeros_like(pos)
    for i in prange(n):
        f = np.zeros(3)
        for j in range(n):
            if i != j:
                diff = pos[j] - pos[i]
                dist = np.linalg.norm(diff) + 1e-5
                f += G * mass[i] * mass[j] * diff / (dist ** 3)
        forces[i] = f
    return forces
