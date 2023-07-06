from pyray import *
import assets.lib.rayhelper as rh

from assets.scripts.tiles import Tiles


class ETiles(Tiles):
    def __init__(self, gm):
        super().__init__(gm)

        self.wrap_solids = [[]]
        self.wrap_airs = [[]]
    
    def blank_wrap(self, size):
        return [[0 for j in range(round(size[0] / 10))] for i in range(round(size[1] / 10))]
    
    def add_w(self, pos, solid=True, v=1):
        try:
            if solid:
                self.wrap_solids[pos[0]][pos[1]] = v
            else:
                
                self.wrap_airs[pos[0]][pos[1]] = v
        except IndexError:
            print(f'Tile at {pos} out of world range! Tile not placed.')
    
    def load(self, filename):
        level = super().load(filename)
        self.wrap_solids = self.blank_wrap(level['size'])
        for sk in level['solids']:
            for t in level['solids'][sk]:
                self.add_w([round(t[0] / 10), round(t[1] / 10)])
        
        self.wrap_airs = self.blank_wrap(level['size'])
        for ak in level['airs']:
            for t in level['airs'][ak]:
                self.add_w([round(t[0] / 10), round(t[1] / 10)])
        




class TileEditor:
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
        init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 'Tile Editor')
        set_target_fps(self.FPS)

        self.screen_camera = Camera2D()
        self.screen_camera.zoom = 1.0



        # self.window_camera = Camera2D()
        # self.window_camera.zoom = 1.0

        self.screen = load_render_texture(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        

        self.mouse = Vector2(0, 0)


        self.tiles = ETiles(self)
        self.tiles.load(0)



    def get_mouse(self):
        # Translates the mouse to its real in-world position
        self.mouse = get_mouse_position()
        self.mouse = rh.vec2(self.mouse.x, self.mouse.y)
        self.mouse /= self.RATIO
        self.mouse.x += self.screen_camera.target.x
        self.mouse.y += self.screen_camera.target.y

    def move_camera(self, speed=2):
        if is_key_down(KeyboardKey.KEY_D): self.screen_camera.target.x += speed 
        elif is_key_down(KeyboardKey.KEY_A): self.screen_camera.target.x -= speed 
        if is_key_down(KeyboardKey.KEY_S): self.screen_camera.target.y += speed 
        elif is_key_down(KeyboardKey.KEY_W): self.screen_camera.target.y -= speed 

        if is_key_down(KeyboardKey.KEY_E): self.screen_camera.zoom += .03
        elif is_key_down(KeyboardKey.KEY_Q): self.screen_camera.zoom -= .03
    


    def run(self):
        while not window_should_close():
            self.get_mouse()


            self.move_camera()


            begin_texture_mode(self.screen)
            

            clear_background(Color(179, 120, 93, 255))

            begin_mode_2d(self.screen_camera)
    

            self.tiles.draw()


            end_mode_2d()


            end_texture_mode()

            self.draw_to_window()
            

        self.unload()
    
    def draw_to_window(self):
        begin_drawing()
        draw_texture_pro(self.screen.texture, self.SCREEN_SOURCE_REC, self.SCREEN_DEST_REC, Vector2(0, 0), 0.0, WHITE)
        end_drawing()
    
    def unload(self):
        self.tiles.unload()

        unload_render_texture(self.screen)
        close_window()

if __name__ == '__main__':
    te = TileEditor()
    te.run()