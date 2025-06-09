from vispy import scene, app
import numpy as np

class ParticleViewer(app.Canvas):
    def __init__(self, positions, sizes, colors):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))
        self.unfreeze()
        self.view = scene.SceneCanvas(keys='interactive', show=True)
        self.scatter = scene.visuals.Markers()
        self.view.central_widget.add_widget(self.scatter)
        self.scatter.set_data(positions, face_color=colors, size=sizes)
        self.camera = scene.cameras.TurntableCamera(fov=45, azimuth=30, elevation=30)
        self.view.central_widget.add_widget(self.scatter)
        self.view.camera = self.camera
        self.show()

    def update_particles(self, positions, sizes, colors):
        self.scatter.set_data(positions, face_color=colors, size=sizes)

# Example usage:
# positions = np.random.normal(size=(100, 3))
# sizes = np.full(100, 5)
# colors = np.ones((100, 4))
# viewer = ParticleViewer(positions, sizes, colors)
# app.run()