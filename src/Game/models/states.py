import random
from copy import deepcopy
from typing import List
from collections import defaultdict

from src.Game.models.level.level import Level
from src.Game.models.occupants import Player, Adversary, Occupant
import src.Game.constants as constants
from src.Game.rule_checker import RuleChecker

class GameState:

    def __init__(self, levels=[], players=[], adversaries=defaultdict(list)):
        """
        Creates a game state.
        A user can either provide a number of players & adversaries,
        or provide a list of Player/Adversary objects.

        Note: We are not doing validity checking on the constructor
        as we assume that is taken care of by the RuleChecker
        """

        # Create occupants
        self.occupants = {occupant.id:occupant for occupant in players+adversaries.get(0, [])}
        self.occupant_order = [o.id for o in players+adversaries.get(0, [])]
        self._all_adversaries = adversaries

        # Create other fields
        self.levels = levels
        self.current_level = -1
        self.current_turn = self.occupant_order[0] if self.occupant_order else None
        self.moves_elapsed = 0
        self.turns_elapsed = 0
        self.is_exit_unlocked = False
        self.is_game_over = False
        self.player_message = ""

    @classmethod
    def from_state_dict(cls, state_dictionary):
        """
        Instantiates a GameState object from a state_dictionary.
        """
        new_game_state = cls()
        new_game_state._all_adversaries = state_dictionary["_all_adversaries"]
        new_game_state.occupants = state_dictionary["occupants"]
        new_game_state.occupant_order = state_dictionary["occupant_order"]
        new_game_state.levels = state_dictionary["levels"]
        new_game_state.current_level = state_dictionary["current_level"]
        new_game_state.current_turn = state_dictionary["current_turn"]
        new_game_state.is_exit_unlocked = state_dictionary["is_exit_unlocked"]
        new_game_state.is_game_over = state_dictionary["is_game_over"]
        new_game_state.turns_elapsed = state_dictionary.get("turns_elapsed", 0)
        new_game_state.turns_elapsed = state_dictionary.get("moves_elapsed", 0)
        new_game_state.player_message = ""

        return new_game_state

    def to_dict(self):
        """
        Creates a state dictionary in order to load it in later.
        """
        return deepcopy(vars(self))

    def to_json(self):
        """
        Constructs json representation of state.
        """
        return {
            "type": "state",
            "level": self.current_level_object.to_json(as_json=False),
            "players": [p.to_json() for p in self.players if p.is_alive and not p.has_exited],
            "adversaries": [a.to_json() for a in self.adversaries],
            "exit-locked": not self.is_exit_unlocked
        }

    @property
    def current_level_object(self) -> Level:
        return self.levels[self.current_level]

    @property
    def current_occupant(self) -> Occupant:
        return self.occupants[self.current_turn]

    @property
    def num_rows(self):
        return self.current_level_object.num_rows

    @property
    def num_cols(self):
        return self.current_level_object.num_cols

    @property
    def players(self) -> List[Player]:
        return [o for o in self.occupants.values() if str(o) == constants.PLAYER_STRING]

    @property
    def adversaries(self) -> List[Adversary]:
        return [o for o in self.occupants.values() if str(o) != constants.PLAYER_STRING]

    def __update_player_level_id(self):
        """
        Updates all players with current level id.
        """
        for p in self.players:
            p.level_id = self.current_level

    def progress_to_next_level(self, place_randomly=True):
        """
        Starts the level.
        Currently makes all players alive and places them at the level start.
        In the future this could have more functionality.
        """
        # Increments the current level
        self.current_level += 1
        self.is_exit_unlocked = False
        self.occupants = {o.id: o for o in self.players +
                          self._all_adversaries.get(self.current_level, [])}
        self.occupant_order = list(self.occupants.keys())
        self.current_turn = self.players[0].id
        self.__update_player_level_id()

        # Places occupants at the level start
        if place_randomly:
            self.__place_occupants_randomly()
        else:
            self.__place_occupants_tl_br()

        # Brings everyone back to life, sets has_exited to False.
        for occupant in self.occupants.values():
            occupant.reset_health()
            if str(occupant) == constants.PLAYER_STRING:
                occupant.has_exited = False

    def __place_occupants_randomly(self):
        """
        Places occupants in the level
        """
        for occupant in self.occupants.values():
            self.__place_occupant_randomly(occupant)

    def __place_occupant_randomly(self, occupant):
        """
        Places an occupants randomly
        """
        placed_occupant = False
        while not placed_occupant:
            occupant_room = random.choice(
                list(self.current_level_object.room_origins_to_room.values()))
            placed_occupant = occupant_room.place_occupant(occupant)

    def __place_occupants_tl_br(self):
        """
        Places players in the top left-most room of the level,
        Places adversaries in the bottom right-most room of the level
        Note: No longer used.
        """
        identifier_to_room = {}

        for identifier in [constants.PLAYER_STRING, constants.ADVERSARY_STRING]:
            occupant_start = (0,0) if identifier == constants.PLAYER_STRING else (self.num_rows - 1, self.num_cols - 1)
            identifier_to_room[identifier] = self.current_level_object.find_available_room(occupant_start)

        for occupant in self.occupants.values():
            identifier = constants.PLAYER_STRING if str(occupant) == constants.PLAYER_STRING else constants.ADVERSARY_STRING
            identifier_to_room[identifier].place_occupant(occupant)

    def __increment_turn(self):
        """
        Increment self.current_turn
        """
        next_turn_id = self.occupant_order.index(self.current_turn) + 1
        self.current_turn = self.occupant_order[next_turn_id%len(self.occupant_order)]
        if next_turn_id == len(self.occupant_order):
            self.turns_elapsed += 1
        if not self.current_occupant.is_active and any(o.is_active for o in self.players):
            self.__increment_turn()
        self.moves_elapsed += 1

    def __store_player_message(self, player, result):
        """
        Stores the message to present to the player.
        """
        result_type_to_message = {
            constants.UNLOCKED_RESULT: "found the key",
            constants.EXITED_RESULT: "exited",
            constants.EJECTED_RESULT: "was expelled"
        }

        if result in result_type_to_message:
            self.player_message = "On move: {}, player {} {}".format(self.moves_elapsed, player.id, result_type_to_message[result])

    def update(self, occupant_id, new_location):
        """
        0 - Precondition: Assume the move is validated by RuleChecker
        1 - Get the tile the occupant moves to
        2 - Move the occupant to the new tile
        2.5 - Ocupant/Ocupant and Ocupant/Item interactions are handled in the move() function
        3. Evaluate the updated game state for level over
        """

        occupant = self.occupants[occupant_id]

        # Move a player to the tile
        # This handles changes to a player
        if not occupant.has_exited:
            tile = self.current_level_object.get_tile(*new_location, False)

            if occupant.actor_type == constants.GHOST_ACTOR_TYPE and tile.is_wall:
                self.__place_occupant_randomly(occupant)
            else:
                occupant.move(tile)

        # This handles changes to the game state
        result = self.__evaluate_game_state(occupant_id)

        # Update the turn
        self.__increment_turn()

        return result

    def __end_game(self):
        """
        Indicates that the game is over.
        """
        self.is_game_over = True

    def __end_level(self):
        """
        Ends the current level and progresses forward.
        """
        self.progress_to_next_level()

    def __evaluate_game_state(self, occupant_id):
        """
        Determines if the game or level is over
        If so, update the state the reflect that.
        """
        result = constants.OK_RESULT
        occupant = self.occupants[occupant_id]

        if not occupant.is_alive:
            result = constants.EJECTED_RESULT
        elif occupant.actor_type == constants.PLAYER_ACTOR_TYPE:
            player_location = occupant.current_location

            # unlocks exit if the player found the key
            if player_location in self.current_level_object.items[constants.KEY_NAME]:
                self.is_exit_unlocked = True
                self.current_level_object.remove_item(constants.KEY_NAME, player_location)
                result = constants.UNLOCKED_RESULT
                occupant.keys_found.add(self.current_level)

            # exits the level if they arrived at an unlocked exit
            elif player_location in self.current_level_object.items[constants.EXIT_NAME] and self.is_exit_unlocked:
                occupant.has_exited = True
                occupant.current_tile.current_occupant = None
                result = constants.EXITED_RESULT
                occupant.exits.add(self.current_level)

        # End Game
        if RuleChecker.is_game_over(self):
            self.__end_game()

        # End level
        elif RuleChecker.is_level_over(self):
            self.__end_level()

        self.__store_player_message(occupant, result)

        return result

