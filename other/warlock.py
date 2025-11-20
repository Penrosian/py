import doctest

class Warlock:
    """
    >>> warlock1 = Warlock("Gorath", "The Fiend", 10, {"Eldritch Blast": {"damage": 8}}, ("Dagger", 4), ("Leather", 1), 0, 0, 0)
    >>> warlock2 = Warlock("Luna", "The Archfey", 12, {"Eldritch Blast": {"damage": 8}}, ("Staff", 6), ("Cloth", 0), 0, 0, 0)
    >>> print(warlock1)
    Gorath
    >>> warlock1.cast_spell("Eldritch Blast", warlock2)
    >>> print(warlock2.hp)
    4
    >>> warlock1.attack(warlock2)
    >>> print(warlock2.hp)
    0
    >>> warlock2.attack(warlock1)
    >>> print(warlock1.hp)
    5
    >>> warlock1.equip("armor", "Chain Mail", 3)
    >>> print(warlock1.armor)
    ('Chain Mail', 3)
    >>> warlock2.attack(warlock1)
    >>> print(warlock1.hp)
    2
    >>> warlock1.hp = 10
    >>> warlock2.hp = 10
    >>> warlock1.charisma = 2
    >>> warlock1.cast_spell("Eldritch Blast", warlock2)
    >>> print(warlock2.hp)
    0
    """
    def __init__(self, name, patron, hp, spells, weapon, armor, level, experience, charisma):
        self.name = name
        self.patron = patron
        self.hp = hp
        self.spells = spells
        self.weapon = weapon
        self.armor = armor
        self.level = level
        self.experience = experience
        self.charisma = charisma

    def __str__(self):
        return self.name
    
    def take_damage(self, damage):
        damage -= self.armor[1]
        if damage < 0:
            damage = 0
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
    
    def cast_spell(self, spell_name, target):
        if spell_name in self.spells:
            spell = self.spells[spell_name]
            target.take_damage(spell["damage"] + self.charisma)

    def attack(self, target):
        weapon_name, weapon_damage = self.weapon
        target.take_damage(weapon_damage)
    
    def equip(self, item_type, item_name, item_value):
        if item_type == "weapon":
            self.weapon = (item_name, item_value)
        elif item_type == "armor":
            self.armor = (item_name, item_value)

if __name__ == "__main__":
    doctest.testmod()