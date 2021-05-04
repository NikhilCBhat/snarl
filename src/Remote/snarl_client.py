from src.Player.local_player import LocalPlayer
from src.Adversary.local_adversary import LocalAdversary
from src.Remote.network_handler import NetworkHandler
import src.Game.constants as constants
from src.Common.occupant_client import OccupantClient

class SnarlClient:
    """
    A user client in a networked game of snarl.
    Interacts with the SnarlServer for updates.
    """

    _occupant : OccupantClient


    def __init__(self, host, port, message_to_function):
        self.__network_handler = NetworkHandler(host=host, port=port)
        self.__message_to_function = {**{
            constants.MOVE_MESSAGE: self._create_move_message
        }, **message_to_function}

    def _create_move_message(self):
        """
        Generates a move message to send to the server.
        """
        return {
            "type": constants.MOVE_MESSAGE,
            "to": self._occupant.provide_move()[::-1]
        }

    def launch(self):
        """
        Initiates game play for this user client.
        Reads incoming messages from the networked server.
        Writes/sends user-specified messages to the networked server.
        Removes this client from game at game over.
        """
        print(constants.CLEAR_SCREEN)
        while True:
            data = self.__network_handler.receive()
            if data:
                if isinstance(data, dict):
                    self._occupant.accept_game_state(data)
                    if data["type"] == constants.END_GAME_MESSAGE:
                        self.__network_handler.close()

                elif isinstance(data, str):
                    if data in self.__message_to_function:
                        self.__network_handler.send(self.__message_to_function[data]())
                    else:
                        print("Received message: ", data)

class SnarlPlayerClient(SnarlClient):

    def __init__(self, host, port):
        self._occupant = LocalPlayer()
        super().__init__(host, port, {
            constants.NAME_MESSAGE: self._occupant.provide_name
        })

class SnarlAdversaryClient(SnarlClient):

    def __init__(self, host, port, adversary_type, level):
        self._occupant = LocalAdversary(adversary_type, level)
        super().__init__(host, port, {
            constants.ADVERSARY_TYPE_MESSAGE: self._occupant.provide_adversary_type,
            constants.ADVERSARY_LEVEL_MESSAGE: self._occupant.provide_level
        })