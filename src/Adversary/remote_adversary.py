from src.Common.adversary_client import AdversaryClient
from src.Remote.remote_occupant import RemoteOccupant
import src.Game.constants as constants

class RemoteAdversary(RemoteOccupant, AdversaryClient):
    """
    Represents an adversary in a local game of snarl. Accepts updates from a game manager.
    """

    __allowed_adversary_types = {constants.GHOST_ACTOR_TYPE, constants.ZOMBIE_ACTOR_TYPE}

    def provide_adversary_type(self):
        """
        Provides type of the adversary
        """
        self._network_handler.send(constants.ADVERSARY_TYPE_MESSAGE)

        self.adversary_type = self._network_handler.receive_until(
            lambda data: isinstance(data, str) \
            and data in self.__allowed_adversary_types)

        return self.adversary_type

    def provide_level(self):
        """
        Provides type of the adversary
        """
        self._network_handler.send(constants.ADVERSARY_LEVEL_MESSAGE)
        return self._network_handler.receive_until(lambda data: isinstance(data, int))