"""Edited 9/22/2026 - Garrison Moore

DUNGEON CRAWLER !

This program will procedurally generate a maze-like dungeon for the player to traverse.

Map is created using a 'tree' data structure:
    * Tree 'trunk' - The direct path from the entrance to exit.
    * Tree 'branches' - Decoy rooms attached to the trunk, lead to dead ends.

Combat uses a 3 input per turn, stamina bound system. Creates a heavy survival-like combat system with consequences.
    * Options:
        * 'a' = Attack (deal heavy damage, costs SP)
        * 'd' = Defend (build hyper-armour for 1 turn, costs SP)
        * 'r' = Recharge SP (Recharge stamina points)
        * 'h' = Heal (recharge health, costs SP)
"""

from Orchestrator import Orchestrator
import Tools

# intro
print(f"\n{Tools.CYAN}========================================{Tools.RESET}")
print(f"{Tools.GREEN}       TERMINAL DUNGEON CRAWLER         {Tools.RESET}")
print(f"{Tools.CYAN}========================================{Tools.RESET}")

GameMaster = Orchestrator()

# instructions
print(f"\nWelcome to the dungeon, {Tools.CYAN}{GameMaster.PC.name}{Tools.RESET}.")
print(f"\n{Tools.YELLOW}HOW TO PLAY:{Tools.RESET}")
print(f" * Navigate the maze using directional string commands ({Tools.GREEN}left, right, straight, back{Tools.RESET}).")
print(f" * Combat uses a {Tools.CYAN}3-action combo system{Tools.RESET} per turn (Max 3 inputs).")
print(f" * [{Tools.RED}a{Tools.RESET}] Attack   - Deals heavy damage (Costs SP)")
print(f" * [{Tools.BLUE}d{Tools.RESET}] Defend   - Builds hyperarmour shield (Costs SP)")
print(f" * [{Tools.GREEN}r{Tools.RESET}] Recharge - Restores stamina / SP")
print(f" * [{Tools.RED}h{Tools.RESET}] Heal     - Recovers HP (Costs SP)")
print(f"\n{Tools.YELLOW}WARNING:{Tools.RESET} Running out of SP leaves you exhausted and unable to act!")
print(f"Find {Tools.GREEN}Bonfires{Tools.RESET} to fully restore your stats and survive the descent.")
input(f"\nPress {Tools.GREEN}Enter{Tools.RESET} to enter the dungeon...")

GameMaster.run()