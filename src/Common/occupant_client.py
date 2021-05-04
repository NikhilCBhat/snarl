from abc import ABC, abstractmethod

class OccupantClient(ABC):
    """
    A formal interface for an occupant in a game of Snarl.

    An OccupantClient receives updates from the game manager
    and passes along moves specified by a user/player.
    """
    actor_type : str

    @abstractmethod
    def accept_game_state(self, state):
        """
        Accept a game state update for this occupant.
        """
        pass

    @abstractmethod
    def provide_move(self):
        """
        Returns the move/destination that a user has specified.
        """
        pass


def respond_to_message(message, message_type_to_action):
    """
    Performs an action based on the message type.
    """
    message_type = message.get("type") if isinstance(message, dict) else ""
    if message_type in message_type_to_action:
        message_type_to_action[message_type](message)
    else:
        print("Received message: ", message)