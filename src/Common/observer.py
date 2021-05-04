from abc import abstractmethod

class Observer:
    """
    A formal interface for an observer in a game of Snarl.

    An Observer receives updates from the GameManager.
    These updates will be rendered via a view.
    """

    @abstractmethod
    def accept_game_state(self, state):
        """
        Accepts a game state from the game manager.
        """
        pass
