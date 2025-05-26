# Manages time stepping, updates, calls physics modules

def run_simulation(config):
    from initializer import init_particles
    from interaction_model import get_forces
    from time_stepper import update_positions

    particles = init_particles(config["particle_count"])
    
    while True:
        forces = get_forces(particles, config)
        update_positions(particles, forces, config)
        yield particles
