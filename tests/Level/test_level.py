import sys
import json

# Local imports
sys.path.append('../../')
from src.Game.models.level.level import Level
from src.Game.models.level.level_builder import LevelBuilder
import src.Game.constants as constants
from tests.utils import read_user_input, print_json, swap_level

def generate_output(tile):
    """
    Creates the output containing information about the tile.
    """
    non_traversable_tiles = {constants.WALL_STRING, constants.VOID_STRING}
    item_string_to_item_name = {constants.KEY_STRING : "key", constants.EXIT_STRING: "exit"}

    return {
        "traversable": str(tile) not in non_traversable_tiles,
        "object": item_string_to_item_name.get(str(tile.current_item)),
        "type": str(tile.parent) if tile.parent else "void",
        "reachable": [x[::-1] for x in tile.get_adjacent_rooms()]
    }

def run_test():
    """
    'Main' method for the test
    """
    # Gets the tile in the level based on the user input
    level_json, point = read_user_input()
    level = LevelBuilder().create_level_from_json(swap_level(level_json))
    tile = level.get_tile(*point)

    # Gets & prints the output
    output = generate_output(tile)
    print_json(output)

if __name__ == "__main__":
    run_test()
