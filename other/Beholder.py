"""
Attributes:
- hp
- damage
- mana
- tentacles

Behaviors:
- bite()
- eye_rays()
- tentacle_attack()
- intimidate()
- take_damage()
- deal_damage()
- isalive()
"""
import random
class beholder:
    def init(self, hp=2000000000, damage=100000000, mana=10000000000, scare=10000000):
        self.hp = hp
        self.isalive = True
        self.name = "Beholder"
        self.damage = damage
        self.mana = mana
        self.scare = scare
    
    def gold(self, wealth):
        self.wealth = wealth
        if self.wealth <= 5:
            print("You are poor, rob someone to get some money.")
        elif self.wealth >= 500:
            print("Calm down buddy, leave some money for the rest of us.")

    def speed(self, speed=100):
        if gold >= 100:
            self.speed = 75
        elif gold >= 200:
            self.speed = 50
        elif gold >= 500:
            self.speed = 25
            print("You have too much money, try to buy something.")
    
    def rob(self, rob_chance):
        self.rob_chance = rob_chance
        s = random.randint (0,5)
        if s == 2:
            print("Robbery successfull, congratulations.")
            self.wealth += random.randint(0, 50)
        else:
            print("Sorry, the robbery failed.")

    
    def intimidate(self):
        self.scare = 25
        if self.scare >= 25:
            self.damage += 1
            print(f"{self.name} intimidates, increasing damage to {self.damage}.")
   
    def dead(self):
        if self.hp <= 0 or self.mana <= 0:
            self.isalive = False
        if not self.isalive:
            print(f"{self.name} is defeated. Game Over.")
            return 0
        return 1

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.name} takes {damage} damage. HP: {self.hp}")
        if self.hp <= 0:
            self.hp = 0
            self.isalive = False
            self.dead()
    def deal_damage(self, target, damage_amount):
        if self.isalive and self.mana >= 0:
            print(f"{self.name} attacks {target.name} for {damage_amount} damage!")
            target.take_damage(damage_amount)
            if not target.is_alive:
                print(f"{target.name} has been defeated!")
        else:
            print(f"{self.name} cannot attack (not alive or out of mana).")


   
    def bite(self):
        self.damage = 25
        self.mana -= 25
        deal_damage()     
   
    def eye_rays(self):
        self.damage = 50
        self.mana -= 50
        deal_damage()
    
    def tentacle_attack(self):
        self.damage = 50
        self.mana -= 50
        deal_damage()

    def attack_chance(self):
        s = random.randint(0,1000)
        if s <= 500:
            print("Congrats, hit successfull.")
        else:
            print("Sorry, hit failed.")
baseStats = {'Health' : 200, 'bite_damage' : 25, 'tentacle_attack_damage' : 50, 'eye_rays_damage' : 50}


def lore(self):
    print("The beholder was originally created in 1974 by Terry Kuntz, the brother of one of the D&D creators Gary Gygax's players, during an early campaign. The beholder hoards treasure and dominates it's enviroment, using it's abilities and intelligence to trap and eliminate it's intruders. Beholders also like to warp reality through their nightmares, creating new beholders.")


class DummyTarget:
     def __init__(self, health=100):
        self.health = health
        self.is_alive = True
        self.name = "Training Dummy"

    
     def take_damage(self, damage):
        """Take damage without any special effects."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False







if __name__ == "__main__":
    import doctest
    doctest.testmod()

