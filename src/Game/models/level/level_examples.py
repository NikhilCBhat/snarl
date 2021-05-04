from src.Game.models.level.level_builder import LevelBuilder

example_level = LevelBuilder()\
                    .create_level(40,16)\
                    .add_room((5,1), 7, 5, {(11,3)})\
                    .add_room((18,2), 5, 8, {(18,3), (20,9)})\
                    .add_room((3,10), 12, 5, {(14,12)})\
                    .add_hallway((18,3), (11,3))\
                    .add_hallway((14,12), (20,9), [(20,12)])\
                    .add_item("key", (6,4))\
                    .add_item("exit", (7,4))\
                    .build()

simple_level = LevelBuilder()\
                    .create_level(20,8)\
                    .add_room((1,1), 3, 5, {(3,4)})\
                    .add_room((6,1), 7, 6, {(6,4)})\
                    .add_hallway((3,4), (6,4))\
                    .add_item("key", (10,2))\
                    .add_item("exit", (8,4))\
                    .build()
