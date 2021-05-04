from src.Common.user import User
from src.Remote.remote_occupant import RemoteOccupant
import src.Game.constants as constants

class RemotePlayer(User, RemoteOccupant):
    """
    A user/player in a networked game of snarl.
    """

    def provide_name(self):
        """
        Forwards a user specified name to the server.
        """
        self._network_handler.send(constants.NAME_MESSAGE)

        return self._network_handler.receive_until(
            condition = lambda data: isinstance(data, str))