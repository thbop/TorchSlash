from pyray import *

class Collider:
    def collider_setup(self):
        pass

    def collider_get_rects(self, tiles, actors):
        rects = []
        for o in tiles + actors:
            rects.append(o.rect)
        return rects
            
    
    def collider_collision_test(self, rects):
        hit_list = []
        for r in rects:
            if self.rect.colliderect(r):
                hit_list.append(r)
        return hit_list

    def collider_update(self, tiles, actors):
        collision_types = {'top':False, 'bottom':False, 'right':False, 'left':False}
        rects = self.collider_get_rects(tiles, actors)

        self.rect.x += self.movement.x
        hit_list = self.collider_collision_test(rects)
        for t in hit_list:
            if self.movement.x > 0:
                self.rect.right = t.left
                collision_types['right'] = True
            elif self.movement.x < 0:
                self.rect.left = t.right
                collision_types['left'] = True
        
        self.rect.y += self.movement.y
        hit_list = self.collider_collision_test(rects)
        for t in hit_list:
            if self.movement.y > 0:
                self.rect.bottom = t.top
                collision_types['bottom'] = True
            elif self.movement.y < 0:
                self.rect.top = t.bottom
                collision_types['top'] = True
        
        return collision_types