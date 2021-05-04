import sys

sys.path.append('../../')
from src.Game.rule_checker import RuleChecker
from src.Game.constants import MANAGER_ID
from src.Game.snarl_errors import PlayerOutofMovesError
from src.Player.testing_player import TestingPlayer
from src.Game.controllers.game_manager import GameManager
from src.Game.models.level.level import Level
from src.Game.models.occupants import Player, Zombie, Occupant
from src.Game.models.states import GameState
from src.Game.models.level.level_builder import LevelBuilder
from tests.utils import read_user_input, swap_level, print_json

class ManagerTester():

    def run_test(self):
        """
        'Main' method for the tester
        """
        self.user_input = read_user_input()
        self.setup_communication_components()
        self.start_communication()
        self.create_initial_game_state()
        self.play_game()

    def setup_communication_components(self):
        """
        Sets up initial communication components.
        Creates a manager, proxy, and players.
        """
        name_list, level_json, _, _, actor_move_list_list = self.user_input
        level = LevelBuilder().create_level_from_json(swap_level(level_json))

        self.proxy = GameProxy()
        self.manager = GameManager(self.proxy, [level])
        self.players = [TestingPlayer(name, actor_move_list, self.proxy)
                        for name, actor_move_list in zip(name_list, actor_move_list_list)]

    def start_communication(self):
        """
        Starts communication between the players & manager.
        """
        # Players send connect message
        for player in self.players:
            player.connect_to_server()

        # Manager accepts connect request
        self.manager.accept_messages_from_server()

        # Players request to start game
        for player in self.players:
            player.start_game()

        # Manager creates & publishes initial game state
        self.manager.accept_messages_from_server()

        # Remove the initial state message
        self.proxy._messages = {key: [] for key in self.proxy._messages}
        self.proxy._trace = []

    def create_initial_game_state(self):
        """
        Creates the initial game state based on the occupant locations.
        """
        name_list, _, _, point_list, _ = self.user_input

        state_dict = self.manager.state.to_dict()

        for i in range(len(point_list) - len(name_list)):
            z = Zombie(str(i))
            state_dict["occupant_order"].append(z.id)
            state_dict["occupants"][str(i)] = z

        for occupant in state_dict["occupants"].values():
            if occupant.current_tile:
                occupant.current_tile.current_occupant = None
                occupant.current_tile = None

        for occupant_id, location in zip(state_dict["occupant_order"], point_list):
            occupant = state_dict["occupants"][occupant_id]
            self.__place_occupant(location, state_dict["levels"][0], occupant)

        self.manager.state = GameState.from_state_dict(state_dict)

    def play_game(self):
        """
        Plays the game using the preestablished moves.
        """
        self.manager._send_players_game_state()

        _, _, num_turns, _, _ = self.user_input

        interactors = [self.manager] + self.players
        while self.manager.state.turns_elapsed < num_turns and not self.manager.state.is_game_over:
            for interactor in interactors:
                try:
                    interactor.accept_messages_from_server()
                except PlayerOutofMovesError:
                    return self.generate_output()
                if RuleChecker.is_game_over(self.manager.state):
                    self.generate_output()

        self.generate_output()

    def generate_output(self):
        """
        Generates & prints the output.
        """
        self.trace = [self.__create_trace_entry(
            trace) for trace in self.proxy._trace]
        self.trace = [x for x in self.trace if x is not None]

        print_json([self.manager.state.to_json(), self.trace])
        sys.exit()

    def __place_occupant(self, location, level: Level, occupant: Occupant):
        """
        Places an occupant at a given location, without updating the state
        """
        tile = level.get_tile(*location)
        occupant.move(tile)

    def __create_trace_entry(self, message):
        """
        Creates a single trace entry
        """
        sender, to, message_type, body = parse_message_json(message)

        if message_type == MessageType.GAME_STATE.value and \
                body["is_alive"] and not body["has_reached_exit"] \
                and not body["is_game_over"]:
            return [to, self.__create_player_update_json(body)]

        if message_type == MessageType.OCCUPANT_MOVE.value and sender == MANAGER_ID:
            return [to, *self.__create_move_update_json(body)]

    def __create_player_update_json(self, player_game_state):
        """
        Creates a JSON of the player update
        """
        return {
            "type": "player-update",
            "layout": player_game_state["layout"],
            "position": player_game_state["current_location"][::-1],
            "objects": player_game_state["objects"],
            "actors": player_game_state["actors"]
        }

    def __create_move_update_json(self, move_response):
        """
        Creates the manager entry corresponding to a move response.
        """
        result = move_response["result"]
        maybe_point = None if move_response["stayed_in_place"] else move_response["move"][::-1]

        return {"type": "move", "to": maybe_point}, result
