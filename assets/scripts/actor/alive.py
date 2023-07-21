
class Alive:
    def alive_setup(self, health=100, attack_damage=10, attack_knockback=10, attack_effects=[]):
        self.health = health
        self.attack_damage = attack_damage
        self.attack_knockback = attack_knockback
        self.attack_effects = attack_effects

        self.effects = []
        self.dead = False

    def alive_hit(self, attacker):
        self.health -= attacker.attack_damage
        self.effects += attacker.attack_effects
        if attacker.attack_knockback > 0:
            self.movement += attacker.get_pointed_vec(self.get_pos_vec()) * attacker.attack_knockback
        if self.health <= 0:
            self.dead = True
    
    def alive_check_hit(self, actors: list):
        for a in actors:
            if self.rect.colliderect(a.rect):
                self.alive_hit(a)
    
    # def alive_run_effects(self):
    #     pass