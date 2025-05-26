DEFAULT_SETTINGS = {
    "fps": 60,
    "resolution": (1920, 1080),
    "fullscreen": False,
    "particle_count": 1000,
    "timestep": 1,
    "gravity": 9.81,
    "physics_options": {
        "enable_collisions": True,
        "enable_gravity": True,
    },
    "interaction_model": "default"
}

POSSIBLE_SETTINGS = {
    "fps": [30, 60, 120],
    "resolution": [(1920, 1080), (1280, 720), (800, 600)],
    "fullscreen": [True, False],
    "particle_count": [100, 500, 1000, 5000],
    "timestep": [1, 2, 5],
    "gravity": 9.81,
    "physics_options": {
        "enable_collisions": [True, False],
        "enable_gravity": [True, False],
    },
    "interaction_model": ["default", "advanced"]
}

CONFIG = {
    "interaction_model": "barnes_hut",  # or 'direct'
    "physics": {
        "gravity": True,
        "electromagnetism": False,
        "dark_matter": True,
        "fluid_dynamics": True,
        "relativity": False
    },
    "gpu_mode": True,
    "particle_count": 100_000,
    "benchmark_mode": False,
    "stress_test": False,
    "integration_method": "verlet",
    "timestep": 0.01
}
