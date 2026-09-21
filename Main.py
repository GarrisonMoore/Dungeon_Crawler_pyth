import colors
import dungeon
import combat
import Characters

# initialize dungeon level at 1
current_level = 1

# intro
print(f"\n{colors.CYAN}========================================{colors.RESET}")
print(f"{colors.GREEN}       TERMINAL DUNGEON CRAWLER         {colors.RESET}")
print(f"{colors.CYAN}========================================{colors.RESET}")

# initialize player character
PC = Characters.Player(50, 50, 0)

# instructions
print(f"\nWelcome to the dungeon, {colors.CYAN}{PC.name}{colors.RESET}.")
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

# Main game loop
while True:
    # check if player character is alive before doing anything
    if PC.hp <= 0:
        print(f"{colors.CYAN}{PC.name}{colors.RESET} has been slain by the {colors.YELLOW}{current_node.mob.name}{colors.RESET}!")
        break

    # generate the dungeon and call visualize_map to display it
    start_node = dungeon.generate_dungeon(current_level)
    print(f"\n DUNGEON LEVEL {colors.GREEN}{current_level}{colors.RESET}.")
    print("\n========== DEBUG: DUNGEON MAP ==========")
    dungeon.visualize_map(start_node)
    print("========================================\n")

    # initialize the map pointer
    current_node = start_node

    # game logic loop
    while PC.hp > 0:
        # print the current room's name and doors'
        print(f"\n--- {colors.CYAN}{current_node.name}{colors.RESET} ---")

        # Build a list of colored strings for the doors (Gemini helped me with this)
        door_display = []
        for direction, destination in current_node.paths.items():
            if destination is not None:
                # Open path
                door_display.append(f"{colors.GREEN}{direction}{colors.RESET}")
            else:
                # Dead end
                door_display.append(f"{colors.RED}{direction} (blocked){colors.RESET}")

        # join the list into a single readable string
        print(f"Doors: [{', '.join(door_display)}]")
        # get user input for traversal action
        action = input("Where to? ")

        # if the action is a valid door, move to the next room
        if action in current_node.paths and current_node.paths[action] is not None:
            current_node = current_node.paths[action]
        else:
            print("You can't go that way!")
            continue

        # check if room is an exit, break loop if it is / increment level and reward player xp
        if current_node.is_exit:
            print("\nYou have reached the exit!\n")
            current_level += 1
            # reward the player xp for completing the level
            reward_xp = 50 * current_level
            PC.gain_xp(reward_xp)
            break

        # if current room is a bonfire, rest safely and heal HP and SP
        if current_node.is_bonfire:
            print(f"\n{colors.GREEN}You rest safely. HP and SP fully restored.{colors.RESET}")
            PC.hp = PC.max_hp
            PC.sp = PC.max_sp
            continue

        # if current room has a mob, spawn it and run combat
        if current_node.mob:
            print (f"\nA {colors.YELLOW}{current_node.mob.name}{colors.RESET} has appeared!")
            while current_node.mob.hp > 0:

                # Player combat turn
                combat.run_turn(PC,current_node.mob,True)
                if current_node.mob.hp <= 0:
                    current_node.mob.hp = 0

                    # reward the player xp,hp and sp for killing the mob
                    reward_xp = 25 * current_level
                    reward_hp_sp = 15 * current_level
                    # cap the reward at max hp and sp
                    PC.hp = min(PC.hp + reward_hp_sp , PC.max_hp)
                    PC.sp = min(PC.sp + reward_hp_sp , PC.max_sp)

                    print(f"\nYou killed the {colors.YELLOW}{current_node.mob.name}{colors.RESET}!")
                    print(f"{colors.CYAN}{PC.name}{colors.RESET} gained {colors.GREEN}+{reward_hp_sp}{colors.RESET} HP & SP")
                    # call the gain_xp method to update the player's xp with the reward'
                    PC.gain_xp(reward_xp)

                    # remove the mob from the room once defeated and break
                    current_node.mob = None
                    break

                # NPC combat turn
                combat.run_turn(PC, current_node.mob, False)
                if PC.hp <= 0:
                    PC.hp = 0
                    break