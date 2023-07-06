from pyray import *
from assets.scripts import general as g
import assets.lib.rayhelper as rh


class Weapon(g.Actor):
    def __init__(self, player):
        super().__init__(rh.Rect(0, 0, 4, 9))
        self.player = player

        self.pos = rh.vec2(0, 0)

        self.ss = rh.spritesheet('assets/graphics/weapon.png')

        self.sprites = {
            'wand': self.ss.image_at(Rectangle(0, 0, 3, 6))
        }
        self.current = 'wand'

    
    def run(self):
        self.z = self.player.z
        self.pos = rh.vec2(self.player.pos.x - 3, self.player.pos.y - 3 - self.z) + self.player.direction * 8 # Baad code

        self.player.gm.particles.emit(rh.vec2(self.pos.x + 1, self.pos.y + 2), .6, 1)

        draw_texture_v(self.sprites[self.current], self.pos.toray(), WHITE)
    
    def unload(self):
        self.ss.unload()


class Player(g.Actor, g.Collider, g.Animator):
    def __init__(self, gm, actors):
        self.gm = gm
        self.actors = actors

        super().__init__(rh.Rect(10, 10, 9, 13))

        self.SPEED = 1.4
        self.DECEL = 0.6
        self.JUMP_VEL = 3

        self.ss = rh.spritesheet('assets/graphics/player/sprites.png')
        base_image = self.ss.image_at(Rectangle(0, 0, 9, 13))
        self.ani_setup(
            ani={
                'idle':{
                    'speed':20,
                    'frames':[
                        base_image,
                        self.ss.image_at(Rectangle(9, 0, 9, 13))
                    ]
                },
                'walk':{
                    'speed':6,
                    'frames':[
                        base_image,
                        self.ss.image_at(Rectangle(0, 13, 9, 13))
                    ]
                },
                'jump':{
                    'speed':6,
                    'frames':[
                        base_image,
                        self.ss.image_at(Rectangle(0, 25, 9, 13)),
                        self.ss.image_at(Rectangle(9, 25, 9, 13)),
                        self.ss.image_at(Rectangle(0, 25, 9, 13))
                    ]
                }
            },
            state='idle'
        )

        self.weapon = Weapon(self)

        self.direction = rh.vec2(1, 0)
        self.pos = self.get_pos_vec()
    
    def animate(self):
        if abs(self.movement.x) < 0.5 and abs(self.movement.y) < 0.5:
            self.ani_state = 'idle'
        else:
            self.ani_state = 'walk'
        
        if self.z > 0:
            self.ani_state = 'jump'
            self.ani_onetime = True

        self.ani_update()
        self.ani_draw()
    
    def run(self):
        self.run_gravity()
        self.pos = self.get_pos_vec()

        if is_mouse_button_down(0) and self.pos.distance_to(self.gm.mouse) > self.rect.width - 2:
            self.movement = self.get_pointed_vec(self.gm.mouse) * self.SPEED
            self.direction = self.movement.copy()
        else:
            self.movement *= self.DECEL
        

        if is_key_pressed(KeyboardKey.KEY_Z) and self.z < 0.2:
            self.z_vel = self.JUMP_VEL


        self.collider_update(self.gm.tiles.solids, [])

        

        self.gm.shadows.append(self.get_shadow_rect())


    
    def draw(self):
        self.weapon.run()
        self.animate()
    
    def unload(self):
        self.ss.unload()
        self.weapon.unload()
        
        
