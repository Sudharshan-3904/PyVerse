# PyVerse: Galaxy-Scale Physics Simulator

PyVerse is a Python-based, interactive, and extensible galaxy-scale simulation platform. It supports real-time visualization, advanced physics models, and performance monitoring, making it ideal for both scientific exploration and educational demos.

---

## Features

- **Physics Models:** Gravity (Newtonian & Barnes-Hut), Electromagnetism, Dark Matter, SPH Fluid Dynamics, General Relativity (post-Newtonian correction)
- **Presets:** Realistic solar system, binary star, three-body, blackhole binary, planet formation, and user-defined systems
- **Visualization:** Real-time rendering with VisPy (OpenGL) and Pygame UI
- **Performance Monitoring:** CPU, RAM, GPU usage (with optional temperature monitoring)
- **Benchmarking & Stress Testing:** Built-in tools for system evaluation
- **Interactive UI:** Windowed borderless menu, real-time settings, and preset management
- **Dynamic Particles:** Add or remove particles during simulation
- **Extensible:** Modular codebase for easy addition of new physics or visualization modules

---

## Installation

1. **Clone the repository:**

   ```sh
   git clone "https://github.com/Sudharshan-3904/PyVerse.git"
   cd PyVerse
   ```

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

   - For GPU/temperature monitoring on Windows, install `wmi` and `pywin32`.
   - For best performance, use a Python environment with CUDA-enabled PyTorch if you have a compatible GPU.

---

## Usage

- **Start the application:**

  ```sh
  uv run main.py
  ```

- **Menu Options:**
  - Start Simulation
  - Run Benchmark
  - Run Stress Test
  - Preset Management
  - Help
  - Exit

- **In-Simulation Controls:**
  - `F1`: Toggle settings sidebar (change presets, physics, etc.)
  - `ESC`: Quit simulation
  - `S`: Save current config as a user preset (in settings menu)
  - `A`: Add particle at cursor
  - `D`: Delete particle at cursor
  - `SPACE`: Pause/Resume simulation
  - `RIGHT`: Step simulation (when paused)
  - `H`: Show/Hide help screen

---

## Project Structure

```text
PyVerse/
├── main.py
├── config.py
├── requirements.txt
├── core/
│   ├── simulation_loop.py
│   ├── initializer.py
│   ├── interaction_model.py
│   ├── time_stepper.py
│   └── physics_engine/
│       ├── gravity.py
│       ├── electromagnetism.py
│       ├── dark_matter.py
│       ├── fluid_dynamics.py
│       ├── barnes_hut.py
│       └── general_relativity.py
├── graphics/
│   ├── vispy_renderer.py
│   ├── hud_overlay.py
│   └── pygame_ui.py
│   └── visualizations/
│       └── vispy_viewer.py
├── utils/
│   ├── logger.py
│   ├── system_monitor.py
│   ├── benchmark.py
│   ├── profiler.py
│   └── stress_tester.py
└── assets/
    └── presets/
        ├── Default/
        │   ├── solar_system.json
        │   ├── binary_star.json
        │   ├── three_body.json
        │   ├── blackhole_binary.json
        │   └── planet_formation.json
        └── user/
```

---

## Presets

- **Default Presets:**
  - Solar System: `assets/presets/Default/solar_system.json`
  - Binary Star System: `assets/presets/Default/binary_star.json`
  - Three-Body Problem: `assets/presets/Default/three_body.json`
  - Blackhole Binary: `assets/presets/Default/blackhole_binary.json`
  - Planet Formation: `assets/presets/Default/planet_formation.json`
- **User Presets:**
  - Save your own configurations from the UI. Presets are stored in `assets/presets/user/`.

---

## Documents

- [Docs/ProjectPlan.md](Docs/ProjectPlan.md):
  - Containes the results of the starting research done for this project
- [Docs/ToDo.md](Docs/ToDo.md):
  - Contains categorized milestones to be achieved
  - Provides a task-wise list for implementation
- [Docs/Problems.md](Docs/Problems.md):
  - List of problems identified
  - Updated with status and current progress

---

## Contributing

- Fork the repository and submit pull requests.
- Please add docstrings and comments to new modules.
- Open issues for bugs, feature requests, or questions.

---

## License

MIT License

---

> *PyVerse is a work in progress. Contributions and feedback are welcome!*
