import sys
from src.Game.models.level.level_builder import LevelBuilder
from src.Game.controllers.game_manager import GameManager
from src.Player.local_player import LocalPlayer
from src.Game.models.level.level_builder import LevelBuilder
import src.Game.constants as constants

class SnarlLauncher:

    def __init__(self, level_file, num_players, initial_level, include_observer):
        """
        Creates a Snarl Launcher
        """
        self.levels = LevelBuilder.create_levels_from_levels_file(level_file)
        self.num_players = num_players
        self.inital_level = initial_level
        self.include_observer = include_observer

        if not constants.MIN_PLAYERS <= self.num_players <= constants.MAX_PLAYERS:
            print("Invalid player count: {}".format(num_players))
            sys.exit()

    def launch(self):
        game_manager = GameManager(self.levels,
                                    observe=self.include_observer,
                                    initial_level=self.inital_level,
                                    get_observation_confirmation=True)

        for _ in range(self.num_players):
            game_manager.register_player(LocalPlayer())
        game_manager.launch_game()