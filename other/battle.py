from . import warlock
from . import Beholder

ben = warlock.Warlock(name="Ben",
                      patron="The Great Old One",
                      charisma=3,
                      spells=[warlock.eldritch_blast, warlock.cure_wounds, warlock.mass_cure_wounds],
                      weapon=warlock.dagger,
                      armor=warlock.leather_armor)
bhol = Beholder.beholder()

ben.attack(target=bhol) # pyright:ignore[reportArgumentType]
print(f"Beholder HP after attack: {bhol.hp}")