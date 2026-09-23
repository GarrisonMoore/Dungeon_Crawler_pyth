import Characters
import colors
import combat
import dungeon

class Game:
    """Game class represents the orchestrator of the game (God basically)"""
    def __init__(self):
        self.name = " "
        self.dungeon_level = 1
        self.PC = Characters.Player(50,50,0)
        self.current_node = None

    def check_bonfire(self):
        """Check if current room is a bonfire, heal and charge if so"""
        # if current room is a bonfire, rest safely and heal HP and SP
        if self.current_node.is_bonfire:
            print(f"\n{colors.GREEN}You rest safely. HP and SP fully restored.{colors.RESET}")
            self.PC.hp = self.PC.max_hp
            self.PC.sp = self.PC.max_sp

    def check_exit(self):
        """Check if current room is an exit room, return True to break loop in main if so"""
        # check if room is an exit, break loop if it is / increment level and reward player xp
        if self.current_node.is_exit:
            print("\nYou have reached the exit!\n")
            self.dungeon_level += 1
            # reward the player xp for completing the level
            reward_xp = 50 * self.dungeon_level
            self.PC.gain_xp(reward_xp)
            return True
        return False

    def check_mob(self):
        """Check if the current room has a mob, run combat if so"""
        # if current room has a mob, spawn it and run combat
        if self.current_node.mob:
            print(f"\nA {colors.YELLOW}{self.current_node.mob.name}{colors.RESET} has appeared!")
            while self.current_node.mob.hp > 0:

                # Player combat turn
                combat.run_turn(self.PC, self.current_node.mob, True)
                if self.current_node.mob.hp <= 0:
                    self.current_node.mob.hp = 0

                    # reward the player xp,hp and sp for killing the mob
                    reward_xp = 25 * self.dungeon_level
                    reward_hp_sp = 15 * self.dungeon_level
                    # cap the reward at max hp and sp
                    self.PC.hp = min(self.PC.hp + reward_hp_sp, self.PC.max_hp)
                    self.PC.sp = min(self.PC.sp + reward_hp_sp, self.PC.max_sp)

                    print(f"\nYou killed the {colors.YELLOW}{self.current_node.mob.name}{colors.RESET}!")
                    print(
                        f"{colors.CYAN}{self.PC.name}{colors.RESET} gained {colors.GREEN}+{reward_hp_sp}{colors.RESET} HP & SP")
                    # call the gain_xp method to update the player's xp with the reward'
                    self.PC.gain_xp(reward_xp)

                    # remove the mob from the room once defeated and break
                    self.current_node.mob = None
                    break

                # NPC combat turn
                combat.run_turn(self.PC, self.current_node.mob, False)
                if self.PC.hp <= 0:
                    self.PC.hp = 0
                    break


    def run(self):
        """Method to run the main game, uses methods above"""

        # Main game loop
        while True:
            # check if player character is alive before doing anything
            if self.PC.hp <= 0:
                print(
                    f"{colors.CYAN}{self.PC.name}{colors.RESET} has been slain by the {colors.YELLOW}{self.current_node.mob.name}{colors.RESET}!")
                break

            # generate the dungeon and call visualize_map to display it
            start_node = dungeon.generate_dungeon(self.dungeon_level)

            print(f"\n DUNGEON LEVEL {colors.GREEN}{self.dungeon_level}{colors.RESET}.")
            print("\n========== DEBUG: DUNGEON MAP ==========")
            dungeon.visualize_map(start_node)
            print("========================================\n")

            # initialize the map pointer
            self.current_node = start_node

            # game logic loop
            while self.PC.hp > 0:
                # print the current room's name and doors'
                print(f"\n--- {colors.CYAN}{self.current_node.name}{colors.RESET} ---")

                # Build a list of colored strings for the doors (Gemini helped me with this)
                door_display = []
                for direction, destination in self.current_node.paths.items():
                    if destination is not None:
                        # Open path
                        door_display.append(f"{colors.GREEN}{direction}{colors.RESET}")
                    else:
                        # Dead end
                        door_display.append(f"{colors.RED}{direction} (blocked){colors.RESET}")

                # join the list into a single readable string
                print(f"Doors: [{', '.join(door_display)}]")

                # get user input for traversal action (use playercharacter move method)
                # assign current node to the players choice (this is how we traverse the map)
                self.current_node = self.PC.move(self.current_node)

                # check if the room is an exit
                if self.check_exit():
                    # break loop if it is
                    break
                # Check if the room is a bonfire
                self.check_bonfire()
                # if current room has a mob, spawn it and run combat
                self.check_mob()