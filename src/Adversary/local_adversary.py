import src.Game.constants as constants
from src.Common.adversary_client import AdversaryClient
from src.Adversary.adversary_strategies import StrategyFactory
from src.Common.occupant_client import respond_to_message

class LocalAdversary(AdversaryClient):
    """
    Represents an adversary in a local game of snarl. Accepts updates from a game manager.
    """
    _trace = []

    def accept_game_state(self, state):
        """
        Accepts a game state update from the game manager.
        """
        self._trace.append(state)
        respond_to_message(state, {
            constants.ADVERSARY_UPDATE_MESSAGE: self.__store_state,
        })

    def __store_state(self, state):
        """
        Stores the adversary state
        """
        self.__level_map = state["level_map"]
        self.__player_locations = state["player_locations"]
        self.__possible_moves = state["available_moves"]
        self.__current_location = state["position"]

    def provide_move(self):
        """
        Returns an adversary move to be played.
        """
        return StrategyFactory.get_strategy(self.strategy_type).calculate_move(
            self.__possible_moves, self.__current_location,
            self.__level_map, self.__player_locations)[::-1]

    def provide_adversary_type(self):
        """
        Returns the type of the adversary
        """
        return self.adversary_type

    def provide_level(self):
        """
        Provides the level of the adversary
        """
        return self.level

