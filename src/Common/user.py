import src.Game.constants as constants
from src.Common.occupant_client import OccupantClient

class User(OccupantClient):
    """
    A user/player client in a game of snarl.
    """
    actor_type = constants.PLAYER_STRING

    def provide_name(self):
        """
        Prompts a user/player to provide their name.
        """
        pass