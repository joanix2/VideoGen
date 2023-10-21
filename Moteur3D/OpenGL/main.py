import moderngl as mgl
import numpy as np
import imageio
#from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer

import pygame as pg
import sys
from tqdm import tqdm

class BaseGraphics:
    def __init__(self, width:int, height:int, hidden:bool=True, backgroundColor = (0.08, 0.16, 0.18)):
        self.WIN_SIZE = (width, height)
        self.hidden = hidden
        self.backgroundColor = backgroundColor
        
        # mouse settings
        # pg.event.set_grab(True)
        # pg.mouse.set_visible(False)
        
        if self.hidden:
            self.ctx = mgl.create_standalone_context()
        else:
            #init pygame modules
            pg.init()
            # set opengl attr
            pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
            pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
            pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
            pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
            
            # detect and use existing opengl context
            self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw' # affichage des triangles dans le sens des aiguilles d'une montre
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        
        self.time = 0
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self, position=(0, 5, 30))
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)
        # renderer
        self.scene_renderer = SceneRenderer(self)

class VideoRenderer(BaseGraphics):
    def __init__(self, width:int=1280, height:int=720, fps:int = 30, backgroundColor = (0.08, 0.16, 0.18)):
        super().__init__(width, height, backgroundColor=backgroundColor)
        self.fps = fps
        
        self.image_list = []
        
    def render_to_framebuffer(self):
        return self.scene_renderer.get_render()
    
    def get_time(self, frame_index):
        self.time = frame_index/self.fps

    def render_frames(self, num_frames):
            for f in tqdm(range(num_frames), desc="Rendering Frames", unit="frame"):
                self.get_time(f)
                self.image_list.append(self.render_to_framebuffer())

    def generate_video(self, output_path):
        imageio.mimsave(output_path, self.image_list, fps= self.fps)
        print("Vidéo générée avec succès:", output_path)
        
    
class GraphicsEngine(BaseGraphics):
    def __init__(self, width:int=1280, height:int=720, backgroundColor = (0.08, 0.16, 0.18)):
        super().__init__(width, height, hidden=False, backgroundColor = backgroundColor)

        # create an object to help track time
        self.clock = pg.time.Clock()
        self.delta_time = 0
        
        self.mouse_left_click = False
        self.mouse_center_click = False
        
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()
    
            if event.type == pg.MOUSEBUTTONDOWN:
                pg.mouse.get_rel()
                if event.button == 1:  # Clic gauche de la souris
                    self.mouse_left_click = True
                elif event.button == 2:  # Clic molette de la souris
                    self.mouse_center_click = True
                elif event.button == 4:  # Molette vers le haut
                    self.camera.move('forward', 50)
                elif event.button == 5:  # Molette vers le bas
                    self.camera.move('forward', -50)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Relâcher le clic gauche de la souris
                    self.mouse_left_click = False
                if event.button == 2:  # Clic molette de la souris
                    self.mouse_center_click = False
    
        # rotation avec le clic gauche
        if self.mouse_left_click:
            rel_x, rel_y = pg.mouse.get_rel()
            self.camera.rotate(-rel_x, -rel_y)
            
        # déplacement avec le clic molette
        if self.mouse_center_click:
            rel_x, rel_y = pg.mouse.get_rel()
            self.camera.move('right', -rel_x)
            self.camera.move('up', rel_y)

    
    def render(self):
        # render scene
        self.scene_renderer.render()
        # swap buffers
        pg.display.flip()
        
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    
    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

def runRendering(num_frames, width=1280, height=720, output_path='render.mp4', fps=30):
    renderer = VideoRenderer(width = width, height = height)
    renderer.render_frames(num_frames = num_frames)
    renderer.generate_video(output_path = output_path)
    
def runEngine():
    app = GraphicsEngine()
    app.run()

if __name__ == "__main__":
    runEngine()
    runRendering(1000)