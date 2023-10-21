import numpy as np

class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def update_render(self):
        self.scene.update()
        self.render_shadow()
        
    def main_render(self):
        for obj in self.scene.objects:
            obj.render()

    def render(self):
        # clear framebuffer
        self.app.ctx.clear(color=self.app.backgroundColor)
        # pass 1
        self.update_render()
        # pass 2
        self.app.ctx.screen.use()
        self.main_render()

        
    def get_render(self):
        # pass 1
        self.update_render()
        # pass 2
        fbo = self.app.ctx.simple_framebuffer(self.app.WIN_SIZE)
        fbo.use()
        fbo.clear(color=self.app.backgroundColor)
        self.main_render()
        
        # Lire les données de l'image depuis le framebuffer
        image_data = fbo.read(components=3)  # Les composants sont RGB
        
        # Créer un tableau NumPy à partir des données de l'image
        image = np.frombuffer(image_data, dtype=np.uint8)
        image = image.reshape((self.app.WIN_SIZE[1], self.app.WIN_SIZE[0], 3))
        
        # Inverser l'ordre des lignes pour corriger l'orientation
        image = image[::-1, :, :]
        
        return image

    def destroy(self):
        self.depth_fbo.release()