# PyVerse Project Plan

## **Module Descriptions**

### `main.py`

- Entry point.
- Loads menu/lobby screen via `pygame_ui.py`.
- Passes selected configuration to `simulation_loop.py`.

---

### `config.py`

- Stores global constants (FPS, resolution, colors)
- User toggles (physics options, interaction model)
- Particle count, timestep, integration method
- Easy to configure from the GUI or CLI.

---

### `core/simulation_loop.py`

- Core of the simulator.
- Manages:
  - Particle state updates
  - Time-stepping
  - Physics model coordination
  - GPU/CPU mode switching
  - Interactive settings and preset management

---

### `core/interaction_model.py`

- Provides `select_model()` to choose:
  - Direct (brute force)
  - Barnes-Hut (tree-based)

---

### `core/physics_engine/`

- Modularized physics logic:
  - Each file implements a single force model or algorithm.
  - Uses **PyTorch tensors** for CUDA compatibility.
  - Some fallback support for NumPy with `@jit` from Numba.
  - Includes gravity, electromagnetism, dark matter, SPH fluid, and GR corrections.

---

### `core/time_stepper.py`

- Contains multiple integrators:
  - **Euler**
  - **Verlet**
  - **RK4**
- Selectable via config or UI

---


### `graphics/vispy_renderer.py`

- Manages 3D scene and real-time rendering of particle systems.
- Applies shaders for glow, blur, etc.

---

### `graphics/hud_overlay.py`

- Uses VisPy text rendering or overlays for:

  - Particle count
  - Simulation speed
  - CPU/GPU/RAM usage
  - Current mode/algorithm

---

### `graphics/pygame_ui.py`

- Launch screen:

  - Start simulation
  - Change configuration
  - View benchmarks
  - Exit

- Toggle:

  - Particle count
  - Gravity/electromagnetic/dark matter/GR
  - Benchmark or stress test mode

---

### `utils/logger.py`

- Writes detailed logs:

  - Frame rate, RAM, GPU usage
  - Particle counts, timestep stats
  - Errors and performance spikes

---

### `utils/system_monitor.py`

- Uses `psutil` + `GPUtil`
- Logs:

  - CPU %
  - RAM used/available
  - GPU temperature, memory, usage

---

### `utils/benchmark.py`

- Runs predefined simulation presets
- Measures:

  - FPS
  - Time per step
  - Peak memory usage
  - GPU throughput

---

### `utils/stress_tester.py`

- Controlled stress loop
- Verifies system specs first
- Prompts user for confirmation
- Gradually increases:

  - Particle count
  - Physics complexity

---

## **Technologies**

| Purpose          | Tech Stack                             |
| ---------------- | -------------------------------------- |
| Numerical Engine | PyTorch (GPU), NumPy + Numba (CPU)     |
| Visualization    | VisPy (OpenGL), Pygame (UI)            |
| Performance      | psutil, GPUtil, logging, time          |
| Profiling        | line_profiler, Py-Spy                  |
| Optional         | PyQt (if GUI is preferred over Pygame) |

---

## Roadmap With Milestones

| Phase       | Milestone                | Description                                                       |
| ----------- | ------------------------ | ------------------------------------------------------------------|
| Phase 1  | Project Setup            | Scaffold project structure, set up `main.py`, basic Pygame UI        |
| Phase 2  | Core Physics Engine      | Build gravity, EM, SPH, GR approximation modules (CPU + GPU support) |
| Phase 3   | Simulation Loop & Models | Implement timestep, Barnes-Hut, direct model switching              |
| Phase 4  | GPU Integration          | Port major computations to PyTorch or Numba/CUDA                     |
| Phase 5 | Visualization            | Setup 3D rendering using VisPy + overlays                             |
| Phase 6  | Monitoring & Logging     | Track performance metrics and log them                               |
| Phase 7  | Stress Testing           | Add safeguards, looping stress tester                                |
| Phase 8  | Benchmarking Tools       | GUI-based and CLI benchmarking modes                                 |
| Phase 9  | QA & Tuning              | Tweak parameters, handle edge cases, config presets                  |
| Final    | Packaging & Demos        | Bundle `.zip`/`.exe`, record demos, document features                |

---
