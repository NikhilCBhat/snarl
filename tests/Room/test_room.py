import json
import sys
sys.path.append('../../')
from src.Game.models.level.level_builder import LevelBuilder
import src.Game.constants as constants
from tests.utils import read_user_input, print_json

class PointOutsideRoomError(Exception):
    """
    Thrown when a point is outside the room.
    """
    pass

def run_test():
    """
    The test `main` method.
    """
    user_input = read_user_input()
    room_origin = user_input[0]["origin"]
    player_location = user_input[1]

    try:
        traversable_tiles = [x[::-1] for x in calculate_traversable_tiles(*user_input)]
        print_json([ "Success: Traversable points from ", player_location, " in room at ", room_origin , " are ", traversable_tiles])
    except PointOutsideRoomError:
        print_json(["Failure: Point ", player_location, " is not in room at ", room_origin])

def get_level_dimensions(room):
    """
    Gets the size of a level based off of the room locations
    """
    bottom_right_corners = [[room["origin"][1] + room["bounds"]["rows"],
                             room["origin"][0] + room["bounds"]["columns"]]]

    num_rows = max(x[0] for x in bottom_right_corners)
    num_columns = max([x[1] for x in bottom_right_corners])

    return num_columns, num_rows

def calculate_traversable_tiles(room_json, player_location):
    """
    Returns traversable tiles in (column, row) format
    raise PointOutsideRoomError if origin is outside room
    """

    # Creates level with this room
    room_json["origin"] = room_json["origin"][::-1]
    player_location = player_location[::-1]
    level = LevelBuilder()\
                        .create_level(*get_level_dimensions(room_json))\
                        .add_room_from_json(room_json).build()

    col, row = player_location
    if not (0 <= col <= level.num_cols) or not (0 <= row <= level.num_rows):
        raise PointOutsideRoomError

    # Checks to see if success/failure
    return level.get_adjacent_tiles(player_location, 1)


## -- Note -- ##
# Below methods are for validating
# the input JSON. They were created
# before we realized that input validation
# was not necessary for this task.

def __validate_input_json(input_json):
    """
    Validate given input json
    """
    return len(input_json) == 2 and __validate_room(input_json[0]) and __validate_point(input_json[1])

def __validate_point(point):
    """
    Validate a provided point JSON
    """
    return len(point) == 2 and all(isinstance(x, int) for x in point)

def __validate_bounds(bounds):
    """
    Validate a provided bounds for a room
    """
    bounds_keys = ["rows", "columns"]
    return isinstance(bounds, dict) and all(key in bounds for key in bounds_keys)

def __validate_room(input):
    """
    Validate a provided room JSON
    """
    room_keys = ["type", "origin", "bounds", "layout"]
    return (all(key in input for key in room_keys) and isinstance(input["type"], str)
    and __validate_point(input["origin"]) and __validate_bounds(input["bounds"])
    and isinstance(input["layout"], list))

if __name__ == "__main__":
    run_test()
