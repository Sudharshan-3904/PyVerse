import os
import json
from loguru import logger
import logging
from logging.handlers import RotatingFileHandler

os.makedirs('logs', exist_ok=True)

# Performance & generic sim logger
def setup_logger():
    logger.add("logs/performance_{time}.log", rotation="10 MB")
    logging.basicConfig(filename='logs/simulation.log', level=logging.INFO)
    return logger

def log_simulation_step(step, particles, stats):
    msg = f"Step {step}: Particles={particles['pos'].shape[0]}, CPU={stats.get('cpu', 0):.1f}%, RAM={stats.get('ram', 0):.1f}%, GPU={stats.get('gpu', 0):.1f}%"
    logging.getLogger().info(msg)

# Specialized Object Tracker logger
obj_logger = logging.getLogger("object_tracker")
obj_logger.setLevel(logging.INFO)
obj_handler = RotatingFileHandler("logs/object_changes.log", maxBytes=10*1024*1024, backupCount=5)
obj_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
if not obj_logger.handlers:
    obj_logger.addHandler(obj_handler)

def log_object_event(action, object_name, details):
    """Log an explicit event for an object's property change or lifecycle."""
    msg = json.dumps({"action": action, "object": object_name, "details": details})
    obj_logger.info(msg)

def log_all_particles_state(step, particles):
    """Log properties (like position) for all objects at a specific step."""
    pos = particles["pos"].cpu().tolist()
    names = particles.get("names")
    if not names:
        names = [f"Particle_{i}" for i in range(len(pos))]
        
    for i in range(len(pos)):
        try:
            mass_val = float(particles["mass"][i][0])
        except Exception:
            try:
                mass_val = float(particles["mass"][i])
            except Exception:
                mass_val = 1.0
                
        details = {
            "step": step,
            "position": [round(p, 4) for p in pos[i]],
            "mass": mass_val
        }
        log_object_event("STATE_UPDATE", names[i], details)
