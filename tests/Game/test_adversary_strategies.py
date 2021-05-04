import sys
sys.path.append('.')
import unittest
from src.Game.models.state_exporter import StateExporter
from src.Adversary.adversary_strategies import RandomStrategy, StayinPlaceStrategy, MovetoPlayerStrategy, GhostStrategy, ZombieStrategy
from tests.Game.examples import create_basic_game_state, create_basic_game_state_ghost

class Test(unittest.TestCase):

    def test_random_strategy_calculate_move(self):
        possible_moves = [(7, 2), (8, 2), (9, 2), (7, 3), (8, 3), (9, 3)]
        current_location = (8, 2)
        level = StateExporter.create_adversary_game_state(create_basic_game_state(), "a1")["level_map"]
        player_locations = [(6, 2), (7, 2)]
        move = RandomStrategy.calculate_move(possible_moves, current_location, level, player_locations)
        self.assertTrue(move in possible_moves)

    def test_stay_in_place_strategy_calculate_move(self):
        possible_moves = [(7, 2), (8, 2), (9, 2), (7, 3), (8, 3), (9, 3)]
        current_location = (8, 2)
        level = StateExporter.create_adversary_game_state(create_basic_game_state(), "a1")["level_map"]
        player_locations = [(6, 2), (7, 2)]
        actual = StayinPlaceStrategy.calculate_move(possible_moves, current_location, level, player_locations)
        self.assertEqual(actual, current_location)

    def test_move_to_player_strategy_calculate_move(self):
        possible_moves = [(7, 2), (8, 2), (9, 2), (7, 3), (8, 3), (9, 3)]
        current_location = (8, 2)
        level = StateExporter.create_adversary_game_state(create_basic_game_state(), "a1")["level_map"]
        player_locations = [(6, 2), (7, 2)]
        actual = MovetoPlayerStrategy.calculate_move(possible_moves, current_location, level, player_locations)
        expected = (7, 2)
        self.assertEqual(actual, expected)

    def test_move_to_player_strategy_closest_player(self):
        current_location = (2, 3)
        player_locations = [(0, 0), (1, 1)]
        actual = MovetoPlayerStrategy.closest_player(current_location, player_locations)
        expected = (1, 1)
        self.assertEqual(actual, expected)

    def test_ghost_strategy_calculate_move(self):
        possible_moves = [(3, 19), (2, 19), (3, 18), (3, 20), (4, 19)]
        current_location = (3, 19)
        level = StateExporter.create_adversary_game_state(create_basic_game_state_ghost(), "a1")["level_map"]
        player_locations = [(2, 6)]
        actual = GhostStrategy.calculate_move(possible_moves, current_location, level, player_locations)
        expected = (2, 19)
        self.assertEqual(expected, actual)

    def test_zombie_strategy_calculate_move(self):
        # zombie guards items
        possible_moves = [(3, 19), (3, 20), (4, 19)]
        current_location = (3, 19)
        level = StateExporter.create_adversary_game_state(create_basic_game_state(), "a1")["level_map"]
        player_locations = [(2, 6)]
        actual = ZombieStrategy.calculate_move(possible_moves, current_location, level, player_locations)
        expected = (3, 20)
        # since no players in room, zombie should move closer to key
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
