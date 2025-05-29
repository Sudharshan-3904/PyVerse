from core.physics_engine import gravity, barnes_hut


def select_model(model_name):
    if model_name == "barnes_hut":
        return barnes_hut.compute_barnes_hut_forces
    else:
        return gravity.compute_gravity_forces


def get_forces(particles, config):
    if config["interaction_model"] == "direct":
        from core.physics_engine.gravity import compute_direct_gravity

        return compute_direct_gravity(particles)
    else:
        from core.physics_engine.barnes_hut import compute_barnes_hut

        return compute_barnes_hut(particles)