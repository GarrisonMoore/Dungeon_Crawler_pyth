from random import randint
import Colors

inputs = ["a", "d", "r", "h"]

class CombatManager:

    @staticmethod
    def show_stats(player,enemy):
        """Displays current combat stats for both entities"""
        print(f"\n---- STATS ----")
        print(f"{Colors.YELLOW}{enemy.name}{Colors.RESET} -> HP: {Colors.RED}{enemy.hp}{Colors.RESET} | SP: {Colors.GREEN}{enemy.sp}{Colors.RESET}")
        print(f"{Colors.CYAN}{player.name}{Colors.RESET} -> HP: {Colors.RED}{player.hp}{Colors.RESET} | SP: {Colors.GREEN}{player.sp}{Colors.RESET}")
        print(f"---------------------")

    @staticmethod
    def player_input():
        """Helper method to get player input

        * 3 inputs max per turn. Can do any combination of (a/d/r/h)"""
        inputs = input("What do you want to do? (a/d/r/h) [Max 3 actions]").lower()

        # slice the string to limit player input to 3 actions
        inputs = inputs[:3]

        print(f"\nDEBUG_INPUTS : {inputs}")
        return inputs

    @staticmethod
    def npc_input(enemy):
        """Helper method to get npc input"""
        npc_inputs = ""

        # get enemy sp
        current_sp = enemy.sp

        # loop handles npc's actions based on their current SP
        for i in range(3):
            fifty_fifty_chance = randint(0, 1)
            one_third_chance = randint(0, 2)
            # if npc is low on sp, use r to recharge
            if current_sp < 5:
                npc_inputs += "r"
                current_sp += 10
            # if npc is low on hp, use h to heal
            elif enemy.hp < (enemy.max_hp * 0.3) and current_sp >= 10:
                if one_third_chance == 0:
                    npc_inputs += "h"
                    current_sp -= 10
                else:
                    npc_inputs += "a"
                    current_sp -= 5
            # else npc attacks or blocks. (50/50) chance
            else:
                if fifty_fifty_chance == 0:
                    npc_inputs += "a"
                    current_sp -= 5
                else:
                    npc_inputs += "d"
                    current_sp -= 5

        print(f"\nDEBUG_INPUTS : {npc_inputs}")
        return npc_inputs

    @staticmethod
    def resolve_turn(name, inputs, is_player, current_sp,player_level):
        """Method to resolve a turn based on any of the inputs. Used for PC and NPC's."""
        # a = attack
        # d = defend
        # r = recharge sp
        # h = heal
        hp_change = 0
        sp_change = 0
        dmg_in = 0
        dmg_out = 0

        # assign color to name based on who's turn it is
        if is_player:
            name = Colors.CYAN + name + Colors.RESET
        else:
            name = Colors.YELLOW + name + Colors.RESET



        # if elif block handles all possible inputs
        for action in inputs:

            # check if the player has enough SP to use the action
            active_sp = current_sp + sp_change

            # if player is attacking, scale combat output based on level
            if is_player:
                base_min = 2 + int(player_level * 1.5)
                base_max = 5 + player_level * 2
            else:
                # scale npc damage at a lower rate
                base_min = 2 + int(player_level * 1.5)
                base_max = 5 + player_level * 2

            # This giant if / else block determines what action to take based on input
            # attack action
            if action == "a":
                # attack cost 1 action and sp equivalent to damage dealt
                dmg_random = randint(base_min,base_max)

                if active_sp >= dmg_random:
                    dmg_out += dmg_random
                    sp_change -= dmg_random
                    print(f"{name} dealt {Colors.RED}{dmg_random}{Colors.RESET} damage! (-{dmg_random} SP)")
                else:
                    print(f"{name} is too exhausted to attack!")

            # defend action
            elif action == "d":
                # costs 1 action and sp equivalent to damage reduction
                dmg_reduction = randint(base_min,base_max) // 2

                if active_sp >= dmg_reduction:
                    dmg_in += dmg_reduction
                    sp_change -= dmg_reduction
                    print(f"{name} reduced incoming damage by {Colors.BLUE}{dmg_reduction}{Colors.RESET}! (-{dmg_reduction} SP)")
                else:
                    print(f"{name} is too exhausted to defend!")

            # recharge SP action
            elif action == "r":
                # costs 1 action, free otherwise.
                sp_random = randint(base_min,base_max)
                sp_change += sp_random
                print(f"{name} recharged SP by {Colors.GREEN}{sp_random}{Colors.RESET}! (+{sp_random} SP)")

            # heal action
            elif action == "h":
                # heal costs 1 action and 1.25x SP
                hp_random = randint(base_min, base_max)

                if active_sp >= hp_random*2:
                    hp_change += hp_random
                    sp_change -= hp_random*2
                    print(f"{name} healed for {Colors.RED}{hp_random}{Colors.RESET} HP! (-{hp_random*2} SP)")
                else:
                    print(f"{name} is too exhausted to heal!")
            else:
                print(f"Invalid input '{action}'. Turn passed.")

        return hp_change, sp_change, dmg_in, dmg_out

    def run_turn(self, player,current_enemy,is_player):
        """Main method to run a combat turn. Handles both PC and NPC's"""
        # show stats before turn
        self.show_stats(player,current_enemy)

        # if player turn, resolve turn based on player input
        if is_player:
            name = player.name
            choice = self.player_input()
            hp_change, sp_change, dmg_in, dmg_out = self.resolve_turn(name, choice, True, player.sp,player.level)

            # calculate actual damage dealt based on hyperarmour
            actual_damage = max(0, dmg_out - current_enemy.hyperarmour)
            current_enemy.hp -= actual_damage
            player.hyperarmour = dmg_in

            # calculate final HP and SP change after turn
            player.hp = min(player.hp + hp_change, player.max_hp)
            player.sp = min(player.sp + sp_change, player.max_sp)

        # calculate NPC combat turn
        else:
            name = current_enemy.name
            choice = self.npc_input(current_enemy)
            hp_change, sp_change, dmg_in, dmg_out = self.resolve_turn(name, choice, False, current_enemy.sp,player.level)

            # calculate actual damage dealt based on hyperarmour
            actual_damage = max(0, dmg_out - player.hyperarmour)
            player.hp -= actual_damage
            current_enemy.hyperarmour = dmg_in

            # calculate final HP and SP change after turn
            current_enemy.hp = min(current_enemy.hp + hp_change, current_enemy.max_hp)
            current_enemy.sp = min(current_enemy.sp + sp_change, current_enemy.max_sp)

        # keep HP from going below 0
        if current_enemy.hp < 0:
            current_enemy.hp = 0
        if player.hp < 0:
            player.hp = 0