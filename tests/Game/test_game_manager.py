import sys
import unittest

# Local Imports
sys.path.append('.')
from tests.Game.examples import level_1
from src.Player.mock_player import MockPlayer
from src.Game.controllers.game_manager import GameManager
from src.Game.constants import STAY_IN_PLACE_STRATEGY, ADVERSARY_UPDATE_MESSAGE
from src.Adversary.local_adversary import LocalAdversary

class Test(unittest.TestCase):

    def test_basic_game_messages(self):
        manager = GameManager([level_1()], False, create_adversaries=False)
        nikhil = MockPlayer("nikhil", [None, None])
        manager.register_player(nikhil)
        try:
            manager.launch_game()
        except IndexError:
            pass

        layout = nikhil.trace[2]["layout"]
        position = nikhil.trace[2]["position"]

        expected_trace = ['nikhil',
                          {'type': 'start-level', 'level': 0,
                              'players': ['nikhil']},
                          {'type': 'player-update', 'layout': layout, 'objects': [], 'actors': [],
                              'position': position, 'message': 'Current Turn: 0\n', 'health': 50},
                          None,
                          'OK',
                          {'type': 'player-update', 'layout': layout, 'objects': [], 'actors': [],
                              'position': position, 'message': 'Current Turn: 1\n', 'health': 50},
                          None,
                          'OK',
                          {'type': 'player-update', 'layout': layout, 'objects': [], 'actors': [],
                              'position': position, 'message': 'Current Turn: 2\n', 'health': 50}]

        self.assertEqual(nikhil.trace, expected_trace)


    def test_game_with_adversaries(self):
        manager = GameManager([level_1()], False, create_adversaries=False)
        nikhil = MockPlayer("nikhil", [None, None])
        adversary = LocalAdversary(strategy_type=STAY_IN_PLACE_STRATEGY)
        manager.register_player(nikhil)
        manager.register_adversary(adversary)
        try:
            manager.launch_game()
        except IndexError:
            pass

        self.assertEqual(len(adversary._trace), 7)
        for message in adversary._trace:
            if isinstance(message, str):
                self.assertEqual(message, "OK")
            else:
                self.assertEqual(message['type'], ADVERSARY_UPDATE_MESSAGE)

if __name__ == '__main__':
    unittest.main()
