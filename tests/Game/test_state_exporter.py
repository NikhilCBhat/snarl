import sys
sys.path.append('.')
import unittest
from src.Game.models.state_exporter import StateExporter
from tests.Game.examples import create_basic_game_state

class Test(unittest.TestCase):

    def test_create_observer_game_state(self):
        game_state = create_basic_game_state()
        actual = StateExporter.create_observer_game_state(game_state)
        expected_level_map = "........................................\n" + \
            ".....WWWWWWW............................\n" + \
            ".....WP    W......WWWWW.................\n" + \
            ".....W     D------DZ  W.................\n" + \
            ".....W     W......W   W.................\n" + \
            ".....WWWWWWW......W   W.................\n" + \
            "..................W   W.................\n" + \
            "..................W   W.................\n" + \
            "..................W   W.................\n" + \
            "..................WWDWW.................\n" + \
            "...WWWWWWWWWWWW.....-...................\n" + \
            "...W          W.....-...................\n" + \
            "...W   K      D------...................\n" + \
            "...W   E      W.........................\n" + \
            "...WWWWWWWWWWWW.........................\n" + \
            "........................................"
        expected = {
            "is_exit_unlocked": False,
            "is_game_over": False,
            "current_turn": "p1",
            "level_count": 1,
            "current_level_number": 0,
            "moves_elapsed": 0,
            "latest_player_message": "",
            "level_map": expected_level_map,
            "exited_players_count": 0,
            "dead_players_count": 0
        }
        self.assertEqual(actual, expected)

    def test_create_adversary_game_state(self):
        game_state = create_basic_game_state()
        actual = StateExporter.create_adversary_game_state(game_state, "a1")
        expected_level_map = "........................................\n" + \
            ".....WWWWWWW............................\n" + \
            ".....WP    W......WWWWW.................\n" + \
            ".....W     D------DZ  W.................\n" + \
            ".....W     W......W   W.................\n" + \
            ".....WWWWWWW......W   W.................\n" + \
            "..................W   W.................\n" + \
            "..................W   W.................\n" + \
            "..................W   W.................\n" + \
            "..................WWDWW.................\n" + \
            "...WWWWWWWWWWWW.....-...................\n" + \
            "...W          W.....-...................\n" + \
            "...W   K      D------...................\n" + \
            "...W   E      W.........................\n" + \
            "...WWWWWWWWWWWW.........................\n" + \
            "........................................"
        actual_level_map = "\n".join(["".join(x) for x in actual["level_map"]])
        self.assertEqual(actual_level_map, expected_level_map)
        self.assertEqual(actual["type"], "adversary-update")
        self.assertEqual(actual["available_moves"], [(3, 19), (3, 20), (4, 19)])
        self.assertEqual(actual["player_locations"], [(2, 6)])
        self.assertEqual(actual["position"], (3, 19))

    def test_create_player_update(self):
        game_state = create_basic_game_state()
        actual = StateExporter.create_player_update(game_state, "p1")
        expected_layout = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1]]
        self.assertEqual(actual["type"], "player-update")
        self.assertEqual(actual["layout"], expected_layout)
        self.assertEqual(actual["objects"], [])
        self.assertEqual(actual["actors"], [])
        self.assertEqual(actual["position"], (2,6))
        self.assertEqual(actual["message"], "Current Turn: 0\n")
        self.assertEqual(actual["health"], 50)

    def test_create_end_level_state(self):
        game_state = create_basic_game_state()
        actual = StateExporter.create_end_level_state(game_state, 1)
        expected =  {
            "type": "end-level",
            "key": None,
            "exits": [],
            "ejects": [],
        }
        self.assertEqual(actual, expected)

    def test_create_end_game_state(self):
        game_state = create_basic_game_state()
        actual = StateExporter.create_end_game_state(game_state)
        expected_scores = [{'ejects': 0, 'exits': 0, 'keys': 0, 'name': 'p1','type': 'player-score'}]
        self.assertEqual(actual["type"], "end-game")
        self.assertEqual(actual["scores"], expected_scores)

if __name__ == '__main__':
    unittest.main()