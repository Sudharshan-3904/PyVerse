import torch

def compute_fluid_dynamics(particles, h=1.0, rho0=1.0, k=1.0, mu=0.1):
    """
    Minimal SPH (Smoothed Particle Hydrodynamics) force implementation.
    Assumes 'pos', 'vel', and 'mass' in particles dict.
    """
    pos = particles["pos"]
    vel = particles["vel"]
    mass = particles["mass"].flatten()
    n = pos.shape[0]
    forces = torch.zeros_like(pos)
    rho = torch.zeros(n, device=pos.device)
    for i in range(n):
        r_ij = pos - pos[i]
        dist = torch.norm(r_ij, dim=1)
        W = torch.exp(-dist**2 / (h**2))
        rho[i] = torch.sum(mass * W)
    for i in range(n):
        f_pressure = torch.zeros(3, device=pos.device)
        f_visc = torch.zeros(3, device=pos.device)
        for j in range(n):
            if i != j:
                r = pos[i] - pos[j]
                dist = torch.norm(r) + 1e-5
                W_grad = -2 * r * torch.exp(-dist**2 / (h**2)) / (h**2)
                f_pressure += -mass[j] * (k * (rho[i] - rho0) / rho[i]**2 + k * (rho[j] - rho0) / rho[j]**2) * W_grad
                f_visc += mu * mass[j] * (vel[j] - vel[i]) / rho[j] * torch.exp(-dist**2 / (h**2))
        forces[i] = f_pressure + f_visc
    return forces
