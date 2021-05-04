from abc import abstractmethod
import src.Game.constants as constants
from src.Common.occupant_client import OccupantClient

class AdversaryClient(OccupantClient):
    """
    An adversary client in a game of snarl.
    """
    actor_type = constants.ADVERSARY_STRING

    def __init__(self, adversary_type=constants.ZOMBIE_ACTOR_TYPE, level=0, strategy_type=None):
        self.name = None
        self.adversary_type = adversary_type
        self.level = level
        self.strategy_type = strategy_type or adversary_type

    @abstractmethod
    def provide_adversary_type(self):
        """
        Returns the type of the adversary
        """
        pass

    @abstractmethod
    def provide_level(self):
        """
        Provides the level of the adversary
        """
        pass
