#TODO

#Give Pokémon experience for battling other Pokémon. A Pokémon’s level should increase once it gets enough experience points.

#Create specific Classes that inherit from the general Pokémon class. For example, could you create a Charmander class that has all of the functionality of a Pokémon plus some extra features?

#Let your Pokémon evolve once they hit a certain level.

#Have more stats associated with a Pokémon. In the real game, every Pokémon has stats like Speed, Attack, Defense. All of those stats effect the way Pokemon battle with each other. For example, the Pokémon with the larger Speed stat will go first in the battle.



# Create a Pokémon class. The __init__() method of our Pokémon class created variables to keep track of the Pokémon’s name, level, type (for example "Fire" or "Water"), maximum health, current health, and whether or not the Pokémon was knocked out. In our implementation, the maximum health was determined by the Pokémon’s level.
class Pokemon:
  def __init__(self, name, level, type):
    self.name = name
    self.level = level
    self.type = type
    self.max_health = self.level * 100
    self.health = self.max_health
    self.is_knocked_out = False
  
  def __repr__(self):
    return "name:  " + self.name + "\nlevel: " + str(self.level) + "\ntype:  " + self.type + "\n"

  def lose_health(self, hit_points):
    self.health -= hit_points
    print("lose " + str(hit_points) + " health.")
    print("current health: " + str(self.health))
    if self.health <= 0:
        self.knock_out()

# A potion should not be able to heal a Pokémon past its maximum health.  
  def gain_health(self, hit_points):
    self.health += hit_points
    if self.health > self.max_health:
      self.health = self.max_health
      print(self.name + " now has MAX health " + str(self.health))
    else:
      print(self.name + " now has " + str(self.health) + " health")
  
  def knock_out(self):
    self.is_knocked_out = True
    print(self.name + " knocked out!")
  
  def revive(self):
    self.is_knocked_out = False
    print(self.name + " revived!")

  def attack(self, other_pokemon):
    # TODO: replace the if with a master dictionary that contains all the lookups for type face/offs
    # https://pokemondb.net/type
    # A Pokémon that is knocked out should not be able to attack another Pokémon
    if self.is_knocked_out == True:
      print(self.name + " cannot attack when knocked out.")
      return
    
    type_multiplier = 1.0
    if self.type == "Fire":
        if other_pokemon.type == "Fire":
            type_multiplier = .5
        if other_pokemon.type == "Water":
            type_multiplier = .5
        if other_pokemon.type == "Grass":
            type_multiplier = 2
    if self.type == "Water":
        if other_pokemon.type == "Fire":
            type_multiplier = 2
        if other_pokemon.type == "Water":
            type_multiplier = .5
        if other_pokemon.type == "Grass":
            type_multiplier = .5
    if self.type == "Grass":
        if other_pokemon.type == "Fire":
            type_multiplier = .5
        if other_pokemon.type == "Water":
            type_multiplier = 2
        if other_pokemon.type == "Grass":
            type_multiplier = .5
    # Damage calculation
    damage = self.level * 50.0 * type_multiplier
    # Inflict the calculated damage on the other Pokemon
    print(other_pokemon.name + " current health: " + str(other_pokemon.health))
    other_pokemon.lose_health(damage)
    print("attack inflicting " + str(damage) + " damage")
    print(other_pokemon.name + " current health: " + str(other_pokemon.health))
    if other_pokemon.is_knocked_out == True:
      print("you knocked out " + other_pokemon.name + "!")


# Make a Trainer class. A Trainer can have up to 6 Pokémon, which we stored in a list. A trainer also has a name, and a number of potions they can use to heal their Pokémon. A trainer also has a “currently active Pokémon”, which we represented as a number.
class Trainer:
  def __init__(self, name, potions, pokemons, current_pokemon):
    self.name = name
    self.potions = potions
    self.pokemons = pokemons
    self.current_pokemon = current_pokemon
  
  def __repr__(self):
    return "Trainer name:    " + str(self.name) + "\n" + "potions:         " + str(self.potions) + "\n" + "current_pokemon: " + str(self.pokemons[self.current_pokemon].name) + "\n"
  
  # When a potion is used, it heals the trainer’s currently active Pokémon. 
  def use_potion(self):
    potion_health_points = 100
    if self.potions > 0:
      print("using " + str(potion_health_points) + " point potion on " + self.pokemons[self.current_pokemon].name)
      self.pokemons[self.current_pokemon].gain_health(potion_health_points)
      self.potions -= 1
      print("potions remaining: " + "" + str(self.potions))
    else:
      print("no potions available")
  
  # When a trainer attacks another trainer, the currently active Pokémon deals damage to the other trainer’s current Pokémon. 
  def attack_other_trainer(self, other_trainer):
    print(self.name + " attacking " + other_trainer.name + " ")
    other_pokemon = other_trainer.pokemons[self.current_pokemon]
    self.pokemons[self.current_pokemon].attack(other_pokemon)
  
  # The trainer is able to switch which Pokémon is currently active.
  def switch_current_pokemon(self, new_pokemon):
    if new_pokemon > 0 and new_pokemon < len(self.pokemons):
      if self.pokemons[new_pokemon].is_knocked_out != True:
        self.current_pokemon = new_pokemon
        print(self.name + " switching current pokemon to " + str(self.pokemons[self.current_pokemon].name))
      else:
        print("cannot switch to " + self.pokemons[new_pokemon].name + " he is knocked out.")
    else:
      raise PokemonOutOfRange

class PokemonOutOfRange(Exception):
  message = "pokemon selected was out of range" 

charmander = Pokemon("charmander", 3, "fire")
charmander.lose_health(250)
charmander.lose_health(100)
charmander.revive()

pikachu = Pokemon("pikachu", 2, "grass")
charmander.attack(pikachu)
print(charmander)
print(pikachu)

charizard = Pokemon("charizard", 4, "fire")
lucario = Pokemon("lucario", 4, "grass")

charizard.attack(lucario)

sean = Trainer("sean", 3, [pikachu, charmander], 1)
rosa = Trainer("rosa", 5, [pikachu, charizard, lucario], 1)

# knock out Rosa's charizard
for i in range(0, 7):
  sean.attack_other_trainer(rosa)

# try to select a knocked-out pokemon
rosa.switch_current_pokemon(1)

print(sean)
# Use potions until they are all used up!
for i in range(0, 4):
  sean.use_potion()

sean.attack_other_trainer(rosa)
sean.switch_current_pokemon(1)

rosa.attack_other_trainer(sean)
rosa.switch_current_pokemon(2)
print(rosa)