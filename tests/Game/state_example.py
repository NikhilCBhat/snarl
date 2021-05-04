"""
Just a small test/example of playing a game using the GameState
"""

import sys
sys.path.append('.')

from src.Game.models.states import GameState
from src.Game.models.level.level_examples import example_level
from src.Game.views.colorful_textual_view import ColorfulTextualView
from src.Game.models.occupants import Player, Zombie, Ghost

if __name__ == "__main__":
    view = ColorfulTextualView()
    players = [Player("p"+str(i)) for i in range(4)]
    adversaries = [Zombie("a"+str(i)) for i in range(5)] + [Ghost("g")]
    game_state = GameState([example_level], players, {0: adversaries})
    game_state.progress_to_next_level()

    moves = [("p1", (7, 3)), ("p2", (7, 12)), ("p2", (8, 12)),
                ("a2", (8, 12)), ("a2", (8, 11))]

    for player, move in moves:
        view.render_level_map(str(game_state.current_level_object))
        game_state.update(player, move)

    state_dict = game_state.to_dict()
    gs = GameState.from_state_dict(state_dict)
    view.render_level_map(str(gs.current_level_object))

    print(gs.current_level_object.to_json())