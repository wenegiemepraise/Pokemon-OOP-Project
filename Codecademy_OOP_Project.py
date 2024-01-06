from random import randint
class Pokemon_Trainer():
    def __init__(self, name, badges):
        self.name =  name
        self.badges = badges
        self.pokemon_team = []
        self.item_bag = []
        self.mega_stone_bag = []

    def __repr__(self) -> str:
        return f"{self.name} is a formidable trainer with {self.badges} gym badges and a pokemon team consisting of {self.pokemon_team} pokemon!"
    
    def show_pokemon(self):
        return [pokemon.name.capitalize() for pokemon in self.pokemon_team]
    
    # Add pokemon created from pokemon class to the team
    def add_pokemon(self, Pokemon):
        if len(self.pokemon_team) < 6:
            self.pokemon_team.append(Pokemon)
        else:
            print("You have a full team")

        return f"Your current team is: {self.pokemon_team}"

    #Remove a pokemon on your team 
    def remove_pokemon(self, Pokemon):
        if Pokemon in self.pokemon_team:
            self.pokemon_team.remove(Pokemon)
        else:
            print(f"{Pokemon.name} is not on your team")

        return f"Your updated team is {self.pokemon_team}"

    def add_to_item_bag(self, Item):
        if len(self.item_bag) < 4:
            self.item_bag.append(Item)

        return f"The Items in your bag are {self.item_bag}"

    def remove_from_item_bag(self, Item):
        if Item in self.item_bag:
            self.item_bag.remove(Item)
        
        return f"The Items in your bag are {self.item_bag}"

    def add_mega_stone(self, Mega_stone):
        if self.name.capitalize == "Praise" and len(self.mega_stone_bag) < 3:
            self.mega_stone_bag.append(Mega_stone)
        elif len(self.mega_stone_bag) < 1:
            self.mega_stone_bag.append(Mega_stone)

        return f"The Mega Stones you have are {self.mega_stone_bag}"
    
    def remove_mega_stone(self, Mega_stone):
        for stone in self.mega_stone_bag:
            if stone.name_mega_stone == Mega_stone.name_mega_stone:
                self.mega_stone_bag.remove(stone)
                break

    def use_revive(self, Pokemon, Item):
        if Item.name.title() == "Weak Revive":
            revived_hp = Pokemon.weak_revive()
        elif Item.name.title() == "Strong Revive":
            revived_hp = Pokemon.strong_revive()
        else:
            return f"{Item.name_item} is not a valid item"
        if Item in self.item_bag:
            self.item_bag.remove(Item)
            return f"{Pokemon.name} has been revived with {revived_hp} using {Item.name_item}."
        else:
            return f"You don't have {Item.name_item} in your bag."
        
    def use_mega_stone(self, Pokemon, Mega_stone):
        if Pokemon.has_mega_evolved == True:
            return f"{Pokemon.name} is already mega evolved!"
        
        if Mega_stone.name_mega_stone in [stone.name_mega_stone for stone in self.mega_stone_bag]:
            # Check if the Mega Stone is compatible with the Pokemon's type
            if (Pokemon.typing.lower() == "fire" and Mega_stone.name_mega_stone == "Charmandernite") or \
               (Pokemon.typing.lower() == "water" and Mega_stone.name_mega_stone == "Blastoisnite") or \
               (Pokemon.typing.lower() == "grass" and Mega_stone.name_mega_stone == "Venusaurite"):
                
                # Apply Mega Stone boosts to the Pokemon
                Pokemon.apply_mega_stone_boosts(Mega_stone)

                # Remove the used Mega Stone from the bag
                self.remove_mega_stone_from_bag(Mega_stone)

                return f"{Pokemon.name} has used {Mega_stone.name_mega_stone}. " \
                       f"Now, it has boosted stats: HP x {Mega_stone.hp_boost}, " \
                       f"Attack x {Mega_stone.attack_boost}, " \
                       f"Defence x {Mega_stone.defence_boost}."
            else:
                return f"{Pokemon.name} cannot use {Mega_stone.name_mega_stone} due to incompatible typing."
        else:
            return f"You don't have {Mega_stone.name_mega_stone} in your Mega Stone bag."
        
    #Need to implement this!
    def use_potion(self, Pokemon, Item):
        if Pokemon.knocked_out:
            return f"{Pokemon.name} has been knocked out, and you need to revive it to use the potion."

        if Item.name_item.lower() == "heal":
            healed_hp = Pokemon.heal(Item.hp_buff)
            self.remove_from_item_bag(Item)
            return f"{Pokemon.name} has been healed with {healed_hp} using {Item.name_item}."
        else:
            return f"{Item.name_item} is not a valid healing item."


