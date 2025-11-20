import doctest

class Warlock:
    """
    >>> warlock1 = Warlock("Gorath", "The Fiend", 10, {"Eldritch Blast": {"damage": 8}}, ("Dagger", 4))
    >>> warlock2 = Warlock("Luna", "The Archfey", 12, {"Eldritch Blast": {"damage": 8}}, ("Staff", 6))
    >>> print(warlock1)
    Gorath
    >>> warlock1.cast_spell("Eldritch Blast", warlock2)
    >>> print(warlock2.hp)
    4
    >>> warlock1.attack(warlock2)
    >>> print(warlock2.hp)
    0
    """
    def __init__(self, name, patron, hp, spells, weapon):
        self.name = name
        self.patron = patron
        self.hp = hp
        self.spells = spells
        self.weapon = weapon

    def __str__(self):
        return self.name
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
    
    def cast_spell(self, spell_name, target):
        if spell_name in self.spells:
            spell = self.spells[spell_name]
            target.take_damage(spell["damage"])

    def attack(self, target):
        weapon_name, weapon_damage = self.weapon
        target.take_damage(weapon_damage)

if __name__ == "__main__":
    doctest.testmod()