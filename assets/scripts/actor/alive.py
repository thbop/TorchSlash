
class Alive:
    def alive_setup(self, health=100):
        self.health = health
        # self.resistance = 1
        self.effects = []
        self.dead = False

    def alive_hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
    
    # def alive_run_effects(self):
    #     pass