def run_benchmark():
    import time
    from config import CONFIG
    from core.simulation_loop import SimulationSystem
    from utils.logger import setup_logger

    logger = setup_logger()
    config = CONFIG.copy()
    logger.info("Starting benchmark...")

    start_time = time.time()
    sim = SimulationSystem(config)

    for frame in range(100):
        sim.update()

    end_time = time.time()
    fps = 100 / (end_time - start_time)
    logger.info(f"Average FPS over 100 frames: {fps:.2f}")

def run_benchmarks(simulation_class, presets):
    import time
    from config import CONFIG
    import sys
    
    print("\n" + "="*40)
    print("Starting Comprehensive Benchmarks")
    print("="*40)
    
    test_presets = ["solar_system", "binary_star", "three_body"]
    
    for preset in test_presets:
        if preset not in presets:
            continue
            
        print(f"\nEvaluating Preset: {preset.upper()}")
        print("-" * 30)
        
        cfg = CONFIG.copy()
        cfg["preset"] = preset
        cfg["benchmark_mode"] = True
        
        sim = simulation_class(cfg)
        
        start = time.time()
        frames_run = 0
        target_frames = 100
        
        for i in range(target_frames):
            try:
                sim.update()
                frames_run += 1
            except Exception as e:
                print(f"Error during benchmark: {e}")
                break
                
        end = time.time()
        elapsed = end - start
        fps = frames_run / max(elapsed, 0.001)
        
        print(f"Frames Completed: {frames_run}")
        print(f"Elapsed Time    : {elapsed:.3f}s")
        print(f"Average FPS     : {fps:.2f}\n")
        
    print("="*40)
    print("Benchmarks Completed Successfully.")
    print("="*40)
    sys.exit(0)
