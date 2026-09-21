from random import choice
from random import randint
import Characters
import colors
from Characters import call_mob, Player
from combat import run_turn

# A pool of room names
room_list = ["Sewer", "Grotto", "Cave", "Sludge pit", "Bonfire", "Corridor","Crypt",
             "Abyss","Tomb","Catacomb","Gutter"]

class Room():
    """A room is a node in the map"""
    def __init__(self,name, current_level):
        self.name = name
        # paths are edges
        self.paths = {"left": None, "right": None, "straight": None, "back": None}

        # is_exit is a boolean that determines if the room is an exit
        self.is_exit = False

        # debug flag to determine if the room is a trunk
        self.is_trunk = False

        # Flag to determine if the room is a Bonfire
        self.is_bonfire = (self.name == "Bonfire")

        # Dont spawn mobs in bonfire or exit rooms (safe rooms)
        if self.is_bonfire or self.is_exit:
            self.mob = None
        else:
            # 50% chance of a mob spawning in each room
            self.mob = call_mob(current_level) if randint(0,1) == 1 else None

    def __repr__(self):
        """format room info in the terminal"""
        return self.name

def generate_dungeon(current_level):
    """Procedurally generates a dungeon based on the current level.

    Uses a 'tree' structure:
        * The trunk is the path from the entrance to the exit
        * The branches are decoy rooms that connect to the trunk"""

    # Math to scale the dungeon size based on the current level
    trunk_length = current_level * 2

    # create a safe starting room
    start_room = Room("Entrance", current_level)
    start_room.mob = None
    # Flag start room as a trunk
    start_room.is_trunk = True

    # create lists for the trunk and branches of the dungeon
    # trunk will be the path from start to exit
    trunk = [start_room]
    # branches will be decoy rooms that connect to the trunk
    branches = []

    # pointer to keep track of the current room
    current_room = start_room

    # list of possible forward doors
    forward_doors = ["left", "right", "straight"]

    # loop to generate the trunk
    for i in range(trunk_length):
        # create a new random room
        new_room = Room(choice(room_list), current_level)
        # Flag new room as a trunk
        new_room.is_trunk = True

        # choose a random door to connect to the new room
        path_out = choice(forward_doors)

        # connect the new room to the current room
        current_room.paths[path_out] = new_room
        # connect the new rooms back door to the current room
        new_room.paths["back"] = current_room

        # add the new room to the trunk
        trunk.append(new_room)

        # update the current room pointer
        current_room = new_room

    # Mark the last room in the trunk as the exit
    current_room.name = "Exit"
    current_room.is_exit = True

    # loop to generate the branches
    for room in trunk:
        if room.is_exit:
            # don't attach decoy rooms to the exit room
            continue

        # choose a random door to connect to a decoy room
        for direction in forward_doors:
            # if the door is empty, 50% chance of a room spawning
            if room.paths[direction] is None and randint(0,1) == 1:
                # create a new random room and connect it to the current room
                decoy_room = Room(choice(room_list), current_level)
                # give the decoy room forward doors
                room.paths[direction] = decoy_room
                # give the decoy room a return door
                decoy_room.paths["back"] = room
                # add the decoy room to the list of branches
                branches.append(decoy_room)
    return start_room

def visualize_map(room, indent=""):
    """DEBUG METHOD: Visualizes the dungeon map

    * GEMINI WROTE THIS METHOD. I needed something to help visualize the data structure."""

    # if the room is on the main path, wrap its name in the green color code
    display_name = f"{colors.GREEN}{room.name}{colors.RESET}" if room.is_trunk else room.name

    # print the rooms mob or safe status
    mob_status = f"[Enemy: {room.mob.name}]" if room.mob else "[Safe]"
    print(f"{indent}■ {display_name} {mob_status}")

    # get a list of forward doors
    forward_doors = {
        direction: target for direction, target in room.paths.items()
        if target is not None and direction != "back"
    }

    # display the forward doors with arrows
    for direction, next_room in forward_doors.items():
        print(f"{indent}    └──({direction})──>")
        visualize_map(next_room, indent + "        ")