from pyray import *
import assets.lib.rayhelper as rh

from assets.scripts.player import Player
from assets.scripts.particles import Particles
from assets.scripts.monsters import Monsters, Ghost

class Game:
    def __init__(self):
        # Constants
        self.SCREEN_WIDTH = 320
        self.SCREEN_HEIGHT = 180
        self.RATIO = 4
        self.WINDOW_WIDTH = self.SCREEN_WIDTH * self.RATIO
        self.WINDOW_HEIGHT = self.SCREEN_HEIGHT * self.RATIO

        self.SCREEN_SOURCE_REC = Rectangle(0.0, 0.0, self.SCREEN_WIDTH, -self.SCREEN_HEIGHT)
        self.SCREEN_DEST_REC = Rectangle(0.0, 0.0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.FPS = 60

        # Initializations
        init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 'Game')
        set_target_fps(self.FPS)

        self.screen_camera = Camera2D()
        self.screen_camera.zoom = 1.0

        # self.window_camera = Camera2D()
        # self.window_camera.zoom = 1.0

        self.screen = load_render_texture(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.darkness = load_shader(0, 'assets/scripts/shaders/darkness.glsl')

        self.lpos_loc = get_shader_location(self.darkness, 'lpos')
        

        self.mouse = Vector2(0, 0)

        self.player = Player(self)
        self.particles = Particles()
        self.monsters = Monsters(self)

        self.shadows = []


    
    def get_mouse(self):
        # Translates the mouse to its real in-world position
        self.mouse = get_mouse_position()
        self.mouse = rh.vec2(self.mouse.x, self.mouse.y)
        self.mouse /= self.RATIO
        self.mouse.x += self.screen_camera.target.x
        self.mouse.y += self.screen_camera.target.y

        

    def run(self):
        while not window_should_close():
            self.get_mouse()
            self.shadows = []

            self.player.run()
            self.monsters.run()

            set_shader_value(self.darkness, self.lpos_loc, self.player.weapon.pos.toray(), ShaderAttributeDataType.SHADER_ATTRIB_VEC2)

            
            begin_texture_mode(self.screen)
            

            clear_background(Color(130, 100, 100, 255))
            
            begin_mode_2d(self.screen_camera)

            if is_mouse_button_pressed(1):
                self.monsters.add(Ghost(rh.Rect(self.mouse.x, self.mouse.y, 9, 13)), 'ghost')
            
            for s in self.shadows:
                draw_rectangle_rec(s, Color(30, 30, 30, 60))

            
            self.monsters.draw()
            self.player.draw()
            self.particles.run()

            

            end_mode_2d()

            begin_shader_mode(self.darkness)
            draw_rectangle(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, WHITE)
            end_shader_mode()

            end_texture_mode()

            self.draw_to_window()
            

        self.unload()
    
    def draw_to_window(self):
        begin_drawing()
        draw_texture_pro(self.screen.texture, self.SCREEN_SOURCE_REC, self.SCREEN_DEST_REC, Vector2(0, 0), 0.0, WHITE)
        end_drawing()
    
    def unload(self):
        self.player.unload()
        self.monsters.unload()

        unload_render_texture(self.screen)
        close_window()

if __name__ == '__main__':
    gm = Game()
    gm.run()