from src.Game.models.states import GameState
import src.Game.constants as constants


class StateExporter:

    @staticmethod
    def create_observer_game_state(game_state) -> dict:
        """
        Used to create a JSON object to give to the Observer.
        """

        output_state = {
            "is_exit_unlocked": game_state.is_exit_unlocked,
            "is_game_over": game_state.is_game_over,
            "current_turn": game_state.current_turn,
            "level_count": len(game_state.levels),
            "current_level_number": game_state.current_level,
            "moves_elapsed": game_state.moves_elapsed,
            "latest_player_message": game_state.player_message,
            "level_map": str(game_state.current_level_object),
            "exited_players_count": sum(1 for x in game_state.players if x.has_exited),
            "dead_players_count": sum(1 for x in game_state.players if not x.is_alive)
        }

        if game_state.is_game_over:
            output_state = {**output_state, **StateExporter.create_end_game_state(game_state)}

        return output_state

    @staticmethod
    def create_adversary_game_state(state: GameState, adversary_id):
        """
        Creates the game state to give to the adversary
        """
        adversary = state.occupants[adversary_id]

        return {
            "type": constants.ADVERSARY_UPDATE_MESSAGE,
            "level_map": [list(x) for x in str(state.current_level_object).split("\n")],
            "available_moves": [x[::-1] for x in state.current_level_object.get_possible_moves(adversary)],
            "player_locations": [p.current_location[::-1] for p in state.players if p.is_active],
            "position": adversary.current_location[::-1]
        }

    @staticmethod
    def create_player_update(game_state: GameState, player_id: int):
        """
        Creates a player update state.
        """
        player = game_state.occupants[player_id]
        visible_tiles = game_state.current_level_object.crop(player.current_location, player.visible_distance)
        json_layout = [[t.get_numerical_representation() if t else constants.WALL_NUMBER for t in row] for row in visible_tiles]
        objects = []
        actors = []

        for row in visible_tiles:
            for tile in row:
                if tile:
                    if tile.current_occupant and tile.current_occupant != player:
                        actors.append({"type": tile.current_occupant.actor_type,
                                       "position": tile.location[::-1],
                                       "name": tile.current_occupant.id})
                    if tile.current_item:
                        objects.append({"type": tile.current_item.item_name,
                                        "position": tile.location[::-1]})

        return {
            "type": constants.UPDATE_MESSAGE,
            "layout": json_layout,
            "objects": objects,
            "actors": actors,
            "position": player.current_location[::-1],
            "message": "Current Turn: {}\n{}".format(
                        game_state.moves_elapsed, game_state.player_message),
            "health": player.health
        }

    @staticmethod
    def create_end_level_state(game_state: GameState, level_number):
        """
        Creates an end of level state with information on ejected players and object finders.
        """
        exits = []
        ejects = []
        key = None

        for p in game_state.players:
            if level_number in p.exits:
                exits.append(p.id)
            if level_number in p.ejections:
                ejects.append(p.id)
            if level_number in p.keys_found:
                key = p.id

        return {
            "type": constants.END_LEVEL_MESSAGE,
            "key": key,
            "exits": exits,
            "ejects": ejects,
        }

    @staticmethod
    def create_end_game_state(game_state: GameState):
        """
        Creates an end game state.
        """
        player_score_list = [{"type": constants.PLAYER_SCORE_MESSAGE,
                              "name": player.id,
                              "exits": len(player.exits),
                              "ejects": len(player.ejections),
                              "keys": len(player.keys_found)} for player in game_state.players]

        return {
                "type": constants.END_GAME_MESSAGE,
                "scores": player_score_list
            }
