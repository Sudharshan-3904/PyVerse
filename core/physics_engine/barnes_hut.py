import torch

class OctreeNode:
    def __init__(self, center, half_size, indices):
        self.center = center
        self.half_size = half_size
        self.indices = indices
        self.children = []
        self.mass = 0.0
        self.mass_center = torch.zeros(3)

    def is_leaf(self):
        return len(self.children) == 0

def build_octree(pos, indices, center, half_size, max_particles=1):
    if len(indices) <= max_particles:
        return OctreeNode(center, half_size, indices)
    node = OctreeNode(center, half_size, indices)
    offsets = torch.tensor([[dx, dy, dz] for dx in [-0.5, 0.5] for dy in [-0.5, 0.5] for dz in [-0.5, 0.5]])
    for offset in offsets:
        child_center = center + offset * half_size
        mask = ((pos[indices] >= (child_center - half_size/2)) & (pos[indices] < (child_center + half_size/2))).all(dim=1)
        child_indices = [indices[i] for i, m in enumerate(mask) if m]
        if child_indices:
            child = build_octree(pos, child_indices, child_center, half_size/2, max_particles)
            node.children.append(child)
    return node

def compute_mass(node, pos, mass):
    if node.is_leaf():
        node.mass = mass[node.indices].sum()
        if node.mass > 0:
            node.mass_center = (pos[node.indices] * mass[node.indices]).sum(dim=0) / node.mass
        else:
            node.mass_center = torch.zeros(3)
    else:
        node.mass = 0.0
        node.mass_center = torch.zeros(3)
        for child in node.children:
            compute_mass(child, pos, mass)
            node.mass += child.mass
            node.mass_center += child.mass * child.mass_center
        if node.mass > 0:
            node.mass_center /= node.mass

def barnes_hut_force(node, pos, mass, i, theta=0.5, G=6.67430e-11):
    if node.is_leaf():
        f = torch.zeros(3)
        for j in node.indices:
            if i != j:
                diff = pos[j] - pos[i]
                dist = torch.norm(diff) + 1e-5
                f += G * mass[i] * mass[j] * diff / (dist ** 3)
        return f
    else:
        d = torch.norm(node.mass_center - pos[i])
        s = node.half_size * 2
        if s / d < theta:
            diff = node.mass_center - pos[i]
            dist = torch.norm(diff) + 1e-5
            return G * mass[i] * node.mass * diff / (dist ** 3)
        else:
            f = torch.zeros(3)
            for child in node.children:
                f += barnes_hut_force(child, pos, mass, i, theta, G)
            return f

def compute_barnes_hut_forces(particles, theta=0.5, G=6.67430e-11):
    pos = particles["pos"]
    mass = particles["mass"].flatten()
    n = pos.shape[0]
    min_pos = pos.min(dim=0).values
    max_pos = pos.max(dim=0).values
    center = (min_pos + max_pos) / 2
    half_size = (max_pos - min_pos).max() / 2 + 1e-5
    indices = list(range(n))
    root = build_octree(pos, indices, center, half_size)
    compute_mass(root, pos, mass)
    forces = torch.zeros_like(pos)
    for i in range(n):
        forces[i] = barnes_hut_force(root, pos, mass, i, theta, G)
    return forces
