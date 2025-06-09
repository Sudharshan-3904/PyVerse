# PyVerse To-Do List

> ---

1. **Physics Engine Improvements**

   | S.No | Task                   | Description                                                               | Done |
   | ---- | ---------------------- | ------------------------------------------------------------------------- | :--: |
   | 1.1  | Barnes-Hut Octree      | Implement full Barnes-Hut octree algorithm for N log N gravity            | ✅  |
   | 1.2  | Direct Gravity (Numba) | Implement direct gravity with Numba for CPU parallelism                   | ✅  |
   | 1.3  | Electromagnetic Force  | Implement electromagnetic force calculation (support for particle charge) | ✅  |
   | 1.4  | Dark Matter Model      | Implement dark matter force model (heuristic or parametric)               | ✅  |
   | 1.5  | SPH Fluid Dynamics     | Implement SPH (Smoothed Particle Hydrodynamics) for fluid dynamics        | ✅  |
   | 1.6  | General Relativity     | Implement general relativity corrections (post-Newtonian or other)        | ✅  |

2. **Simulation Loop & Models**

   | S.No | Task              | Description                                                                 | Done |
   | ---- | ----------------- | --------------------------------------------------------------------------- | :--: |
   | 2.1  | Generator Loop    | Refactor simulation loop to support generator/yield for stepwise simulation | ✅  |
   | 2.2  | Pause/Resume/Step | Add support for pausing, resuming, and stepping simulation from UI          | ✅  |
   | 2.3  | Dynamic Particles | Add support for dynamic addition/removal of particles during simulation     | ✅  |

3. **Visualization**

   | S.No | Task               | Description                                                            | Done |
   | ---- | ------------------ | ---------------------------------------------------------------------- | :--: |
   | 3.1  | VisPy 3D Rendering | Implement 3D rendering of particles using VisPy (with camera controls) | ✅  |
   | 3.2  | OpenGL Shaders     | Add support for OpenGL shaders (glow, blur, etc.) in VisPy             | ✅  |
   | 3.3  | VisPy HUD Overlay  | Implement HUD overlay in VisPy for real-time stats                     | ✅  |
   | 3.4  | Color/Size Coding  | Add color/size coding for different particle types                     | ✅  |
   | 3.5  | Orbit Trails       | Add orbit trails and path visualization                                | ✅  |

4. **User Interface (UI)**

   | S.No | Task                 | Description                                                                 | Done |
   | ---- | -------------------- | --------------------------------------------------------------------------- | :--: |
   | 4.1  | Settings Menu        | Integrate settings menu into simulation (expand for more options)           | ✅  |
   | 4.2  | Preset Management    | Add support for creating, editing, and deleting user presets from the UI    | ✅  |
   | 4.3  | Preset Loading       | Add support for loading any preset (solar system, user, random) from the UI | ✅  |
   | 4.4  | Help Screen          | Add in-simulation help screen (key bindings, controls)                      | ✅  |
   | 4.5  | Confirmation Dialogs | Add confirmation dialogs for destructive actions                            | ✅  |

5. **Presets & Initialization**

   | S.No | Task              | Description                                                                          | Done |
   | ---- | ----------------- | ------------------------------------------------------------------------------------ | :--: |
   | 5.1  | More Presets      | Add more realistic galaxy/cluster presets                                            | ✅  |
   | 5.1.1  | New Preset      | Add a three-body problem simulation                                                  | ✅  |
   | 5.1.2  | New Preset      | Add a binary star system simulation                                                  | ✅  |
   | 5.1.3  | New Preset      | Add a blackhole binary system simulation                                             | ✅  |
   | 5.1.4  | New Preset      | Simulation of planet formulation (if possible with current level of system)          | ✅  |
   | 5.2  | Preset Editor     | Add UI for user to create and save custom presets                                    | ✅  |
   | 5.3  | Preset Validation | Add validation for preset files (check for required fields, handle errors)           | ✅  |

6. **Performance & Monitoring**

   | S.No | Task                 | Description                                                                   | Done |
   | ---- | -------------------- | ----------------------------------------------------------------------------- | :--: |
   | 6.1  | Temp Monitoring      | Add GPU/CPU temperature monitoring (currently only usage is shown)            | ❎  |
   | 6.2  | Memory Monitoring    | Add memory usage monitoring (RAM, VRAM)                                       | ❎  |
   | 6.3  | Logging Improvements | Improve logging: add error logging, performance spikes, and simulation events | ❎  |
   | 6.4  | Real-Time Graphs     | Add real-time performance graphs (FPS, CPU, GPU, RAM) in overlay              | ❎  |

7. **Benchmarking & Stress Testing**

   | S.No | Task                     | Description                                                                                         | Done |
   | ---- | ------------------------ | --------------------------------------------------------------------------------------------------- | :--: |
   | 7.1  | Benchmarking Mode        | Implement full benchmarking mode (run multiple presets, log results, generate reports)              | ❎  |
   | 7.2  | Interactive Stress Test  | Implement interactive stress testing (gradually increase load, show system health, abort if unsafe) | ❎  |
   | 7.3  | GUI/CLI Benchmark/Stress | Add GUI/CLI options to run benchmarks and stress tests                                              | ❎  |

8. **Profiling & Optimization**

   | S.No | Task                        | Description                                            | Done |
   | ---- | --------------------------- | ------------------------------------------------------ | :--: |
   | 8.1  | Profiler Integration        | Integrate cProfile/py-spy for profiling from the UI    | ❎  |
   | 8.2  | Performance Summary         | Add performance summary after simulation/benchmark run | ❎  |
   | 8.3  | Physics/Render Optimization | Optimize bottlenecks in physics and rendering          | ❎  |

> ---
