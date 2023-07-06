from pyray import *
import json

import assets.lib.rayhelper as rh

class Tile:
    def __init__(self, rect, tile, i):
        self.rect = rect
        self.tile = tile # This defines the type of tile
        self.i = i # This defines the specific corner, edge, middle, and wall/floor of the tile. (Check graphics/tiles/ref.png for indexes)

class TileType:
    def __init__(self, filename):
        self.ss = rh.spritesheet('assets/graphics/tiles/' + filename)
        
        self.i = [
            self.ss.image_at(Rectangle(0, 0, 10, 10)),
            self.ss.image_at(Rectangle(10, 0, 10, 10)),
            self.ss.image_at(Rectangle(20, 0, 10, 10)),
            self.ss.image_at(Rectangle(0, 10, 10, 10)),
            self.ss.image_at(Rectangle(10, 10, 10, 10)),
            self.ss.image_at(Rectangle(20, 10, 10, 10)),
            self.ss.image_at(Rectangle(0, 20, 10, 10)),
            self.ss.image_at(Rectangle(10, 20, 10, 10)),
            self.ss.image_at(Rectangle(20, 20, 10, 10)),
            self.ss.image_at(Rectangle(0, 30, 10, 10)),
            self.ss.image_at(Rectangle(10, 30, 10, 10)),
            self.ss.image_at(Rectangle(20, 30, 10, 10)),
            self.ss.image_at(Rectangle(0, 40, 10, 10)),
            self.ss.image_at(Rectangle(10, 40, 10, 10)),
            self.ss.image_at(Rectangle(20, 40, 10, 10)),
            self.ss.image_at(Rectangle(0, 50, 10, 10)),
            self.ss.image_at(Rectangle(10, 50, 10, 10)),
            self.ss.image_at(Rectangle(20, 50, 10, 10))
        ]
    
    def unload(self):
        self.ss.unload()

class Tiles:
    def __init__(self, gm):
        self.gm = gm

        self.tile_types = {
            'test': TileType('ref.png'),
            'skull': TileType('skull.png')
        }

        self.solids = []
        self.airs = [] # These tiles are displayed but do not collide with actors
    
    def add(self, rect, tile, i, solid=True):
        if solid:
            self.solids.append(Tile(rect, tile, i))
        else:
            self.airs.append(Tile(rect, tile, i))
    
    def load(self, name):
        file = open('assets/levels/' + str(name) + '.json')
        level = json.load(file)
        file.close()

        for sk in level['solids']:
            for t in level['solids'][sk]:
                self.add(rh.Rect(t[0], t[1], 10, 10), sk, t[2])
        for ak in level['airs']:
            for t in level['airs'][ak]:
                self.add(rh.Rect(t[0], t[1], 10, 10), ak, t[2], solid=False)
    
    def draw(self):
        for t in self.solids + self.airs:
            draw_texture_rec(
                self.tile_types[t.tile].i[t.i],
                t.rect.toray(),
                t.rect.toray_vec2(),
                WHITE
            )
    
    def unload(self):
        for tt in self.tile_types.values():
            tt.unload()

    
