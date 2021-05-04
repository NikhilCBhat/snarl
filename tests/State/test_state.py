import sys
import json

# Local imports
sys.path.append('../../')
from tests.utils import read_user_input, print_json
from src.Game.models.states import GameState
from src.Game.rule_checker import RuleChecker
from src.Game.snarl_errors import InvalidOccupantIdError, NonTraversableTileError
from src.Game.models.occupants import Player, Zombie, Ghost, Occupant
from src.Game.models.level.level import Level
from src.Game.models.level.level_builder import LevelBuilder
from tests.utils import swap_level

def construct_occupant(occupant_json, level: Level) -> Occupant:
    """
    Creates an occupant from the JSON representation.
    Places the occupant on the correct tile in the level.
    """
    occupant_name_to_type = {"player": Player, "zombie": Zombie, "ghost": Ghost}

    occupant_type = occupant_json["type"]
    name = occupant_json["name"]
    position = occupant_json["position"]

    occupant = occupant_name_to_type[occupant_type](name)
    occupant.move(level.get_tile(*position))

    return occupant

def construct_state(json_object, name) -> GameState:
    """
    Creates a GameState object from a JSON representation
    """

    level = LevelBuilder().create_level_from_json(json_object["level"])
    occupant_jsons = json_object["players"] + json_object["adversaries"]
    occupants = [construct_occupant(oj, level) for oj in occupant_jsons]

    state_dict = {
        "current_level": 0,
        "levels": [level],
        "is_game_over": False,
        "is_exit_unlocked": not json_object["exit-locked"],
        "occupant_order": [o.id for o in occupants],
        "current_turn": name,
        "occupants": {o.id: o for o in occupants}
    }

    return GameState.from_state_dict(state_dict)

def run_test():
    """
    'Main' method for the test
    """
    # Creates the intermediate game state based on the user input
    state_json, name, desired_location = read_user_input()
    state_json["level"] = swap_level(state_json["level"])
    state = construct_state(state_json, name)

    # Validates the given move
    try:
        RuleChecker.validate_move(state, name, desired_location[::-1])

    except InvalidOccupantIdError:
        print_json(["Failure", "Player ", name, " is not a part of the game."])
        return

    except NonTraversableTileError:
        print_json(["Failure", "The destination position ", desired_location, " is invalid."])
        return

    except:
        # Note:
        # Ignoring other exceptions (particularly InvalidDestinationError)
        # Because the assignment states:
        # > We are not checking rules, so the position
        # > can be arbitrarily removed from the original position
        pass

    # Update the state
    state.update(name, desired_location[::-1])

    # Print the output
    if not state.occupants[name].is_alive:
        print_json(["Success", "Player ", name, " was ejected.", state.to_json()])

    elif state.occupants[name].has_exited:
        print_json(["Success", "Player ", name, " exited.", state.to_json()])

    else:
        print_json(["Success", state.to_json()])

if __name__ == "__main__":
    run_test()

