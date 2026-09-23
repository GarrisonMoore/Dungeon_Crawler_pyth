from random import randint
from random import choice
import colors

# Using a dictionary to store different characters and their stats
mob_list = {
    "Goblin": {"hp":10, "sp":10},
    "Orc": {"hp":20, "sp":20},
    "Troll": {"hp":40, "sp":40}
}

class Character:
    """Universal Character class to initialize character data"""
    def __init__(self,name,hp,sp):
        self.name = name
        self.hp = hp
        self.sp = sp
        self.hyperarmour = 0

    # formatting character data for the terminal
    def __str__(self):
        return f"{self.name, self.hp, self.sp}"

class Player(Character):
    """Player class to initialize player data"""
    def __init__(self,hp,sp,xp):
        user_name = input("What is your warriors name? ")
        self.hp = hp
        self.sp = sp
        self.max_hp = hp
        self.max_sp = sp
        self.xp = xp
        self.level = 1
        self.xp_to_next_level = 100

        self.is_Player = True

        super().__init__(user_name,hp,sp)

        # start player xp at 0
        self.xp = 0

    def move(self,current_node):

        while True:
            player_action = input("Where to? ")

            # if the action is a valid door, move to the next room
            if player_action in current_node.paths and current_node.paths[player_action] is not None:
                current_node = current_node.paths[player_action]
                break
            else:
                print("You can't go that way!")
                continue

        return  current_node

    def gain_xp(self, amount):
        """Method to add xp to the player and level up if necessary"""
        self.xp += amount
        print(f"{colors.CYAN}{self.name}{colors.RESET} gained {colors.GREEN}+{amount}{colors.RESET} XP!")

        # check if player has reached the next level
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            # increase max hp and sp by 20 for every level
            self.max_hp += 20
            self.max_sp += 20
            self.hp = self.max_hp
            self.sp = self.max_sp

            print(f"{colors.CYAN}{self.name}{colors.RESET} leveled up to level {colors.GREEN}{self.level}{colors.RESET}!")
            print(f"Max HP and SP increased by {colors.GREEN}20{colors.RESET}!")

class Mob(Character):
    """Mob class to initialize mob data"""
    def __init__(self,name,hp,sp):
        self.name = name
        self.hp = hp
        self.sp = sp
        self.max_hp = hp
        self.max_sp = sp

        super().__init__(name,hp,sp)

def call_mob(current_level):
    """Randomly selects a mob from the mob_list dictionary and scales its stats based on the current level."""
    mob_name = choice(list(mob_list.keys()))

    # get mob stats from the mob_list dictionary
    stats = mob_list[mob_name]

    # scale the mob's stats based on the current level
    scaled_hp = stats["hp"] * (current_level)
    scaled_sp = stats["sp"] * (current_level)

    # return a Mob object with the scaled stats
    return Mob(name = mob_name, hp = scaled_hp, sp = scaled_sp)