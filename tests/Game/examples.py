from src.Game.models.states import GameState
from src.Game.models.occupants import Player, Zombie, Ghost
from src.Game.models.level.level_builder import LevelBuilder

def level_1():
    return LevelBuilder()\
        .create_level(40, 16)\
        .add_room((5, 1), 7, 5, {(11, 3)})\
        .add_room((18, 2), 5, 8, {(18, 3), (20, 9)})\
        .add_room((3, 10), 12, 5, {(14, 12)})\
        .add_hallway((18, 3), (11, 3))\
        .add_hallway((14, 12), (20, 9), [(20, 12)])\
        .add_item("key", (7, 12))\
        .add_item("exit", (7, 13))\
        .build()


def level_2():
    return LevelBuilder()\
        .create_level(40, 16)\
        .add_room((5, 1), 7, 5, {(11, 3)})\
        .add_room((18, 2), 5, 8, {(18, 3), (20, 9)})\
        .add_item("key", (19, 5))\
        .add_item("exit", (21, 5))\
        .build()


def create_basic_game_state() -> GameState:
    players = [Player("p1")]
    adversaries = [Zombie("a1")]

    game_state = GameState([level_1()], players, {0: adversaries})
    game_state.progress_to_next_level(False)
    return game_state

def create_basic_game_state_ghost() -> GameState:
    players = [Player("p1")]
    adversaries = [Ghost("a1")]

    game_state = GameState([level_1()], players, {0: adversaries})
    game_state.progress_to_next_level(False)
    return game_state


def create_two_level_game_state(num_players=3, two_levels=True) -> GameState:
    players = [Player("p"+str(i)) for i in range(num_players)]
    adversaries = [Zombie("a"+str(i)) for i in range(5)]
    levels = [level_1(), level_2()] if two_levels else [level_1()]

    game_state = GameState(levels, players, {0: adversaries, 1: []})
    game_state.progress_to_next_level(False)
    return game_state
