import math
from typing import Literal, final, override

class Item:
    def __init__(self, name: str, effect: Literal["heal", "equip"], value: int):
        self.name: str = name
        self.effect: Literal["heal", "equip"] = effect
        self.value: int = value
    
    @override
    def __str__(self):
        return self.name

@final
class Spell:
    def __init__(self, name: str, damage: int, range: int, effect: Literal["damage", "heal"], max_targets: int = 1):
        self.name = name
        self.damage = damage
        self.range = range
        self.effect: Literal["damage", "heal"] = effect
        self.max_targets = max_targets
    
    @override
    def __str__(self):
        return self.name

eldritch_blast = Spell(name="Eldritch Blast", damage=8, range=120, effect="damage")
hex = Spell(name="Hex", damage=4, range=90, effect="damage")
cure_wounds = Spell(name="Cure Wounds", damage=6, range=1, effect="heal")
mass_cure_wounds = Spell(name="Mass Cure Wounds", damage=10, range=60, effect="heal", max_targets=6)

@final
class Weapon(Item):
    def __init__(self, name: str, damage: int):
        super().__init__(name=name, effect="equip", value=damage)
    
    @override
    def __str__(self):
        return self.name

dagger = Weapon(name="Dagger", damage=4)
staff = Weapon(name="Staff", damage=6)

@final
class Armor(Item):
    def __init__(self, name: str, defence: int):
        super().__init__(name=name, effect="equip", value=defence)
    
    @override
    def __str__(self):
        return self.name

leather_armor = Armor(name="Leather Armor", defence=1)
cloth_armor = Armor(name="Cloth Armor", defence=0)
chainmail_armor = Armor(name="Chainmail Armor", defence=3)

small_healing_potion = Item(name="Small Healing Potion", effect="heal", value=3)
healing_potion = Item(name="Healing Potion", effect="heal", value=7)
big_healing_potion = Item(name="Big Healing Potion", effect="heal", value=10)

class Entity:
    def __init__(self,
                 name: str = "",
                 hp: int = 10,
                 x: int = 0,
                 y: int = 0
                 ):
        self.name: str = name
        self.hp: int = hp
        self.max_hp: int = hp
        self.x: int = x
        self.y: int = y
        self.isalive: bool = True if hp > 0 else False

    @override
    def __str__(self):
        return self.name
    
    def take_damage(self, damage: int):
        if damage < 0:
            damage = 0
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
            print(f"{self.name} has died!")
            self.isalive = False
    
    def heal(self, amount: int):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp > 0:
            self.isalive = True

class Hero(Entity):
    """
    >>> hero = Hero("Arin", 15, dagger, leather_armor, 1, 0, 0, 0, [], 30)
    >>> hero.walk(10, 10)
    >>> print((hero.x, hero.y))
    (10, 10)
    >>> hero.walk(50, 50)
    Destination is too far to walk in one turn.
    >>> print((hero.x, hero.y))
    (10, 10)
    """
    def __init__(self,
                 name: str = "",
                 hp: int = 10,
                 weapon: Weapon = Weapon(name="Fists", damage=1),
                 armor: Armor = Armor(name="Cloth Armor", defence=0),
                 level: int = 1,
                 experience: int = 0,
                 x: int = 0,
                 y: int = 0,
                 inventory: list[Item] = [],
                 speed: int = 30,
                 ):
        super().__init__(name, hp, x, y)
        self.weapon: Weapon = weapon
        self.armor: Armor = armor
        self.level: int = level
        self.experience: int = experience
        self.inventory: list[Item] = inventory
        self.speed: int = speed

        self.hp: int
        self.max_hp: int
        self.x: int
        self.y: int
        self.isalive: bool
    
    @override
    def take_damage(self, damage: int):
        damage -= self.armor.value
        if damage < 0:
            damage = 0
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
            print(f"{self.name} has died!")
            self.isalive = False
    
    def walk(self, x: int, y: int):
        distance = math.dist((self.x, self.y), (x, y))
        if distance <= self.speed:
            self.x = x
            self.y = y
        else:
            print("Destination is too far to walk in one turn.")
    
    def pickup_item(self, item: Item):
        self.inventory.append(item)
    
    def use_item(self, item_name: str):
        item = self.find_item(item_name)
        if item is not None:
            if item.effect == "heal":
                self.hp += item.value
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                self.inventory.remove(item)
        else:
            print(f"No item named {item_name} found in inventory.")
    
    def equip(self, item_name: str):
        item = self.find_item(item_name)
        if item is None:
            print(f"No item named {item_name} found in inventory.")
            return
        if isinstance(item, Weapon):
            self.weapon = item
            self.inventory.remove(item)
        elif isinstance(item, Armor):
            self.armor = item
            self.inventory.remove(item)
        else:
            print(f"Item {item_name} cannot be equipped.")

    def attack(self, target: Entity):
        if math.dist((self.x, self.y), (target.x, target.y)) <= 1:
            target.take_damage(damage=self.weapon.value)
        else:
            print("Target is out of range for melee attack.")

    def gain_experience(self, amount: int):
        self.experience += amount
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100
    
    def level_up(self):
        self.level += 1
        self.max_hp += 3
        self.hp = self.max_hp
    
    def get_items(self):
        items: list[str] = []
        for item in self.inventory:
            items.append(item.name)
        return items
    
    def find_item(self, item_name: str):
        items = self.get_items()
        for i in range(len(items)):
            if item_name == items[i]:
                return self.inventory[i]
        return None
    
    def get_info(self):
        return f"\
Name: {self.name}\n\
HP: {self.hp}\n\
weapon: {self.weapon}\n\
Armor: {self.armor}\n\
Level: {self.level}\n\
Experience: {self.experience}\n\
Postion: ({self.x}, {self.y})"