class Pokemon():
    def __init__(self, name, typing, attack1, attack2, defence, hp):
        self.name = name
        self.typing = typing
        self.attack1 = attack1
        self.attack2 = attack2
        self.defence = defence
        self.hp = hp
        self.knocked_out = False
        self.has_mega_evolved = False

    def __repr__(self) -> str:
        return f"{self.name} is a {self.typing} type pokemon with {self.hp} hp, {self.defence} defence and {self.attack1} dmg first attack and {self.attack2} dmg for his second attack."
    
    def fun_fact(self):
        if self.typing.lower() == "fire":
            return f"Fire type pokemon are great against grass types but watch out they take double the damage against water types!!"
        elif self.typing.lower() == "water":
            return f"Water type pokemon are great against fire types but watch out they take double the damage against grass types!!"
        else:
            return f"Grass type pokemon are great against water types but watch out they take double the damage against fire types!!"
        
    def fainted(self):
        if self.hp == 0:
            self.knocked_out = True
            return f"{self.name} hp has fallen to 0 and is now knocked out"
        else:
            return f"{self.name} still have some fight left in him! {self.hp} hp remaining."
        
    def weak_revive(self):
        if self.knocked_out == True:
            self.hp += 20
            self.knocked_out = False
            f"{self.name} has been revived with 20 health points."
            return 20
        else:
            print(f"{self.name} has not fallen yet. {self.hp} hp remains")
            return 0
        
    def strong_revive(self):
        if self.knocked_out == True:
            self.hp += 45
            self.knocked_out = False
            print(f"{self.name} has been revived with 45 health points")
            return 45
        else:
            print(f"{self.name} has not fallen yet. {self.hp} hp remains")
            return 0
        
        
    def loose_health(self, amount):
        amount -= self.defence
        self.hp += self.revived_hp  # Add the revived health before subtracting damage
        self.hp -= amount 

        self.revived_hp = 0

        if self.hp <= 0:
            self.hp = 0
            self.knocked_out()
        else:
            return f"{self.name} has taken significant damage. He lost {amount} hp!"
        
    def apply_mega_stone_boosts(self, mega_stone):
        self.hp *= mega_stone.hp_boost
        self.attack *= mega_stone.attack_boost
        self.defence *= mega_stone.defence_boost
        self.has_mega_evolved = True
        
    #Need to implement this!
    def attack_pokemon(self, other_pokemon):
            # Check if the attacking Pokemon is knocked out
        if self.knocked_out:
            return f"{self.name} is knocked out and cannot attack."

            # Calculate the damage based on the attack power
        damage = self.attack1 if randint(0, 1) == 0 else self.attack2

            # Apply damage to the other Pokemon
        other_pokemon.loose_health(damage)

        return f"{self.name} attacked {other_pokemon.name} with {damage} damage!"
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > 100:
            self.hp = 100  # Cap the HP at 100
        return amount

class Item():
    def __init__(self, name_item, hp_buff):
        self.name_item = name_item
        self.hp_buff = hp_buff

    def __repr__(self) -> str:
        return f"{self.name_item} is an item that can be used to assist pokemon in battle."
    
        
class Mega_stone():
    def __init__(self, name_mega_stone, hp_boost, attack_boost, defence_boost):
        self.name_mega_stone = name_mega_stone
        self.hp_boost = hp_boost
        self.attack_boost = attack_boost
        self.defence_boost = defence_boost

    def __repr__(self) -> str:
        return f"{self.name_mega_stone} is ancient stone that can give a single pokemon on your team immeasurable power!"    
        
    
        
        
    
#Fire Moves      
ember =  15
fire_claw = 25

#Water Moves
bubble = 10
water_gun = 30

#Grass Moves
razor_leaf = 10
giga_drain = 20

#Items
#Revives
weak_revive_info = ["weak revive", 20]
strong_revive_info= ["strong revive", 45]
#Potions
heal_info = ["heal", 30]
super_heal_info = ["super heal", 55]

#Mega Stones
fire_stone_info = ["Charmandernite", 1.5, 2, 1.3]
water_stone_info = ["Blastoisinite", 1.5, 1.3, 2]
grass_stone_info = ["Venusaurite", 2, 1.5, 1.3]
