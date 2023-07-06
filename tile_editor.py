from pyray import *
import json

import assets.lib.rayhelper as rh

from assets.scripts.tiles import Tiles


class ETiles(Tiles):
    def __init__(self, gm):
        super().__init__(gm)

        self.wrap_solids = [[]]
        self.wrap_airs = [[]]

        self.wrap_db = [
            [0, 0, 1, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
            [1, 1, 1, 0],
            [1, 1, 0, 0]
        ]

        self.size = []
    
    def blank_wrap(self, size):
        return [[0 for j in range(round(size[0]+1 / 10))] for i in range(round(size[1]+1 / 10))]
    
    def remove(self, pos, solid=True):
        if solid:
            for t in self.solids:
                if [t.rect.x, t.rect.y] == pos:
                    self.solids.remove(t)
        else:
            for t in self.airs:
                if [t.rect.x, t.rect.y] == pos:
                    self.airs.remove(t)
    
    def add_w(self, pos, solid=True, v=1):
        try:
            if solid:
                self.wrap_solids[pos[1]][pos[0]] = v
            else:
                
                self.wrap_airs[pos[1]][pos[0]] = v
        except IndexError:
            print(f'Tile at {pos} out of world range! Tile not placed.')
    
    def add_f(self, pos, tile, i=0, solid=True):
        if tile == None:
            self.remove(pos, solid)
            self.add_w([round(pos[0] / 10), round(pos[1] / 10)], solid, 0)
        else:
            self.add(rh.Rect(pos[0], pos[1], 10, 10), tile, i, solid)
            self.add_w([round(pos[0] / 10), round(pos[1] / 10)], solid)
    
    def load(self, filename):
        level = super().load(filename)
        self.wrap_solids = self.blank_wrap(level['size'])
        for sk in level['solids']:
            for t in level['solids'][sk]:
                self.add_w([round(t[0] / 10), round(t[1] / 10)])
        
        self.wrap_airs = self.blank_wrap(level['size'])
        for ak in level['airs']:
            for t in level['airs'][ak]:
                self.add_w([round(t[0] / 10), round(t[1] / 10)], solid=False)
    
    def get_wrap(self, pos, solid=True):
        if solid:
            ws = self.wrap_solids
        else:
            ws = self.wrap_airs
        
        wpos = [round(pos[0]/10), round(pos[1]/10)]
        others = [
            ws[wpos[1]][wpos[0]-1],
            ws[wpos[1]-1][wpos[0]],
            ws[wpos[1]][wpos[0]+1],
            ws[wpos[1]+1][wpos[0]]
        ]
        index = 4
        for i, v in enumerate(self.wrap_db):
            if others == v:
                index = i
        if not solid:
            index += 9
        return index

    def get_tile(self, pos, solid=True):
        if solid: tiles = self.solids
        else: tiles = self.airs

        for t in tiles:
            if [t.rect.x, t.rect.y] == pos:
                return t
    
    def export(self, name):
        level = {
            'size': [self.level_size.x, self.level_size.y],
            'solids':{},
            'airs':{}
        }
        for t in self.solids:
            if t.tile not in level['solids']:
                level['solids'][t.tile] = [[t.rect.x, t.rect.y, t.i]]
            else:
                level['solids'][t.tile].append([t.rect.x, t.rect.y, t.i])
        for t in self.airs:
            if t.tile not in level['airs']:
                level['airs'][t.tile] = [[t.rect.x, t.rect.y, t.i]]
            else:
                level['airs'][t.tile].append([t.rect.x, t.rect.y, t.i])
        
        file = open('assets/levels/' + str(name) + '.json', 'w')
        file.write(json.dumps(level))
        file.close()




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
        self.cursor = [0, 0]


        self.tiles = ETiles(self)
        self.level_id = 0
        self.tiles.load(self.level_id)


        self.brush_type = 'paint'
        self.brush_tile = 'skull'
        self.brush_solid = True
        self.sel = {
            'sel':False,
            'start':[0, 0]
        }



    def get_mouse(self):
        # Translates the mouse to its real in-world position
        self.mouse = get_mouse_position()
        self.mouse = rh.vec2(self.mouse.x, self.mouse.y)
        self.mouse /= self.RATIO
        self.mouse.x += self.screen_camera.target.x
        self.mouse.y += self.screen_camera.target.y

        self.cursor = [
            round(self.mouse.x / 10) * 10,
            round(self.mouse.y / 10) * 10
        ]

    def move_camera(self, speed=2):
        if is_key_down(KeyboardKey.KEY_D): self.screen_camera.target.x += speed 
        elif is_key_down(KeyboardKey.KEY_A): self.screen_camera.target.x -= speed 
        if is_key_down(KeyboardKey.KEY_S): self.screen_camera.target.y += speed 
        elif is_key_down(KeyboardKey.KEY_W): self.screen_camera.target.y -= speed 

    


    def run(self):
        while not window_should_close():
            self.get_mouse()
            self.move_camera()
            if is_key_pressed(KeyboardKey.KEY_Z):
                self.brush_solid = not self.brush_solid
                print(f'Brush solid: {self.brush_solid}')
            
            elif is_key_pressed(KeyboardKey.KEY_Q):
                self.tiles.export(self.level_id)

            begin_texture_mode(self.screen)
            clear_background(Color(179, 120, 93, 255))

            begin_mode_2d(self.screen_camera)

            draw_rectangle_lines(0, 0, int(self.tiles.level_size.x), int(self.tiles.level_size.y), BLUE)

            self.tiles.draw()

            draw_rectangle_lines(self.cursor[0], self.cursor[1], 10, 10, WHITE)
            self.select()

            end_mode_2d()


            end_texture_mode()

            self.draw_to_window()
            self.paint()
            

        self.unload()
    
    def paint(self):
        if self.brush_type == 'paint':
            if is_mouse_button_down(0):
                i = 4
                if not self.brush_solid: i += 9
                self.tiles.add_f(self.cursor, self.brush_tile, i, self.brush_solid)
            elif is_mouse_button_down(1):
                self.tiles.add_f(self.cursor, None, solid=self.brush_solid)
    
    def select(self):
        rect = Rectangle(self.sel['start'][0], self.sel['start'][1], self.cursor[0] - self.sel['start'][0], self.cursor[1] - self.sel['start'][1])
        if is_mouse_button_pressed(2) and not self.sel['sel']:
            self.sel['sel'] = True
            self.sel['start'] = self.cursor.copy()
        if is_mouse_button_down(2) and self.sel['sel']:
            draw_rectangle_lines_ex(rect, 1.0, WHITE)
            if is_key_pressed(KeyboardKey.KEY_SPACE):
                for x in range(self.sel['start'][0], self.cursor[0], 10):
                    for y in range(self.sel['start'][1], self.cursor[1], 10):
                        pos = [x, y]
                        tile = self.tiles.get_tile(pos, self.brush_solid)
                        if tile != None:
                            tile.i = self.tiles.get_wrap(pos, self.brush_solid)

            elif is_key_pressed(KeyboardKey.KEY_F):
                for x in range(self.sel['start'][0], self.cursor[0], 10):
                    for y in range(self.sel['start'][1], self.cursor[1], 10):
                        pos = [x, y]
                        i = 4
                        if not self.brush_solid: i += 9
                        self.tiles.add_f(pos, self.brush_tile, i, self.brush_solid)
            elif is_key_pressed(KeyboardKey.KEY_E):
                for x in range(self.sel['start'][0], self.cursor[0], 10):
                    for y in range(self.sel['start'][1], self.cursor[1], 10):
                        pos = [x, y]
                        self.tiles.add_f(pos, None, solid=self.brush_solid)

        if is_mouse_button_released(2) and self.sel['sel']:
            self.sel['sel'] = False

    
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