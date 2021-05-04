from src.Common.user import User
from src.Common.occupant_client import respond_to_message

class MockPlayer(User):
    """
    A mock player for testing purposes.
    """

    def __init__(self, name, moves_list):
        self.name = name
        self.moves = moves_list
        self.trace = []

    def accept_game_state(self, state):
        """
        Accepts a game state update from the game server/manager.
        """
        self.trace.append(state)
        respond_to_message(state, {})

    def provide_move(self):
        """
        Returns the top of the moves stack
        """
        move = self.moves.pop()
        self.trace.append(move)
        return move

    def provide_name(self):
        """
        Returns the given name
        """
        self.trace.append(self.name)
        return self.name
