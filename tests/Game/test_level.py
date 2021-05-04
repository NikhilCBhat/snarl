import sys
import unittest

# Local imports
sys.path.append('.')
from src.Game.models.level.level_builder import LevelBuilder
from src.Game.snarl_errors import *

class Test(unittest.TestCase):

    def test_empty_level(self):
        level = LevelBuilder().create_level(10, 3).build()
        actual = str(level)
        expected = "..........\n" \
                   "..........\n" \
                   ".........."
        self.assertEqual(actual, expected, "Empty Level 10x3 Test Failed.")
        level = LevelBuilder().create_level(2, 3).build()
        actual = str(level)
        expected = "..\n" \
                   "..\n" \
                   ".."
        self.assertEqual(actual, expected, "Empty Level 2x3 Test Failed.")

    def test_level_with_room(self):
        level = LevelBuilder()\
                            .create_level(20, 10)\
                            .add_room((5,1), 7, 5, {(11,3)})\
                            .build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W     W........\n" \
                   ".....W     D........\n" \
                   ".....W     W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Room with Door Creation Failed.")
        level = LevelBuilder()\
                            .create_level(20, 10)\
                            .add_room((5,1), 7, 5, {(11,3)})\
                            .add_room((15,2), 5, 5, {(15,3)})\
                            .add_hallway((11,3), (15,3))\
                            .build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W     W...WWWWW\n" \
                   ".....W     D---D   W\n" \
                   ".....W     W...W   W\n" \
                   ".....WWWWWWW...W   W\n" \
                   "...............WWWWW\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Second Room & Hallway Creation Failed.")

    def test_room_with_key(self):
        level = LevelBuilder()\
                            .create_level(20, 10)\
                            .add_item("key", (8,4))\
                            .add_room((5,1), 7, 5, {(11,3)})\
                            .build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W     W........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Room with Key Creation Failed.")

    def test_exits_and_keys(self):
        level = LevelBuilder()\
                            .create_level(20, 10)\
                            .add_item("key", (8,4))\
                            .add_room((5,1), 7, 5, {(11,3)})\
                            .add_item("key", (10,2))\
                            .add_item("exit", (8,2))\
                            .build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Keys and Exits Failed.")

    def test_multiple_rooms(self):
        level = LevelBuilder()\
                            .create_level(40, 10)\
                            .add_item("key", (8,4))\
                            .add_room((5,1), 7, 5, {(11,3)})\
                            .add_room((18,2), 5, 3, {(18,3), (21,4)})\
                            .add_room((20,7), 13, 3, {(21,7)})\
                            .add_hallway((11,3), (18,3))\
                            .add_hallway((21,4), (21,7))\
                            .add_item("key", (8, 4))\
                            .build()
        actual = str(level)
        expected = "........................................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W......WWWWW.................\n" \
                   ".....W     D------D   W.................\n" \
                   ".....W  K  W......WWWDW.................\n" \
                   ".....WWWWWWW.........-..................\n" \
                   ".....................-..................\n" \
                   "....................WDWWWWWWWWWWW.......\n" \
                   "....................W           W.......\n" \
                   "....................WWWWWWWWWWWWW......."
        self.assertEqual(actual, expected, "Multiple Rooms Creation Failed.")


    def test_hallway_with_waypoint(self):
        level = LevelBuilder()\
                            .create_level(40, 16)\
                            .add_room((5,1), 7, 5, {(11,3)})\
                            .add_room((18,2), 5, 8, {(18,3), (20,9)})\
                            .add_room((3,10), 12, 5, {(14,12)})\
                            .add_hallway((18,3), (11,3))\
                            .add_hallway((14,12), (20,9), [(20,12)])\
                            .add_item("key", (7, 12))\
                            .build()

        actual = str(level)
        expected = "........................................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W......WWWWW.................\n" \
                   ".....W     D------D   W.................\n" \
                   ".....W     W......W   W.................\n" \
                   ".....WWWWWWW......W   W.................\n" \
                   "..................W   W.................\n" \
                   "..................W   W.................\n" \
                   "..................W   W.................\n" \
                   "..................WWDWW.................\n" \
                   "...WWWWWWWWWWWW.....-...................\n" \
                   "...W          W.....-...................\n" \
                   "...W   K      D------...................\n" \
                   "...W          W.........................\n" \
                   "...WWWWWWWWWWWW.........................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Hallway with Waypoint Creation Failed.")

    def test_corner_door(self):
        level = LevelBuilder().create_level(40,7)\
                              .add_room((5,1), 7, 5, {(11,5)})\
                              .add_room((15,1), 4, 3, {(15,3)})\
                              .add_room((22,1), 5, 4, {(22,1)})\
                              .add_room((32,1), 4, 4, {(35,1)})\
                              .build()

        actual = str(level)
        expected = "........................................\n" \
                   ".....WWWWWWW...WWWW...DWWWW.....WWWD....\n" \
                   ".....W     W...W  W...W   W.....W  W....\n" \
                   ".....W     W...DWWW...W   W.....W  W....\n" \
                   ".....W     W..........WWWWW.....WWWW....\n" \
                   ".....WWWWWWD............................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Corner Door Creation Failed.")

    def test_multiple_connections_between_two_rooms(self):
        lb = LevelBuilder().create_level(40, 16)\
                                .add_room((5,5), 7, 5, {(11, 7), (11, 8)})\
                                .add_room((26,6), 5, 8, {(26,7), (26, 8)})\
                                .add_hallway((26,7), (11,7))\
                                .add_hallway((26,8), (11,8))
        level = lb.build()
        actual = str(level)
        expected = "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W..............WWWWW.........\n" \
                   ".....W     D--------------D   W.........\n" \
                   ".....W     D--------------D   W.........\n" \
                   ".....WWWWWWW..............W   W.........\n" \
                   "..........................W   W.........\n" \
                   "..........................W   W.........\n" \
                   "..........................W   W.........\n" \
                   "..........................WWWWW.........\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Room with multiple connections failed.")

    def test_hallway_loops_back_to_room(self):
        lb = LevelBuilder().create_level(40, 16)\
                                .add_room((5,5), 7, 5, {(11, 8), (10, 9)})\
                                .add_hallway((10, 9), (11,8), [(10, 11), (21, 11), (21, 8)])
        level = lb.build()
        actual = str(level)
        expected = "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W............................\n" \
                   ".....W     W............................\n" \
                   ".....W     D----------..................\n" \
                   ".....WWWWWDW.........-..................\n" \
                   "..........-..........-..................\n" \
                   "..........------------..................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Loop back hallway failed.")

    def test_hallway_no_rooms_invalid(self):
        with self.assertRaises(InvalidHallwayError):
            level = LevelBuilder()\
                                .create_level(40, 16)\
                                .add_hallway((18,3), (11,3))\
                                .build()

    def test_hallway_one_room_invalid(self):
        with self.assertRaises(InvalidHallwayError):
            level = LevelBuilder()\
                                .create_level(40, 16)\
                                .add_room((5,1), 7, 5, {(11,3)})\
                                .add_hallway((18,3), (11,3))\
                                .build()

    def test_door_in_room_invalid(self):
        with self.assertRaises(InvalidDoorError):
            level = LevelBuilder()\
                                .create_level(40, 16)\
                                .add_room((5,1), 7, 5, {(8, 4)})\
                                .build()

    def test_door_in_void_invalid(self):
        with self.assertRaises(InvalidDoorError):
            level = LevelBuilder().create_level(40, 16)\
                                  .add_room((5,1), 7, 5, {(30, 12)})\
                                  .build()

    def test_room_overlap_invalid(self):
        with self.assertRaises(FloorPlanOverlapError):
            level = LevelBuilder().create_level(40, 16)\
                                  .add_room((5,1), 7, 5, {(11, 5)})\
                                  .add_room((7,4), 7, 5, {(8,4)})\
                                  .build()

    def test_hallway_overlap_room_invalid(self):
        lb = LevelBuilder().create_level(40, 16)\
                                .add_room((5,1), 7, 5, {(11, 3)})\
                                .add_room((26,2), 5, 8, {(26,3)})\
                                .add_room((15,2), 6, 4, {(16,2)})
        level = lb.build()
        actual = str(level)
        expected = "........................................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W...WDWWWW.....WWWWW.........\n" \
                   ".....W     D...W    W.....D   W.........\n" \
                   ".....W     W...W    W.....W   W.........\n" \
                   ".....WWWWWWW...WWWWWW.....W   W.........\n" \
                   "..........................W   W.........\n" \
                   "..........................W   W.........\n" \
                   "..........................W   W.........\n" \
                   "..........................WWWWW.........\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Three Rooms Creation Failed.")
        with self.assertRaises(FloorPlanOverlapError):
            lb.add_hallway((26,3), (11,3))

    def test_hallways_overlap_invalid(self):
        lb = LevelBuilder().create_level(40, 16)\
                                .add_room((5,5), 7, 5, {(11, 7)})\
                                .add_room((26,6), 5, 8, {(26,7)})\
                                .add_hallway((26,7), (11,7))\
                                .add_room((14,1), 6, 4, {(17,4)})\
                                .add_room((14,9), 7, 4, {(17,9)})
        level = lb.build()
        actual = str(level)
        expected = "........................................\n" \
                   "..............WWWWWW....................\n" \
                   "..............W    W....................\n" \
                   "..............W    W....................\n" \
                   "..............WWWDWW....................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W..............WWWWW.........\n" \
                   ".....W     D--------------D   W.........\n" \
                   ".....W     W..............W   W.........\n" \
                   ".....WWWWWWW..WWWDWWW.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............WWWWWWW.....W   W.........\n" \
                   "..........................WWWWW.........\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Four Rooms with Hallway Creation Failed.")
        with self.assertRaises(FloorPlanOverlapError):
            lb.add_hallway((17,4), (17,9))

    def test_diagonal_hallway_invalid(self):
        lb = LevelBuilder().create_level(40, 16)\
                                .add_room((5,5), 7, 5, {(11, 7)})\
                                .add_room((26,6), 5, 8, {(26,7)})\
                                .add_room((14,1), 6, 4, {(17,4)})\
                                .add_room((14,9), 7, 4, {(17,9)})
        level = lb.build()
        actual = str(level)
        expected = "........................................\n" \
                   "..............WWWWWW....................\n" \
                   "..............W    W....................\n" \
                   "..............W    W....................\n" \
                   "..............WWWDWW....................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W..............WWWWW.........\n" \
                   ".....W     D..............D   W.........\n" \
                   ".....W     W..............W   W.........\n" \
                   ".....WWWWWWW..WWWDWWW.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............WWWWWWW.....W   W.........\n" \
                   "..........................WWWWW.........\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Four Rooms Creation Failed.")
        with self.assertRaises(InvalidHallwayError):
            lb.add_hallway((17,4), (26,7))
        with self.assertRaises(InvalidHallwayError):
            lb.add_hallway((17,4), (26,7), [(18,6)])
        with self.assertRaises(InvalidHallwayError):
            lb.add_hallway((17,4), (26,7), [(16,7)])
        lb.add_hallway((17,4), (26,7), [(17,7)])
        level = lb.build()
        actual = str(level)
        expected = "........................................\n" \
                   "..............WWWWWW....................\n" \
                   "..............W    W....................\n" \
                   "..............W    W....................\n" \
                   "..............WWWDWW....................\n" \
                   ".....WWWWWWW.....-......................\n" \
                   ".....W     W.....-........WWWWW.........\n" \
                   ".....W     D.....---------D   W.........\n" \
                   ".....W     W..............W   W.........\n" \
                   ".....WWWWWWW..WWWDWWW.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............WWWWWWW.....W   W.........\n" \
                   "..........................WWWWW.........\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Hallway with Waypoint Creation Failed.")

    def test_room_no_door_invalid(self):
        lb = LevelBuilder().create_level(20, 10)
        level = lb.build()
        with self.assertRaises(InvalidRoomError):
            lb.add_room((5,1), 7, 5, {})

    def test_find_available_room_simple(self):
        level = LevelBuilder().create_level(20, 10)\
                                .add_item("key", (8,4))\
                                .add_item("key", (10,2))\
                                .add_item("exit", (8, 2))\
                                .add_room((5,1), 7, 5, {(11,3)}).build()

        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Room Creation Failed.")
        actual_room = level.find_available_room((0, 0))
        actual_origin = actual_room.origin
        actual_width = actual_room.width
        actual_height = actual_room.height
        actual_doors = actual_room.doors

        self.assertEqual(actual_origin, (5, 1), "Unexpected origin.")
        self.assertEqual(actual_width, 7, "Unexpected width.")
        self.assertEqual(actual_height, 5, "Unexpected height.")
        self.assertEqual(actual_doors, {(11,3)}, "Unexpected doors.")

    def test_find_available_room_complex(self):
        level = LevelBuilder().create_level(40, 16)\
                                .add_room((5,5), 7, 5, {(11,7)})\
                                .add_room((26,6), 5, 8, {(26,7)})\
                                .add_room((14,1), 6, 4, {(17,4)})\
                                .add_room((14,9), 7, 4, {(17,9)})\
                                .build()
        actual = str(level)
        expected = "........................................\n" \
                   "..............WWWWWW....................\n" \
                   "..............W    W....................\n" \
                   "..............W    W....................\n" \
                   "..............WWWDWW....................\n" \
                   ".....WWWWWWW............................\n" \
                   ".....W     W..............WWWWW.........\n" \
                   ".....W     D..............D   W.........\n" \
                   ".....W     W..............W   W.........\n" \
                   ".....WWWWWWW..WWWDWWW.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............W     W.....W   W.........\n" \
                   "..............WWWWWWW.....W   W.........\n" \
                   "..........................WWWWW.........\n" \
                   "........................................\n" \
                   "........................................"
        self.assertEqual(actual, expected, "Room Creation Failed.")


    def test_remove_key(self):
        level = LevelBuilder().create_level(20, 10)\
                                .add_item("key", (8,4))\
                                .add_item("key", (10,2))\
                                .add_item("exit", (8, 2))\
                                .add_room((5,1), 7, 5, {(11,3)}).build()

        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        level.remove_item("key", (8, 4))
        self.assertEqual(actual, expected, "Room Creation Failed.")
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W     W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "First Key Removal Failed.")
        level.remove_item("key", (10, 2))
        self.assertEqual(actual, expected, "Room Creation Failed.")
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E  W........\n" \
                   ".....W     D........\n" \
                   ".....W     W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Second Key Removal Failed.")

    def test_remove_exit(self):
        level = LevelBuilder().create_level(20, 10)\
                                .add_item("key", (8,4))\
                                .add_item("key", (10,2))\
                                .add_item("exit", (8, 2))\
                                .add_room((5,1), 7, 5, {(11,3)}).build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        level.remove_item("exit", (8, 2))
        self.assertEqual(actual, expected, "Room Creation Failed.")
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W    KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        self.assertEqual(actual, expected, "Exit Removal Failed.")

    def test_remove_item_invalid_key(self):
        level = LevelBuilder().create_level(20, 10)\
                                .add_item("key", (8,4))\
                                .add_item("key", (10,2))\
                                .add_item("exit", (8, 2))\
                                .add_room((5,1), 7, 5, {(11,3)}).build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        with self.assertRaises(KeyError):
            level.remove_item("potions", (8, 2))

    def test_remove_item_invalid_location(self):
        level = LevelBuilder().create_level(20, 10)\
                                .add_item("key", (8,4))\
                                .add_item("key", (10,2))\
                                .add_item("exit", (8, 2))\
                                .add_room((5,1), 7, 5, {(11,3)}).build()
        actual = str(level)
        expected = "....................\n" \
                   ".....WWWWWWW........\n" \
                   ".....W  E KW........\n" \
                   ".....W     D........\n" \
                   ".....W  K  W........\n" \
                   ".....WWWWWWW........\n" \
                   "....................\n" \
                   "....................\n" \
                   "....................\n" \
                   "...................."
        with self.assertRaises(KeyError):
            level.remove_item("key", (9, 4))

if __name__ == '__main__':
    unittest.main()
