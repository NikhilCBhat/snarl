from src.Common.occupant_client import OccupantClient
from src.Remote.network_handler import NetworkHandler
import src.Game.constants as constants

class RemoteOccupant(OccupantClient):
    """
    A remote occupant in a networked game of snarl.
    """

    def __init__(self, sock):
        self._network_handler = NetworkHandler(sock)

    def accept_game_state(self, state):
        """
        Accepts a game state update.
        """
        self._network_handler.send(state)

    def provide_move(self):
        """
        Forwards a user specified move to the server.
        """
        self._network_handler.send(constants.MOVE_MESSAGE)
        response = self._network_handler.receive_until(
            condition = lambda data: isinstance(data, dict) and "to" in data)

        move = response["to"]
        return move[::-1] if move is not None else move