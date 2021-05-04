import sys
import unittest

sys.path.append('.')
import src.Game.constants as constants
from src.Game.rule_checker import RuleChecker
from src.Game.snarl_errors import InvalidDestinationError, \
    InvalidOccupantIdError, NonTraversableTileError, InvalidOccupantTurnOrder

from tests.Game.examples import create_basic_game_state, create_two_level_game_state

class Test(unittest.TestCase):

    def test_game_and_level_over_when_players_die(self):
        state = create_basic_game_state()
        self.assertFalse(RuleChecker.is_game_over(state))
        self.assertFalse(RuleChecker.is_level_over(state))
        RuleChecker.validate_game_state(state)

        a1_location = state.occupants["a1"].current_location
        p1_location = state.occupants["p1"].current_location

        with self.assertRaises(InvalidDestinationError):
            RuleChecker.validate_move(state, "p1", a1_location)

        for _ in range(5):
            state.update("a1", p1_location)

        self.assertTrue(RuleChecker.is_game_over)
        self.assertTrue(RuleChecker.is_level_over)
        self.assertEqual(RuleChecker.get_game_winner(state), constants.ADVERSARY_STRING)

    def test_game_not_over_when_one_player_dies(self):
        state = create_two_level_game_state()
        self.assertFalse(RuleChecker.is_game_over(state))
        self.assertFalse(RuleChecker.is_level_over(state))
        RuleChecker.validate_game_state(state)

        a1_location = state.occupants["a1"].current_location

        with self.assertRaises(InvalidOccupantTurnOrder):
            RuleChecker.validate_move(state, "p1", a1_location)

        state.update("p1", a1_location)
        self.assertFalse(RuleChecker.is_game_over(state))
        self.assertFalse(RuleChecker.is_level_over(state))

    def test_game_over_when_player_wins(self):
        state = create_basic_game_state()
        self.assertFalse(RuleChecker.is_game_over(state))
        self.assertFalse(RuleChecker.is_level_over(state))
        RuleChecker.validate_game_state(state)

        # move player to key
        state.update("p1", (7, 12))
        # move player to exit
        state.update("p1", (7, 13))

        self.assertTrue(RuleChecker.is_game_over)
        self.assertTrue(RuleChecker.is_level_over)
        self.assertEqual(RuleChecker.get_game_winner(state), constants.PLAYER_STRING)

    def test_level_over_but_not_game_over_when_player_beats_level(self):
        state = create_two_level_game_state(num_players=1)
        self.assertFalse(RuleChecker.is_game_over(state))
        self.assertFalse(RuleChecker.is_level_over(state))
        RuleChecker.validate_game_state(state)

        # move player to key
        state.update("p0", (7, 12))
        # move player to exit
        state.update("p0", (7, 13))

        self.assertFalse(RuleChecker.is_game_over(state))

    def test_valid_move(self):
        state = create_basic_game_state()

        with self.assertRaises(InvalidOccupantIdError):
            RuleChecker.validate_move(state, "p0", [6,4])

        with self.assertRaises(InvalidDestinationError):
            RuleChecker.validate_move(state, "p1", [10,2])

        with self.assertRaises(NonTraversableTileError):
            RuleChecker.validate_move(state, "p1", [16,4])

        RuleChecker.validate_move(state, "p1", state.occupants["p1"].current_location)

if __name__ == '__main__':
    unittest.main()
