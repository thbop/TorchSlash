from pyray import *
# import assets.lib.rayhelper as rh

class Ui:
    def __init__(self, gm):
        self.gm = gm
        self.states = ['ingame']
    
    def get_mouse(self):
        # Translates the mouse to its on screen position
        self.mouse = get_mouse_position()
        self.mouse.x /= self.gm.RATIO
        self.mouse.y /= self.gm.RATIO
    
    def button(self, rect, text, onclick=None):
        
        if check_collision_point_rec(self.mouse, rect):
            draw_rectangle_lines_ex(rect, 1.0, RAYWHITE)
            if is_mouse_button_pressed(0) and onclick != None:
                onclick()
        draw_line(int(rect.x + 1), int(rect.y + rect.height - 1), int(rect.x + rect.width - 1), int(rect.y + rect.height - 1), WHITE)
        draw_text(text, int(rect.x + 2), int(rect.y + 1), 10, WHITE)

    
    def play(self):
        self.states.remove('paused')
    
    def overlay(self):
        draw_rectangle(0, 0, self.gm.SCREEN_WIDTH, self.gm.SCREEN_HEIGHT, Color(30, 30, 35, 200))

    def paused(self):
        self.overlay()
        self.button(Rectangle(10, 10, 50, 11), 'Play', self.play)
        self.button(Rectangle(10, 25, 50, 11), 'Controls', self.play)
        self.button(Rectangle(10, 40, 50, 11), 'Back', self.play)
    
    def hud(self, health):
        draw_rectangle_lines_ex(Rectangle(10, 10, 50, 10), 1, WHITE)
        draw_rectangle_rec(Rectangle(11, 11, health, 8), RED)

    def run(self):
        self.get_mouse()

        for s in self.states:
            if s == 'paused':
                self.paused()