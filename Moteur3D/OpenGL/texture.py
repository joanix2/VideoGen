from PIL import Image
import numpy as np
import moderngl as mgl

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img.png')
        self.textures[1] = self.get_texture(path='textures/img_1.png')
        self.textures[2] = self.get_texture(path='textures/img_2.png')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        self.textures['depth_texture'] = self.get_depth_texture()
        
    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture(self, path):
        # Charger l'image avec Pillow (PIL)
        with Image.open(path) as img:
            # Convertir l'image en mode RGB si nécessaire
            img = img.convert("RGB")
            
            # Inverser l'image selon l'axe Y
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
    
            # Récupérer les dimensions de l'image
            width, height = img.size
    
            # Obtenir les données de l'image sous forme de bytes
            image_data = np.array(img)
            
            # Créer une texture avec les données de l'image
            texture = self.ctx.texture((width, height), 3, image_data.tobytes())
    
            # mipmaps
            texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
            texture.build_mipmaps()
            # AF
            texture.anisotropy = 32.0
            
            return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]