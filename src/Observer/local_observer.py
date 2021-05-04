from src.Game.views.colorful_textual_view import ColorfulTextualView
from src.Common.observer import Observer

class LocalObserver(Observer):
    """
    An observer in a local game of snarl. Accepts updates from a local game manager.
    """
    __view = ColorfulTextualView()

    def accept_game_state(self, state, wait_for_confirmation=False):
        """
        Accepts game state update from server and renders the update.
        """
        self.__view.render_observer_state(state)
        if wait_for_confirmation:
            input("Press enter to continue")
