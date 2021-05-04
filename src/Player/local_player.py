import sys

from src.Game.snarl_errors import MissingUserInputError
from src.Common.user import User
from src.Game.views.colorful_textual_view import ColorfulTextualView
import src.Game.constants as constants
from src.Common.occupant_client import respond_to_message

class LocalPlayer(User):
    """
    Represents a player/user in a local game of snarl. Accepts updates from a game manager.
    """
    __view = ColorfulTextualView()

    def accept_game_state(self, state):
        """
        Accepts a game state update from the game server/manager.
        """
        respond_to_message(state, {
            constants.UPDATE_MESSAGE: self.__player_update_response,
            constants.END_GAME_MESSAGE: self.__view.render_game_over,
            constants.END_LEVEL_MESSAGE: self.__view.render_level_over,
            constants.START_LEVEL_MESSAGE: lambda message: print("Starting level {} with {}".\
                            format(message.get("level"), message.get("players"))),
            constants.WELCOME_MESSAGE: lambda message: print("Welcome Message\n" + message.get("info"))
        })

    def __player_update_response(self, player_update):
        """
        Updates a local player's location and state to reflect an newly updated state.
        Renders the state to the view.
        """
        self.player_location = player_update["position"]
        self.last_state = player_update
        self.__view.render_player_update(player_update)

    def provide_move(self):
        """
        1. Prompts a player to specify a move.
        2. Parses user input.
        3. Returns the move specification as a tuple.
        """
        move = None
        self.__view.render_player_update(self.last_state)

        while True:
            try:
                user_input = input("\n{}, where would you like to move to?\n".format(self.name) +
                "Either provide a location (row, col) or a directional WASD input\n").strip()
                if user_input.startswith('(') and user_input.endswith(')'):
                    x, y = user_input[1:-1].split(",")
                    move = (int(x), int(y))
                else:
                    move = self.__wasd_movement(user_input)
                break
            except EOFError:
                sys.exit()
            except:
                print("Invalid selection, try again.")
                continue

        return move[::-1]

    def __wasd_movement(self, string_input):
        """
        Performs movement based on WASD commands
        """
        move = self.player_location

        if not string_input:
            raise MissingUserInputError

        for c in string_input:
            move = self.__apply_char_based_move(c, move)

        return move

    def __apply_char_based_move(self, c, position):
        """
        Applies an update to position based on the charectar
        """
        string_to_movement = {
            "w": (-1, 0), "s": (1, 0),
            "a": (0, -1), "d": (0, 1)
        }
        x, y = string_to_movement[c]
        return [position[0] + x, position[1] + y]

    def provide_name(self):
        """
        Prompts a player for their name.
        """
        self.name = "#"
        while not self.name.isalnum():
            self.name = input("\nPlayer, what is your name?\n")
        return self.name
