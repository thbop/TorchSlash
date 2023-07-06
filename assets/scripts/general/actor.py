from pyray import *
import assets.lib.rayhelper as rh

class Actor:
    def __init__(self, rect: rh.Rect):
        self.rect = rect

        self.SPEED = 1

        self.z_vel = 0
        self.z = 0
        self.movement = rh.vec2(0, 0)
    
    def run_gravity(self, gravity=.3):
        if self.z > 0:
            self.z_vel -= gravity
        else:
            self.z_vel = max(self.z_vel, 0)
        
        self.z += self.z_vel
        self.z = max(self.z, 0)
    
    def get_display_rect(self):
        return Rectangle(self.rect.x, self.rect.y - self.z, self.rect.width, self.rect.height)
    
    def get_display_vec(self):
        return Vector2(self.rect.x, self.rect.y - self.z)

    def get_shadow_rect(self):
        f_height = self.rect.height / 8
        return Rectangle(self.rect.x + 1, self.rect.y + f_height * 7, self.rect.width - 2, f_height)

    def draw_shadow(self):
        draw_rectangle_rec(self.get_shadow_rect(), Color(30, 30, 30, 100))
    
    def get_pos_vec(self):
        return rh.vec2(self.rect.centerx, self.rect.centery)

    def get_pointed_vec(self, target):
        dif = ( target - self.get_pos_vec() )
        if dif == rh.vec2(0, 0):
            return rh.vec2(0, 0)
        return dif.normalize()