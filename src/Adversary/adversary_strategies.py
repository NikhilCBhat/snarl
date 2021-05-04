import random
from abc import abstractstaticmethod
import src.Game.constants as constants

def manhattan_distance(p1, p2):
    """
    Calculates the manhattan distance between two points
    """
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def get_closest_point(source, other_points):
    """
    Gets the point in other_points closest to the source
    """
    return min(other_points, key=lambda point: manhattan_distance(source, point))

class AdversaryStrategy:
    """
    AdversaryStrategy has the 'AI' logic for adversary movements.
    """

    @abstractstaticmethod
    def calculate_move(possible_moves, current_location, level_map, player_locations):
        """
        Calculates the best move given the above information.
        """
        pass

class StrategyFactory:

    @staticmethod
    def get_strategy(strategy_name) -> AdversaryStrategy:
        """
        Gets the strategy for the given adversary type
        """
        strategies = {
            constants.GHOST_ACTOR_TYPE: GhostStrategy,
            constants.ZOMBIE_ACTOR_TYPE: ZombieStrategy,
            constants.STAY_IN_PLACE_STRATEGY: StayinPlaceStrategy
        }

        return strategies.get(strategy_name, RandomStrategy)

class RandomStrategy(AdversaryStrategy):

    def calculate_move(possible_moves, current_location, level, player_locations):
        """
        Randomly chooses a move.
        """
        return random.choice(possible_moves)

class StayinPlaceStrategy(AdversaryStrategy):

    def calculate_move(possible_moves, current_location, level, player_locations):
        """
        Always stays in place
        """
        return current_location

class MovetoPlayerStrategy(AdversaryStrategy):

    def calculate_move(possible_moves, current_location, level, player_locations):
        """
        Gets the move closest to any player.
        """
        selected_move = get_closest_point(
            MovetoPlayerStrategy.closest_player(current_location, player_locations),
            possible_moves)

        if selected_move == current_location and len(possible_moves) > 1:
            return [x for x in possible_moves if x != current_location][0]

        return selected_move

    @staticmethod
    def closest_player(current_location, player_locations):
        return get_closest_point(current_location, player_locations)

class GhostStrategy(AdversaryStrategy):

    def calculate_move(possible_moves, current_location, level, player_locations):
        """
        If the Ghost is far away from a player,
        it will try to move onto a wall, to teleport onto them.
        Otherwise, the ghost will move to the player.
        """
        closest_move_to_player = MovetoPlayerStrategy.calculate_move(
            possible_moves, current_location, level, player_locations)

        if manhattan_distance(closest_move_to_player,
            MovetoPlayerStrategy.closest_player(current_location, player_locations)) > 3:
            for i,j in possible_moves:
                if level[i][j] == constants.WALL_STRING:
                    return (i,j)

        return closest_move_to_player

class ZombieStrategy(AdversaryStrategy):

    def calculate_move(possible_moves, current_location, level, player_locations):
        """
        As a Zombie is restricted to the room it is in,
        the main strategy for the Zombie is to "guard" items.
        If there are no items in its vicinity, it will select
        the tile closest to any player.
        """

        # guard items
        for i, j in possible_moves:
            if level[i][j] in {constants.KEY_STRING, constants.EXIT_STRING}:
                return (i,j)

        # otherwise get closer to a player
        return MovetoPlayerStrategy.calculate_move(possible_moves,
            current_location, level, player_locations)
