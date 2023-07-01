from pyray import *
from assets.scripts import general as g
import assets.lib.rayhelper as rh

from math import radians, cos
from random import randint


class Monster(g.Actor, g.Collider, g.Animator):
    def init(self, ani):
        self.ani_setup(ani, 'walk')


    def step(self, player_pos, tiles, monster_rects):
        self.movement = self.get_pointed_vec(player_pos) * self.SPEED
        self.collider_update(tiles, monster_rects)
    


class Ghost(Monster):
    def __init__(self, rect):
        super().__init__(rect)
        self.float_tick = 1

        self.tint = randint(160, 200)
    
    def run(self):
        if self.float_tick < 360:
            self.float_tick += 5
        else:
            self.float_tick = 1
        
        self.z = cos(radians(self.float_tick)) * 2 + 2

        self.ani_update()
        
    def draw(self):
        self.ani_draw(Color(self.tint, self.tint + 6, self.tint, self.tint))

class Monsters:
    def __init__(self, gm):
        self.gm = gm

        self.ss_types = {
            'ghost': rh.spritesheet('assets/graphics/monsters/ghost/sprites.png')
        }
        self.animations = {
            'ghost':{
                'walk':{
                    'speed':5,
                    'frames':[
                        self.ss_types['ghost'].image_at(Rectangle(0, 0, 9, 13)),
                        self.ss_types['ghost'].image_at(Rectangle(9, 0, 9, 13)),
                        self.ss_types['ghost'].image_at(Rectangle(18, 0, 9, 13))
                    ]
                }
            }
        }

        self.monsters = []
    
    def add(self, monster, ani_type):
        monster.init(self.animations[ani_type])
        self.monsters.append(monster)
    
    def run(self):
        for m in self.monsters:
            other_monsters = self.monsters.copy()
            other_monsters.remove(m)
            m.step(self.gm.player.pos, [], other_monsters)

            self.gm.shadows.append(m.get_shadow_rect())

            m.run()
    def draw(self):
        for m in self.monsters:
            m.draw()
    
    def unload(self):
        for ss in self.ss_types.values():
            ss.unload()