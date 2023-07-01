from pyray import *
from assets.scripts import general as g
import assets.lib.rayhelper as rh

from random import uniform, randint

class Particle(g.Actor):
    def __init__(self, rect, movement):
        super().__init__(rect)
        self.movement = movement

        self.lifetime = randint(8, 15)
        self.color = Color(
            randint(200, 255),
            randint(100, 150),
            randint(100, 120),
            255
        )
    
    def run(self):
        
        self.lifetime -= 1

        draw_rectangle_rec(self.get_display_rect(), self.color)

class Particles:
    def __init__(self):
        self.particles = []
        self.wind = rh.vec2(-.02, .05)
    
    def add(self, particle):
        self.particles.append(particle)
    
    def emit(self, pos, max_speed=1.0, amount=15):
        for p in range(amount):
            self.add(Particle(
                rh.Rect(pos.x, pos.y, 1, 1),
                rh.vec2(uniform(-max_speed, max_speed), uniform(-max_speed-0.5, max_speed))
            ))
    
    def run(self):
        remove_list = []
        for p in self.particles:
            p.movement += self.wind
            p.rect.x += p.movement.x
            p.rect.y += p.movement.y

            p.run()
            if p.lifetime <= 0:
                remove_list.append(p)

        for p in remove_list:
            self.particles.remove(p)
    