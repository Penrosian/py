import doctest
import math

class Spell:
    """
    >>> spell = Spell("spell", 1, 50)
    >>> print(spell)
    spell
    """
    def __init__(self, name: str, damage: int, range: int):
        self.name = name
        self.damage = damage
        self.range = range
    
    def __str__(self):
        return self.name

eldritch_blast = Spell("Eldritch Blast", 8, 120)
hex = Spell("Hex", 4, 90)

class Weapon:
    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage
    
    def __str__(self):
        return self.name

dagger = Weapon("Dagger", 4)
staff = Weapon("Staff", 6)

class Armor:
    def __init__(self, name: str, ap: int):
        self.name = name
        self.ap = ap
    
    def __str__(self):
        return self.name

leather_armor = Armor("Leather Armor", 1)
cloth_armor = Armor("Cloth Armor", 0)
chainmail_armor = Armor("Chainmail Armor", 3)

class Warlock:
    """
    >>> warlock1 = Warlock("Gorath", "The Fiend", 10, [eldritch_blast], dagger, leather_armor, 1, 0, 0)
    >>> warlock2 = Warlock("Luna", "The Archfey", 12, [eldritch_blast], staff, cloth_armor, 1, 0, 0)
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
    >>> warlock1.equip(chainmail_armor)
    >>> print(warlock1.armor)
    Chainmail Armor
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
    >>> warlock2.x = 200
    >>> warlock1.cast_spell("Eldritch Blast", warlock2)
    >>> print(warlock2.hp)
    7
    """
    def __init__(
                self,
                name: str = "",
                patron: str = "",
                hp: int = 10,
                spells: list[Spell] = [Spell("Eldritch Blast", 8, 120)],
                weapon: Weapon = Weapon("Fists", 1),
                armor: Armor = Armor("Cloth Armor", 0),
                level: int = 1,
                experience: int = 0,
                charisma: int = 0,
                x: int = 0,
                y: int = 0,
                ):
        self.name = name
        self.patron = patron
        self.hp = hp
        self.spells = spells
        self.weapon = weapon
        self.armor = armor
        self.level = level
        self.experience = experience
        self.charisma = charisma
        self.x = x
        self.y = y

    def __str__(self):
        return self.name
    
    def take_damage(self, damage):
        damage -= self.armor.ap
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
            if spell is not None:
                if math.dist((self.x, self.y), (target.x, target.y)) <= spell.range:
                    target.take_damage(spell.damage + self.charisma)

    def attack(self, target):
        target.take_damage(self.weapon.damage)
    
    def equip(self, item):
        if isinstance(item, Weapon):
            self.weapon = item
        elif isinstance(item, Armor):
            self.armor = item

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100
    
    def level_up(self):
        self.level += 1
        self.hp += 3
        self.charisma += 1

    def get_info(self):
        return f"\
Name: {self.name}\n\
Patron: {self.patron}\n\
HP: {self.hp}\n\
Spells: {self.get_spells()}\n\
Weapon: {self.weapon}\n\
Armor: {self.armor}\n\
Level: {self.level}\n\
Experience: {self.experience}\n\
Charisma: {self.charisma}\n\
Postion: ({self.x}, {self.y})"

warlock = Warlock("Gnar", "The Fiend", 35, [eldritch_blast], staff, chainmail_armor, 1, 0, 2)
print(warlock.get_info())

if __name__ == "__main__":
    doctest.testmod()