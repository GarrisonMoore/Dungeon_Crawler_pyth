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
        * 'h' = Heal (recharge health, costs SP)"""


from Orchestrator import Game
import Colors

# intro
print(f"\n{Colors.CYAN}========================================{Colors.RESET}")
print(f"{Colors.GREEN}       TERMINAL DUNGEON CRAWLER         {Colors.RESET}")
print(f"{Colors.CYAN}========================================{Colors.RESET}")

Narrator = Game()

# instructions
print(f"\nWelcome to the dungeon, {Colors.CYAN}{Narrator.PC.name}{Colors.RESET}.")
print(f"\n{Colors.YELLOW}HOW TO PLAY:{Colors.RESET}")
print(f" * Navigate the maze using directional string commands ({Colors.GREEN}left, right, straight, back{Colors.RESET}).")
print(f" * Combat uses a {Colors.CYAN}3-action combo system{Colors.RESET} per turn (Max 3 inputs).")
print(f" * [{Colors.RED}a{Colors.RESET}] Attack   - Deals heavy damage (Costs SP)")
print(f" * [{Colors.BLUE}d{Colors.RESET}] Defend   - Builds hyperarmour shield (Costs SP)")
print(f" * [{Colors.GREEN}r{Colors.RESET}] Recharge - Restores stamina / SP")
print(f" * [{Colors.RED}h{Colors.RESET}] Heal     - Recovers HP (Costs SP)")
print(f"\n{Colors.YELLOW}WARNING:{Colors.RESET} Running out of SP leaves you exhausted and unable to act!")
print(f"Find {Colors.GREEN}Bonfires{Colors.RESET} to fully restore your stats and survive the descent.")
input(f"\nPress {Colors.GREEN}Enter{Colors.RESET} to enter the dungeon...")

Narrator.run()