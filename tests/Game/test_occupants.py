import sys
sys.path.append('.')
import unittest
import src.Game.constants as constants
from src.Game.models.occupants import Player, Zombie
from src.Game.models.level.tile import Tile

class Test(unittest.TestCase):

    def test_occupant_creation(self):
        p1 = Player("p1")
        self.assertEqual(p1.id, "p1")
        self.assertIsNone(p1.current_tile)
        self.assertTrue(p1.is_alive)

    def test_adversary_creation(self):
        a1 = Zombie("a1")
        self.assertEqual(a1.id, "a1")
        self.assertIsNone(a1.current_tile)
        self.assertTrue(a1.is_alive)

    def test_expel(self):
        p1 = Player("p1")
        self.assertTrue(p1.is_alive)
        p1.expel()
        self.assertFalse(p1.is_alive)

    def test_reset_health(self):
        p1 = Player("p1")
        self.assertEqual(p1.health, constants.PLAYER_HEALTH)
        p1.health = 0
        self.assertEqual(p1.health, 0)
        p1.reset_health()
        self.assertEqual(p1.health, constants.PLAYER_HEALTH)

    def test_move(self):
        """
        Further movement based interactions
        are tested in test_state and test_adversary_strategies.
        """
        p1 = Player("p1")
        a1 = Zombie("a1")

        for occupant in [p1, a1]:
            t1 = Tile(3,4)
            t2 = Tile(4,5)

            self.assertIsNone(occupant.current_tile)

            occupant.move(t1)
            self.assertEqual(occupant.current_tile, t1)
            self.assertEqual(t1.current_occupant, occupant)

            occupant.move(t2)
            self.assertEqual(occupant.current_tile, t2)
            self.assertEqual(t2.current_occupant, occupant)
            self.assertIsNone(t1.current_occupant)

    def test_receive_attack(self):
        p1 = Player("p1")
        a1 = Zombie("a1")
        self.assertEqual(p1.health, constants.PLAYER_HEALTH)
        p1.receive_attack(a1)
        self.assertEqual(p1.health, constants.PLAYER_HEALTH - constants.ZOMBIE_HIT_STRENGTH)

    def test_interact_with_player(self):
        # interacting with player = receiving an attack from player
        p1 = Player("p1")
        a1 = Zombie("a1")
        self.assertEqual(a1.health, constants.ZOMBIE_HEALTH)
        a1.receive_attack(p1)
        self.assertEqual(a1.health, constants.ZOMBIE_HEALTH - constants.PLAYER_HIT_STRENGTH)

    def test_interact_with_adversary(self):
        # interacting with adversary = receiving an attack from adversary
        p1 = Player("p1")
        a1 = Zombie("a1")
        self.assertEqual(p1.health, constants.PLAYER_HEALTH)
        p1.interact_with_adversary(a1)
        self.assertEqual(p1.health, constants.PLAYER_HEALTH - constants.ZOMBIE_HIT_STRENGTH)

    def test_interact_with_occupant(self):
        p1 = Player("p1")
        a1 = Zombie("a1")
        # player receives zombie attack
        self.assertEqual(a1.health, constants.ZOMBIE_HEALTH)
        a1.interact_with_occupant(p1)
        self.assertEqual(p1.health, constants.PLAYER_HEALTH - constants.ZOMBIE_HIT_STRENGTH)
        self.assertEqual(a1.health, constants.ZOMBIE_HEALTH)
        # zombie receives player attack
        p1.interact_with_occupant(a1)
        self.assertEqual(p1.health, constants.PLAYER_HEALTH - constants.ZOMBIE_HIT_STRENGTH)
        self.assertEqual(a1.health, constants.ZOMBIE_HEALTH - constants.PLAYER_HIT_STRENGTH)

    def test_to_json(self):
        p1 = Player("p1")
        t1 = Tile(3,4)
        p1.move(t1)
        expected = {
            "type": constants.PLAYER_ACTOR_TYPE,
            "name": "p1",
            "position": (4, 3)
        }
        actual = p1.to_json()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
