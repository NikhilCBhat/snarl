import src.Game.constants as constants
import src.Game.snarl_errors as errors

class RuleChecker:

    @staticmethod
    def is_game_over(game_state):
        """
        Examines the fields of a game state to identify if the game is over.
        The game is over when the last level is completed or all the players have died.
        """
        return all(not p.is_alive for p in game_state.players) or \
            RuleChecker.is_level_over(game_state) and game_state.current_level == len(game_state.levels) - 1

    @staticmethod
    def is_level_over(game_state):
        """
        Examines the fields of a game state to identify if the level is over.
        The level is over if every player has either died or exited.
        """
        return all(not p.is_alive or p.has_exited for p in game_state.players)

    @staticmethod
    def get_game_winner(game_state):
        """
        Identifies who won the game
        Precondition: Game is over.
        """
        return constants.PLAYER_STRING if any(p.is_alive for p in game_state.players) else constants.ADVERSARY_STRING

    @staticmethod
    def validate_game_state(current_game_state):
        """
        Determines whether the current game state is valid.
        """
        if not current_game_state.levels:
            raise errors.InvalidLevelCountError

        if not (-1 <= current_game_state.current_level < len(current_game_state.levels)):
            raise errors.InvalidCurrentLevelError

        if current_game_state.current_turn not in current_game_state.occupants:
            raise errors.InvalidOccupantIdError

        if set(current_game_state.occupant_order) != set(current_game_state.occupants.keys()):
            raise errors.OccupantMismatchError

        if not (constants.MIN_PLAYERS <= len(current_game_state.players) <= constants.MAX_PLAYERS):
            raise errors.InvalidPlayerCountError

    @staticmethod
    def validate_move(current_game_state, occupant_id, new_location):
        """
        Determines whether an occupant move is valid.
        """

        # General state checks
        RuleChecker.validate_game_state(current_game_state)

        if current_game_state.is_game_over:
            raise errors.GameAlreadyOverError

        if occupant_id not in current_game_state.occupants:
            raise errors.InvalidOccupantIdError

        if occupant_id != current_game_state.current_turn:
            raise errors.InvalidOccupantTurnOrder

        # Check to see if new_location is within reach & traversable
        occupant = current_game_state.occupants[occupant_id]
        level = current_game_state.current_level_object
        new_location = tuple(new_location)
        allowed_moves = set(level.get_possible_moves(occupant))

        if str(level.get_tile(*new_location, False)) in occupant.tiles_to_filter_out\
            and new_location != occupant.current_location:
            raise errors.NonTraversableTileError

        if new_location not in allowed_moves:
            raise errors.InvalidDestinationError

