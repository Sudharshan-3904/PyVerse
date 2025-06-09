# PyVerse: Galaxy-Scale Physics Simulator

PyVerse is a Python-based, interactive, and extensible galaxy-scale simulation platform. It supports real-time visualization, advanced physics models, and performance monitoring, making it ideal for both scientific exploration and educational demos.

## Features

- **Physics Models:** Gravity (Newtonian & Barnes-Hut), Electromagnetism, Dark Matter, SPH Fluid Dynamics, General Relativity (planned)
- **Presets:** Realistic solar system, random galaxies, and user-defined systems
- **Visualization:** Real-time rendering with VisPy (OpenGL) and Pygame UI
- **Performance Monitoring:** CPU, RAM, GPU usage (with optional temperature monitoring)
- **Benchmarking & Stress Testing:** Built-in tools for system evaluation
- **Interactive UI:** Fullscreen menu, real-time settings, and preset management
- **Extensible:** Modular codebase for easy addition of new physics or visualization modules

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

## Usage

- **Start the application:**

  ```sh
  python main.py
  ```

- **Menu Options:**
  - Start Simulation
  - Run Benchmark
  - Run Stress Test
  - Exit

- **In-Simulation Controls:**
  - `F1`: Toggle settings sidebar (change presets, physics, etc.)
  - `ESC`: Quit simulation
  - `S`: Save current config as a user preset (in settings menu)

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
├── utils/
│   ├── logger.py
│   ├── system_monitor.py
│   ├── benchmark.py
│   ├── profiler.py
│   └── stress_tester.py
└── assets/
    ├── shaders/
    ├── fonts/
    └── presets/
        ├── solar_system/
        └── user/
```

## Presets

- **Solar System:** Provided as a realistic preset in `assets/presets/solar_system/solar_system.json`.
- **User Presets:** Save your own configurations from the UI. Presets are stored in `assets/presets/user/`.

## Roadmap

See [ProjectPlan.md](ProjectPlan.md) and [ToDo.md](ToDo.md) for milestones and detailed tasks.

## Contributing

- Fork the repository and submit pull requests.
- Please add docstrings and comments to new modules.
- Open issues for bugs, feature requests, or questions.

## License

MIT License

---

*PyVerse is a work in progress. Contributions and feedback are welcome!*
