def run_stress_test(simulation_class, base_config):
    import time
    import sys
    import copy
    
    print("\n" + "="*40)
    print("Starting Interactive Stress Test")
    print("="*40)
    
    particle_counts = [500, 1000, 2500, 5000, 10000]
    
    for count in particle_counts:
        print(f"\n--- Testing with {count} particles ---")
        cfg = copy.deepcopy(base_config)
        cfg["particle_count"] = count
        cfg["stress_test"] = True
        
        sim = simulation_class(cfg)
        start = time.time()
        
        frames_run = 0
        target_frames = 50
        
        for i in range(target_frames):
            try:
                sim.update()
                frames_run += 1
            except Exception as e:
                print(f"Error during stress test: {e}")
                break
                
        end = time.time()
        elapsed = end - start
        fps = frames_run / max(elapsed, 0.001)
        
        stats = getattr(sim, "stats", {})
        print(f"System Load -> CPU: {stats.get('cpu',0):.1f}% | RAM: {stats.get('ram',0):.1f}%")
        
        print(f"Result           : {fps:.2f} FPS")
        
        if fps < 10.0:
            print("\nWARNING: System is struggling. Frame rate dropped below 10 FPS.")
            print("Aborting further stress testing to prevent unresponsiveness.")
            break
            
    print("\n" + "="*40)
    print("Stress Testing Concluded.")
    print("="*40)
    sys.exit(0)