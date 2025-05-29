import torch

def compute_barnes_hut(particles):
    """
    Placeholder: A real implementation would build an Octree for fast N log N gravity approximation.
    """
    # For now, simulate zero force for simplicity
    forces = torch.zeros_like(particles["pos"])
    return forces

def compute_barnes_hut_forces(particles):
    # Placeholder: returns zero force (replace with octree logic for real use)
    return torch.zeros_like(particles["pos"])
