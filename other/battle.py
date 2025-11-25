import warlock
import Beholder

ben = warlock.Warlock(name="Ben",
                      patron="The Great Old One",
                      charisma=3,
                      spells=[warlock.eldritch_blast, warlock.cure_wounds, warlock.mass_cure_wounds],
                      weapon=warlock.dagger,
                      armor=warlock.leather_armor)
bhol = Beholder.beholder()

ben.attack(bhol) # type: ignore
print(f"Beholder HP after attack: {bhol.hp}")