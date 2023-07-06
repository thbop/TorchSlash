from pyray import *
from assets.scripts import actor as g
import assets.lib.rayhelper as rh

from .player import Player
from .monsters import *


class Actors:
    def __init__(self, gm):
        self.gm = gm

        self.player = Player(gm, self)
        self.monsters = Monsters(gm, self)
    
    def get_all(self):
        return [self.player] + self.monsters.monsters
    

    
    def run(self):
        self.player.run()
        self.monsters.run()
    
    def draw(self):
        actors = self.get_all()
        for i in range(int(self.gm.screen_camera.target.y), self.gm.SCREEN_HEIGHT + int(self.gm.screen_camera.target.y)):
            remove_list = []
            for a in actors:
                if round(a.rect.y) == i:
                    a.draw()
                    remove_list.append(a)
            for a in remove_list:
                actors.remove(a)
            
    
    def unload(self):
        self.player.unload()
        self.monsters.unload()