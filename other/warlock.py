import doctest

class Spell:
    """
    >>> spell = Spell("spell", 1)
    >>> print(spell)
    spell
    """
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
    
    def __str__(self):
        return self.name

eldritch_blast = Spell("Eldritch Blast", 8)
hex = Spell("Hex", 4)

class Warlock:
    """
    >>> warlock1 = Warlock("Gorath", "The Fiend", 10, [eldritch_blast], ("Dagger", 4), ("Leather", 1), 1, 0, 0)
    >>> warlock2 = Warlock("Luna", "The Archfey", 12, [eldritch_blast], ("Staff", 6), ("Cloth", 0), 1, 0, 0)
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
    >>> warlock1.gain_experience(50)
    >>> print(warlock1.experience)
    50
    >>> print(warlock1.level)
    1
    >>> warlock1.gain_experience(50)
    >>> print(warlock1.experience)
    0
    >>> print(warlock1.level)
    2
    >>> print(warlock1.hp)
    13
    >>> warlock2.hp = 20
    >>> warlock1.cast_spell("Eldritch Blast", warlock2)
    >>> print(warlock2.hp)
    9
    >>> warlock1.gain_experience(200)
    >>> print(warlock1.charisma)
    5
    >>> warlock2.hp = 20
    >>> warlock1.cast_spell("Eldritch Blast", warlock2)
    >>> print(warlock2.hp)
    7
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
    
    def get_spells(self):
        spells = []
        for spell in self.spells:
            spells.append(spell.name)
        return spells
    
    def cast_spell(self, spell_name, target):
        spells = self.get_spells()
        if spell_name in spells:
            spell = None
            for i in range(len(spells)):
                if spell_name == spells[i]:
                    spell = self.spells[i]

            target.take_damage(spell.damage + self.charisma)

    def attack(self, target):
        target.take_damage(self.weapon[1])
    
    def equip(self, item_type, item_name, item_value):
        if item_type == "weapon":
            self.weapon = (item_name, item_value)
        elif item_type == "armor":
            self.armor = (item_name, item_value)

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100
    
    def level_up(self):
        self.level += 1
        self.hp += 3
        self.charisma += 1

if __name__ == "__main__":
    doctest.testmod()