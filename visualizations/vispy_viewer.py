from vispy import scene, app
import numpy as np

class ParticleViewer(app.Canvas):
    def __init__(self, positions, sizes, colors, trails=None):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))
        self.unfreeze()
        self.view = scene.SceneCanvas(keys='interactive', show=True)
        self.scatter = scene.visuals.Markers(parent=self.view.scene)
        self.scatter.set_data(positions, face_color=colors, size=sizes)
        self.camera = scene.cameras.TurntableCamera(fov=45, azimuth=30, elevation=30, parent=self.view.scene)
        self.view.camera = self.camera
        self.hud = scene.visuals.Text('', color='white', font_size=16, pos=(10, 10), parent=self.view.scene)
        self.trails = []
        if trails is not None:
            for trail in trails:
                line = scene.visuals.Line(pos=trail, color='white', width=1, parent=self.view.scene)
                self.trails.append(line)
        self.frame_count = 0
        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.show()

    def update_particles(self, positions, sizes, colors):
        self.scatter.set_data(positions, face_color=colors, size=sizes)

    def update_trails(self, trails):
        for line, trail in zip(self.trails, trails):
            line.set_data(pos=trail)

    def on_timer(self, event):
        self.frame_count += 1
        self.hud.text = f'Particles: {len(self.scatter._data)} | Frame: {self.frame_count}'
        self.update()

# OpenGL Shader for Glow Effect
from vispy.visuals.shaders import Function

def add_glow_shader(markers_visual):
    glow_code = """
    void main() {
        float dist = length(gl_PointCoord - vec2(0.5, 0.5));
        float alpha = exp(-10.0 * dist * dist);
        gl_FragColor = vec4($color.rgb, $color.a * alpha);
    }
    """
    markers_visual._program.frag['glow'] = Function(glow_code)

# Color/Size Coding for Particle Types
def get_particle_colors_types(types):
    color_map = {
        0: [1, 1, 0, 1],    # yellow (star)
        1: [0, 0, 1, 1],    # blue (planet)
        2: [0.5, 0, 0.5, 1] # purple (dark matter)
    }
    return np.array([color_map.get(t, [1, 1, 1, 1]) for t in types])

def get_particle_sizes_types(types):
    size_map = {
        0: 10,  # star
        1: 5,   # planet
        2: 3    # dark matter
    }
    return np.array([size_map.get(t, 5) for t in types])

# Example usage (to be integrated with simulation loop):
# positions = np.random.normal(size=(100, 3))
# types = np.random.randint(0, 3, size=100)
# sizes = get_particle_sizes_types(types)
# colors = get_particle_colors_types(types)
# trails = [np.cumsum(np.random.randn(100, 3), axis=0) for _ in range(10)]
# viewer = ParticleViewer(positions, sizes, colors, trails=trails)
# add_glow_shader(viewer.scatter)
# app.run()
