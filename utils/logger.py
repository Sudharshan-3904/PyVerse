from loguru import logger
import logging

def setup_logger():
    logger.add("logs/performance_{time}.log", rotation="10 MB")
    logging.basicConfig(filename='simulation.log', level=logging.INFO)
    return logger

def log_simulation_step(step, particles, stats):
    msg = f"Step {step}: Particles={particles['pos'].shape[0]}, CPU={stats.get('cpu', 0):.1f}%, RAM={stats.get('ram', 0):.1f}%, GPU={stats.get('gpu', 0):.1f}%"
    logging.info(msg)