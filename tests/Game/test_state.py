import sys
sys.path.append('.')
import unittest
from src.Game.models.level.level_builder import LevelBuilder
from src.Game.models.states import GameState
from src.Game.models.occupants import Player, Zombie
from tests.Game.examples import create_basic_game_state, create_two_level_game_state, level_1

class Test(unittest.TestCase):

    def create_basic_game_state(self):
        return create_basic_game_state(), level_1()

    def create_two_level_game_state(self):
        create_two_level_game_state()

    def test_create_game_state(self):
        """
        Ensures that a new game state is created correctly.
        """
        error_string_format = "Error: Create game state test failed. Invalid: {}"
        game_state, level = self.create_basic_game_state()

        self.assertEqual(game_state.current_level, 0, error_string_format.format("Level Id"))
        self.assertEqual(game_state.current_turn, "p1", error_string_format.format("Current Turn"))
        self.assertEqual(len(game_state.occupants), 2, error_string_format.format("Occupant Count"))
        self.assertFalse(game_state.is_exit_unlocked, error_string_format.format("is_exit_unlocked"))
        self.assertFalse(game_state.is_game_over, error_string_format.format("is_game_over"))

    def test_occupant_movement(self):
        """
        Tests to see if an occupant is able to move.
        We test both player and adversary movement.
        """
        for i, id in enumerate(["p1", "a1"]):
            error_string_format = "Error: Occupant Movement test failed. Invalid: {}"
            game_state, _ = self.create_basic_game_state()

            p1_start_location = game_state.occupants[id].current_tile

            self.assertIsNotNone(p1_start_location, error_string_format.format("Start location is not None"))

            new_location = (7,3+i)
            game_state.update(id,new_location)

            self.assertEqual(game_state.occupants[id].current_location, new_location)
            self.assertIsNone(p1_start_location.current_occupant)

    def test_player_runs_into_adversary(self):
        """
        Tests to see interactions when a player runs into an adversary
        """

        game_state, _ = self.create_basic_game_state()

        player1 = game_state.occupants["p1"]
        adversary1 = game_state.occupants["a1"]

        new_location = (8,12)

        game_state.update("p1", new_location)

        self.assertTrue(player1.is_alive)

        game_state.update("a1", new_location)

        self.assertTrue(player1.is_alive)

    def test_adversary_runs_into_player(self):
        """
        Tests to see interactions when a player runs into an adversary
        """

        game_state, _ = self.create_basic_game_state()

        player1 = game_state.occupants["p1"]

        new_location = (8,12)
        game_state.update("p1", new_location)
        self.assertTrue(player1.is_alive)

        for _ in range(5):
            self.assertTrue(player1.is_alive)
            game_state.update("a1", new_location)

        self.assertFalse(player1.is_alive)

    def test_game_over_players_die(self):
        actual = create_two_level_game_state(4, False)
        self.assertEqual(actual.current_level, 0, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "p0", "Unexpected current turn")
        self.assertFalse(actual.is_exit_unlocked, "Level should be locked")
        self.assertFalse(actual.is_game_over, "Game should not be over")

        # move adversary to all players
        player_locations = [p.current_location for p in actual.players]
        for _ in range(5):
            for location in player_locations:
                actual.update("a1", location)

        self.assertEqual(actual.current_level, 0, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "a0", "Unexpected current turn")
        self.assertFalse(actual.is_exit_unlocked, "Level should be locked")
        self.assertTrue(actual.is_game_over, "Game should be over")

    def test_progress_to_next_level(self):
        actual = create_two_level_game_state(num_players=1)
        self.assertEqual(actual.current_level, 0, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "p0", "Unexpected current turn")
        self.assertFalse(actual.is_exit_unlocked, "Level should be locked")
        self.assertFalse(actual.is_game_over, "Game should not be over")

        # move player to key
        actual.update("p0", (7, 12))
        self.assertEqual(actual.current_level, 0, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "a0", "Unexpected current turn")
        self.assertTrue(actual.is_exit_unlocked, "Level should be unlocked")
        self.assertFalse(actual.is_game_over, "Game should not be over")

        # move player to exit
        actual.update("p0", (7, 13))
        self.assertEqual(actual.current_level, 1, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "p0", "Unexpected current turn")
        self.assertFalse(actual.is_exit_unlocked, "Level should not be unlocked")
        self.assertFalse(actual.is_game_over, "Game should not be over")

    def test_players_win_game(self):
        actual, _ = self.create_basic_game_state()
        self.assertEqual(actual.current_level, 0, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "p1", "Unexpected current turn")
        self.assertFalse(actual.is_exit_unlocked, "Level should be locked")
        self.assertFalse(actual.is_game_over, "Game should not be over")

        # move player to key, then exit
        actual.update("p1", (7, 12))
        actual.update("p1", (7, 13))

        self.assertEqual(actual.current_level, 0, "Unexpected current level.")
        self.assertEqual(actual.current_turn, "p1", "Unexpected current turn")
        self.assertTrue(actual.is_exit_unlocked, "Level should be unlocked")
        self.assertTrue(actual.is_game_over, "Game should be over")

    def test_create_state_dict(self):
        level_1 = LevelBuilder()\
                        .create_level(40,16)\
                        .add_room((5,1), 7, 5, {(11,3)})\
                        .add_room((18,2), 5, 8, {(18,3), (20,9)})\
                        .add_room((3,10), 12, 5, {(14,12)})\
                        .add_hallway((18,3), (11,3))\
                        .add_hallway((14,12), (20,9), [(20,12)])\
                        .add_item("key", (7,12))\
                        .add_item("exit", (7,13))\
                        .build()
        p100 = Player("p100")
        p101 = Player("p101")
        a0 = Zombie("a0")
        adversaries={0: [a0]}

        actual = GameState(levels=[level_1], players=[p100, p101], adversaries=adversaries).to_dict()
        expected = {
            "occupants": {"p100": p100, "p101": p101, "a0": a0},
            "levels": [level_1],
            "current_level": -1,
            "current_turn": "p100",
            "is_exit_unlocked": False,
            "is_game_over": False
        }
        self.assertEqual(actual["occupants"], expected["occupants"], "Occupants mismatch")
        self.assertEqual(actual["current_level"], expected["current_level"], "Current level mismatch")
        self.assertEqual(actual["current_turn"], expected["current_turn"], "Current turn mismatch")
        self.assertEqual(actual["is_exit_unlocked"], expected["is_exit_unlocked"], "is_exit_unlocked mismatch")
        self.assertEqual(actual["is_game_over"], expected["is_game_over"], "is_game_over mismatch")

    def test_load_state_dict(self):
        level_1 = LevelBuilder()\
                        .create_level(40,16)\
                        .add_room((5,1), 7, 5, {(11,3)})\
                        .add_room((18,2), 5, 8, {(18,3), (20,9)})\
                        .add_room((3,10), 12, 5, {(14,12)})\
                        .add_hallway((18,3), (11,3))\
                        .add_hallway((14,12), (20,9), [(20,12)])\
                        .add_item("key", (7,12))\
                        .add_item("exit", (7,13))\
                        .build()

        p0 = Player("p0")
        p1 = Player("p1")
        a0 = Zombie("a0")
        adversaries={0: [a0]}

        test_dict = {
            "occupants": {"p0": p0, "p1": p1, "a0": a0},
            "_all_adversaries": {0: [a0]},
            "levels": [level_1],
            "current_level": -1,
            "current_turn": "p0",
            "is_exit_unlocked": False,
            "is_game_over": False,
            "occupant_order": ["p0", "p1", "a0"]
        }
        actual = GameState.from_state_dict(test_dict)
        expected = GameState(levels=[level_1], players=[p0, p1], adversaries=adversaries)
        self.assertEqual(actual.occupants, expected.occupants, "Occupants mismatch")
        self.assertEqual(actual.current_level, expected.current_level, "Current level mismatch")
        self.assertEqual(actual.current_turn, expected.current_turn, "Current turn mismatch")
        self.assertEqual(actual.is_exit_unlocked, expected.is_exit_unlocked, "is_exit_unlocked mismatch")
        self.assertEqual(actual.is_game_over, expected.is_game_over, "is_game_over mismatch")
        self.assertEqual(actual.occupant_order, expected.occupant_order, "occupant order mismatch")

if __name__ == '__main__':
    unittest.main()
