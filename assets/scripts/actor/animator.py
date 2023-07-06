from pyray import *
from math import copysign

class Animator:
    def ani_setup(self, ani, state):
        self.ani = ani
        self.ani_tick = 0
        self.ani_frame = 0
        self.ani_state = state
        self.ani_direction = 1

        self.ani_onetime = False

    def ani_update(self):
        self.ani_direction = copysign(self.ani_direction, self.movement.x)
        self.ani_tick += 1
        if self.ani_tick > self.ani[self.ani_state]['speed']:
            self.ani_tick = 0
            self.ani_frame += 1
        if self.ani_frame > len( self.ani[self.ani_state]['frames'] )-1:
            if self.ani_onetime:
                self.ani_onetime = False
            self.ani_frame = 0
        
    

                
    def ani_draw(self, tint=WHITE):
        
        tex = self.ani[self.ani_state]['frames'][self.ani_frame]

        draw_texture_pro(tex, Rectangle(0, 0, 9 * self.ani_direction, 13), self.get_display_rect(), Vector2(0, 0), 0.0, tint)