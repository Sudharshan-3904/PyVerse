# PyVerse Project Plan

## 🗂️ **Directory Structure**

```
galaxy_simulator/
│
├── main.py                         # Entry point
├── config.py                       # Global configuration and toggles
├── requirements.txt                # Dependencies
│
├── core/
│   ├── simulation_loop.py         # Main simulation execution logic
│   ├── initializer.py             # Galaxy/system setup, random or structured
│   ├── interaction_model.py       # Switch logic between direct and Barnes-Hut
│   ├── physics_engine/
│   │   ├── gravity.py             # Gravity (Newtonian, GR approximation)
│   │   ├── electromagnetism.py    # Electromagnetic forces
│   │   ├── dark_matter.py         # Dark matter physics (heuristic or parametric)
│   │   ├── fluid_dynamics.py      # SPH implementation
│   │   ├── barnes_hut.py          # Barnes-Hut octree implementation
│   │   └── general_relativity.py  # GR correction approximations
│   └── time_stepper.py            # Euler / Verlet / Runge-Kutta integrator
│
├── graphics/
│   ├── vispy_renderer.py          # Handles 3D rendering using VisPy
│   ├── hud_overlay.py             # Displays metrics: FPS, load, particle count
│   └── pygame_ui.py               # Menu/lobby screen and interaction with Pygame
│
├── utils/
│   ├── logger.py                  # Custom logging (RAM, GPU, CPU, simulation data)
│   ├── system_monitor.py          # Performance monitoring using psutil and GPUtil
│   ├── benchmark.py               # Benchmark testing and result logging
│   ├── profiler.py                # Optional performance profiling (cProfile, py-spy)
│   └── stress_tester.py           # Safely run load tests with user confirmation
│
└── assets/
    ├── shaders/                   # Custom OpenGL shaders for VisPy rendering
    ├── fonts/                     # Fonts for UI
    └── presets/                   # Galaxy/system configuration presets
```

---

## 📄 **Module Descriptions**

### `main.py`

- Entry point.
- Loads menu/lobby screen via `pygame_ui.py`.
- Passes selected configuration to `simulation_loop.py`.

---

### `config.py`

Stores:

- Global constants (FPS, resolution, colors)
- User toggles (physics options, interaction model)
- Particle count, timestep, integration method

✅ Makes it easy to configure from the GUI or CLI.

---

### `core/simulation_loop.py`

- Core of the simulator.
- Manages:

  - Particle state updates
  - Time-stepping
  - Physics model coordination
  - GPU/CPU mode switching

---

### `core/interaction_model.py`

- Provides `select_model()` to choose:

  - Direct (brute force)
  - Barnes-Hut (tree-based)

---

### `core/physics_engine/`

Modularized physics logic:

- Each file implements a single force model or algorithm.
- Uses **PyTorch tensors** for CUDA compatibility.
- Some fallback support for NumPy with `@jit` from Numba.

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

## 🛠️ **Technologies**

| Purpose          | Tech Stack                             |
| ---------------- | -------------------------------------- |
| Numerical Engine | PyTorch (GPU), NumPy + Numba (CPU)     |
| Visualization    | VisPy (OpenGL), Pygame (UI)            |
| Performance      | psutil, GPUtil, logging, time          |
| Profiling        | line_profiler, Py-Spy                  |
| Optional         | PyQt (if GUI is preferred over Pygame) |

---
