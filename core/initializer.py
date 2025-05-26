# Initializes particles in a disk, cluster, or user-defined preset

def init_particles(n):
    import torch
    positions = torch.randn((n, 3))
    velocities = torch.zeros((n, 3))
    masses = torch.ones(n)
    return {"pos": positions, "vel": velocities, "mass": masses}
