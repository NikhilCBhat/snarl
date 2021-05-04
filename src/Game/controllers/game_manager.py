from src.Common.adversary_client import AdversaryClient
from src.Game.models.states import GameState
from src.Game.models.occupants import Player, Ghost, Zombie
from src.Game.models.state_exporter import StateExporter
from src.Game.rule_checker import RuleChecker
import src.Game.constants as constants
from collections import defaultdict
from src.Observer.local_observer import LocalObserver
from src.Common.user import User
from src.Adversary.local_adversary import LocalAdversary

class GameManager:

    def __init__(self, levels, observe=True, initial_level=1, create_adversaries=True, get_observation_confirmation=False):
        """
        Creates a manager for a Snarl game.
        """
        self.__players = {}
        self.__adversaries = defaultdict(dict)
        self.__observers = [LocalObserver()] if observe else []
        self.__levels = levels
        self.__initial_level = initial_level
        self.__get_observation_confirmation = get_observation_confirmation
        self.__actor_type_to_state_function = {
            constants.PLAYER_STRING: StateExporter.create_player_update,
            constants.ADVERSARY_STRING: StateExporter.create_adversary_game_state
        }
        if create_adversaries:
            self.__create_local_adversaries()

    @property
    def __current_actors(self):
        """
        The current players & adversaries
        """
        return {**self.__players, **self.__adversaries[self.state.current_level]}

    @property
    def __all_actors(self):
        """
        All players and adversaries
        """
        actors = self.__players
        for dict_of_adversaries in self.__adversaries.values():
            actors = {**actors, **dict_of_adversaries}
        return actors

    @property
    def __names(self):
        """
        All the names of the players & adversaries.
        Used for ensuring name validity
        """
        names = set(self.__players.keys())
        for adv_dict in self.__adversaries.values():
            names |= adv_dict.keys()
        return names

    def register_player(self, player: User):
        """
        Registers a player to a game.
        """
        player_name = None
        while not player_name or player_name in self.__names:
            player_name = player.provide_name()
        self.__players[player_name] = player

    def register_adversary(self, adversary: AdversaryClient):
        """
        Registers a adversary to a game.
        """
        level = None
        while level is None:
            level = adversary.provide_level()

        adversary.name = "level{}_{}{}".format(level,
            adversary.provide_adversary_type(), len(self.__adversaries[level]))

        self.__adversaries[level][adversary.name] = adversary

    def launch_game(self):
        """
        1. Creates a game & notifies players
        2. Starts the game loop
        3. Sends the game over message
        """
        self.__create_initial_game_state()
        self.__send_start_message()

        while not RuleChecker.is_game_over(self.state):
            current_level = self.state.current_level
            while current_level == self.state.current_level \
                and not RuleChecker.is_level_over(self.state):
                self.__send_state()
                self.__play_move()
            self.__send_level_over()
        self.__send_game_over()

    def __create_initial_game_state(self):
        """
        Creates inital game state.
        """
        actor_type_to_object_type = {
            constants.GHOST_ACTOR_TYPE: Ghost,
            constants.ZOMBIE_ACTOR_TYPE: Zombie
        }
        adversary_dict = {
            level: [actor_type_to_object_type[adversary.provide_adversary_type()](adversary.name, level_number=level) \
                    for adversary in dict_of_adversaries.values()]
            for level, dict_of_adversaries in self.__adversaries.items()
        }

        self.state = GameState(self.__levels, [Player(name) for name in self.__players], adversary_dict)
        for _ in range(self.__initial_level):
            self.state.progress_to_next_level()

    def __send_start_message(self):
        """
        Sends the start message for every player.
        """
        message = {
            "type": "start-level",
            "level": self.state.current_level,
            "players": list(self.__players.keys())
            }

        for player in self.__players.values():
            player.accept_game_state(message)

    def __play_move(self):
        """
        1. Gets the move from the current actor
        2. Applies that move to the GameState
        3. Sends the result to the actor.
        """
        current_turn = self.state.current_turn
        current_actors = self.__current_actors
        if current_turn in current_actors:
            while True:
                move = current_actors[current_turn].provide_move() or \
                    self.state.occupants[current_turn].current_location
                try:
                    RuleChecker.validate_move(self.state, current_turn, move)
                    result = self.state.update(current_turn, move)
                    current_actors[current_turn].accept_game_state(result)
                    break
                except Exception as e:
                    print("Player provided an invalid move.\nIt raised a:", type(e))
                    current_actors[current_turn].accept_game_state(constants.INVALID_RESULT)
                    continue

    def __update_observers(self):
        """
        Updates the observer on the GameState.
        """
        for observer in self.__observers:
            observer.accept_game_state(StateExporter.create_observer_game_state(self.state),
                                        self.__get_observation_confirmation)

    def __send_state(self):
        """
        Sends the game state to all connected entitites.
        """
        for actor_name, actor in self.__current_actors.items():
            state_to_send = self.__actor_type_to_state_function[actor.actor_type](self.state, actor_name)
            actor.accept_game_state(state_to_send)
        self.__update_observers()

    def __send_level_over(self):
        """
        Sends the level over message to all connected entitites.
        """
        level_number = self.state.current_level - 1 + RuleChecker.is_game_over(self.state)
        for actor in self.__all_actors.values():
            actor.accept_game_state(StateExporter.create_end_level_state(self.state, level_number))
        self.__update_observers()

    def __send_game_over(self):
        """
        Sends the game over message to all connected entitites.
        """
        for actor in self.__all_actors.values():
            actor.accept_game_state(StateExporter.create_end_game_state(self.state))
        self.__update_observers()

    def __create_local_adversaries(self):
        """
        Creates local adversaries based on the description in the Milestone.
        """
        for level_number, _ in enumerate(self.__levels, 1):
            for _ in range(level_number//2 + 1):
                self.register_adversary(LocalAdversary(constants.ZOMBIE_ACTOR_TYPE, level_number - 1))
            for _ in range((level_number-1)//2):
                self.register_adversary(LocalAdversary(constants.GHOST_ACTOR_TYPE, level_number - 1))