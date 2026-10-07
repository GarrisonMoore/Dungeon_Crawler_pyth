import sys

import Characters
import CombatManager
import Dungeon
import Tools

class Orchestrator:
    """
    Game class represents the orchestrator of the game (God basically)
    """

    def __init__(self):
        self.name = " "
        self.dungeon_level = 1
        self.PC = Characters.Player(50, 50, 0)
        self.current_node = None

        self.combat_manager = CombatManager.CombatManager()

    def check_bonfire(self):
        """
        Check if current room is a bonfire, heal and charge if so
        """

        # if current room is a bonfire, rest safely and heal HP and SP
        if self.current_node.is_bonfire:
            print(f"\n{Tools.GREEN}You rest safely. HP and SP fully restored.{Tools.RESET}")
            self.PC.full_restore()

    def check_exit(self):
        """
        Check if current room is an exit room, return True to break loop in main if so
        """

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
        """
        Check if the current room has a mob, run combat if so
        """

        # if current room has a mob, spawn it and run combat
        if self.current_node.mob:
            print(f"\nA {Tools.YELLOW}{self.current_node.mob.name}{Tools.RESET} has appeared!")
            while self.current_node.mob.hp > 0:

                # Player combat turn
                self.combat_manager.run_turn(self.PC, self.current_node.mob, True)
                if self.current_node.mob.hp <= 0:

                    # reward the player xp,hp and sp for killing the mob
                    reward_xp = 25 * self.dungeon_level
                    reward_hp_sp = 10 * self.dungeon_level

                    self.PC.update_HP(reward_hp_sp)
                    self.PC.update_SP(reward_hp_sp)

                    Tools.clear_terminal()

                    print(f"\nYou killed the {Tools.YELLOW}{self.current_node.mob.name}{Tools.RESET}!")
                    print(
                        f"{Tools.CYAN}{self.PC.name}{Tools.RESET} gained {Tools.GREEN}+{reward_hp_sp}{Tools.RESET} HP & SP")
                    # call the gain_xp method to update the player's xp with the reward'
                    self.PC.gain_xp(reward_xp)

                    # remove the mob from the room once defeated and break
                    self.current_node.mob = None
                    break

                # NPC combat turn
                self.combat_manager.run_turn(self.PC, self.current_node.mob, False)
                if self.PC.hp <= 0:
                    break

    def run(self):
        """
        Method to run the main game, uses methods above
        """

        # Main game loop
        while True:
            # check if player character is alive before doing anything
            if self.PC.hp <= 0:

                # Print death screen
                Tools.clear_terminal()
                print(f"{Tools.CYAN}{self.PC.name}{Tools.RESET} has been slain by the {Tools.YELLOW}{self.current_node.mob.name}{Tools.RESET}!")

                # Print stats
                print(f"{Tools.CYAN}{self.PC.name}{Tools.RESET} made it to: "
                      f"\nDungeon Level {Tools.GREEN}{self.dungeon_level}{Tools.RESET}"
                      f"\nPlayer Level {Tools.GREEN}{self.PC.level}{Tools.RESET}")

                # Input validation loop, ask to play again
                while True:
                    play_again = input("\nPlay again? (y/n) : ")

                    if play_again.lower() == "n":
                        sys.exit()
                    elif play_again.lower() == "y":
                        self.__init__()
                        break
                    else:
                        print("Huh?")

            # generate the dungeon and call visualize_map to display it
            start_node = Dungeon.generate_dungeon(self.dungeon_level)

            print(f"\n DUNGEON LEVEL {Tools.GREEN}{self.dungeon_level}{Tools.RESET}.")
            print("\n========== DEBUG: DUNGEON MAP ==========")
            Dungeon.visualize_map(start_node)
            print("========================================\n")

            # initialize the map pointer
            self.current_node = start_node

            # game logic loop
            while self.PC.hp > 0:
                # print the current room's name and doors'
                print(f"\n--- {Tools.MAGENTA}{self.current_node.name}{Tools.RESET} ---")

                # Build a list of colored strings for the doors (Gemini helped me with this)
                door_display = []
                for direction, destination in self.current_node.paths.items():
                    if destination is not None:
                        # Open path
                        door_display.append(f"{Tools.GREEN}{direction}{Tools.RESET}")
                    else:
                        # Dead end
                        door_display.append(f"{Tools.RED}{direction} (blocked){Tools.RESET}")

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