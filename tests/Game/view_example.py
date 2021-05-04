import sys
sys.path.append('.')

from src.Game.models.state_exporter import StateExporter
from src.Game.views.colorful_textual_view import ColorfulTextualView
from tests.Game.examples import create_two_level_game_state

view = ColorfulTextualView()
state = create_two_level_game_state()

def observer_view():
    view.render_observer_state(StateExporter.create_observer_game_state(state))

def player_update():
    view.render_player_update(StateExporter.create_player_update(state, "p0"))

def adversary_update():
    update = StateExporter.create_adversary_game_state(state, "a0")
    print(update)

def end_level():
    view.render_level_over(StateExporter.create_end_level_state(state, 0))

def end_game():
    view.render_game_over(StateExporter.create_end_game_state(state))

def end_level_example():
    sample_end_level = { "type": "end-level",
        "key": "dio", "exits": ["nikhil", "ferd"], "ejects": ["karmen", "andy"]
    }
    view.render_level_over(sample_end_level)

def end_game_example():
    ps_1 = { "type": "player-score",
        "name": "ferd",
        "exits": 2,
        "ejects": 0,
        "keys": 1
    }
    ps_2 = { "type": "player-score",
        "name": "dio",
        "exits": 3,
        "ejects": 5,
        "keys": 2
    }
    ps_3 = { "type": "player-score",
        "name": "nikhil",
        "exits": 5,
        "ejects": 2,
        "keys": 1
    }
    sample_end_game = { "type": "end-game",
        "scores": [ps_1, ps_2, ps_3]
    }

    view.render_game_over(sample_end_game)

if __name__ == "__main__":
    # Comment out the ones you don't want to try out
    observer_view()
    # player_update()
    # adversary_update()
    # end_level()
    # end_game()
    # end_level_example()
    # end_game_example()
