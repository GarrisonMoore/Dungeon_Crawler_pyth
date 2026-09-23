"""Edited 9/22/2026 - Garrison Moore

DUNGEON CRAWLER !

This program will procedurally generate a maze-like dungeon for the player to traverse.
Map is created using a 'tree' data structure:
    * Tree 'trunk' - The direct path from the entrance to exit.
    * Tree 'branches' - Decoy rooms attached to the trunk, lead to dead ends.

Combat uses a 3 input per turn, stamina bound system. Creates a heavy survival like combat system with consequences.
    * Options:
        * 'a' = Attack (deal heavy damage, costs SP)
        * 'd' = Defend (build hyper-armour for 1 turn, costs SP)
        * 'r' = Recharge SP (Recharge stamina points)
        * 'h' = Heal (recharge health, costs SP)"""


import game
import colors

# intro
print(f"\n{colors.CYAN}========================================{colors.RESET}")
print(f"{colors.GREEN}       TERMINAL DUNGEON CRAWLER         {colors.RESET}")
print(f"{colors.CYAN}========================================{colors.RESET}")

Narrator = game.Game()

# instructions
print(f"\nWelcome to the dungeon, {colors.CYAN}{Narrator.PC.name}{colors.RESET}.")
print(f"\n{colors.YELLOW}HOW TO PLAY:{colors.RESET}")
print(f" * Navigate the maze using directional string commands ({colors.GREEN}left, right, straight, back{colors.RESET}).")
print(f" * Combat uses a {colors.CYAN}3-action combo system{colors.RESET} per turn (Max 3 inputs).")
print(f" * [{colors.RED}a{colors.RESET}] Attack  - Deals heavy damage (Costs SP)")
print(f" * [{colors.BLUE}d{colors.RESET}] Defend  - Builds hyperarmour shield (Costs SP)")
print(f" * [{colors.GREEN}r{colors.RESET}] Recharge- Restores stamina / SP")
print(f" * [{colors.RED}h{colors.RESET}] Heal    - Recovers HP (Costs SP)")
print(f"\n{colors.YELLOW}WARNING:{colors.RESET} Running out of SP leaves you exhausted and unable to act!")
print(f"Find {colors.GREEN}Bonfires{colors.RESET} to fully restore your stats and survive the descent.")
input(f"\nPress {colors.GREEN}Enter{colors.RESET} to enter the dungeon...")

Narrator.run()