@final
class Warlock(Hero):
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
    >>> warlock1.pickup_item(chainmail_armor)
    >>> warlock1.equip("Chainmail Armor")
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
    >>> warlock2.learn_spell(hex)
    >>> print(warlock2.get_spells())
    ['Eldritch Blast', 'Hex']
    >>> warlock2.pickup_item(small_healing_potion)
    >>> warlock2.use_item("Small Healing Potion")
    >>> print(warlock2.hp)
    10
    >>> warlock2.max_hp = 15
    >>> warlock2.pickup_item(healing_potion)
    >>> warlock2.use_item("Healing Potion")
    >>> print(warlock2.hp)
    15
    >>> print(warlock2.get_items())
    []
    >>> warlock3 = Warlock("Mira", "The Great Old One", 8, [mass_cure_wounds], dagger, cloth_armor, 1, 0, 0)
    >>> warlock1.max_hp = 30
    >>> warlock1.hp = 13
    >>> warlock2.hp = 10
    >>> warlock2.x = 0
    >>> warlock3.cast_spell("Mass Cure Wounds", [warlock1, warlock2])
    >>> print(warlock1.hp)
    23
    >>> print(warlock2.hp)
    15
    >>> warlock1.x = 3
    >>> warlock3.learn_spell(cure_wounds)
    >>> print(warlock3.get_spells())
    ['Mass Cure Wounds', 'Cure Wounds']
    >>> warlock3.cast_spell("Cure Wounds", warlock1)
    >>> print(warlock1.hp)
    23
    >>> warlock3.attack(warlock1)
    Target is out of range for melee attack.
    >>> print(warlock1.hp)
    23
    """
    def __init__(self,
                 name: str = "",
                 patron: str = "",
                 hp: int = 10,
                 spells: list[Spell] = [Spell(name="Eldritch Blast", damage=8, range=120, effect="damage")],
                 weapon: Weapon = Weapon(name="Fists", damage=1),
                 armor: Armor = Armor(name="Cloth Armor", defence=0),
                 level: int = 1,
                 experience: int = 0,
                 charisma: int = 0,
                 x: int = 0,
                 y: int = 0,
                 inventory: list[Item] = []
                 ):
        super().__init__(name, hp, weapon, armor, level, experience, x, y, inventory)
        self.patron = patron
        self.spells = spells
        self.charisma = charisma
    
    def cast_spell(self, spell_name: str, targets: list[Entity] | Entity):
        spell = self.get_spell(spell_name)
        if spell is not None:
            if not isinstance(targets, list):
                targets = [targets]
            if len(targets) >= spell.max_targets:
                targets = targets[:spell.max_targets]
            for target in targets:
                if math.dist((self.x, self.y), (target.x, target.y)) <= spell.range:
                    match spell.effect:
                        case "damage":
                            target.take_damage(damage=spell.damage + self.charisma)
                        case "heal":
                            target.heal(amount=spell.damage + self.charisma)
        else:
            print(f"Spell {spell_name} not found.")
    
    def learn_spell(self, spell: Spell):
        self.spells.append(spell)

    def get_spells(self):
        spells: list[str] = []
        for spell in self.spells:
            spells.append(spell.name)
        return spells
    
    def get_spell(self, spell_name: str):
        spells = self.get_spells()
        for i in range(len(spells)):
            if spell_name == spells[i]:
                return self.spells[i]
        return None
    
    @override
    def level_up(self):
        self.level += 1
        self.max_hp += 3
        self.hp = self.max_hp
        self.charisma += 1

    @override
    def get_info(self):
        return f"\
Name: {self.name}\n\
Patron: {self.patron}\n\
HP: {self.hp}\n\
Spells: {self.get_spells()}\n\
weapon: {self.weapon}\n\
Armor: {self.armor}\n\
Level: {self.level}\n\
Experience: {self.experience}\n\
Charisma: {self.charisma}\n\
Postion: ({self.x}, {self.y})"

if __name__ == "__main__":
    import doctest
    doctest.testmod()