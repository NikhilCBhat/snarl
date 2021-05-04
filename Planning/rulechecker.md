# Rule Checker

```python

class RuleChecker:

    def is_game_over(GameState: game_state) -> bool:
        """
        Examines the fields of a game state to identify if the game is over.
        """
        pass

    def is_level_over(GameState: game_state) -> bool:
        """
        Examines the fields of a game state to identify if the level is over.
        """
        pass

    def validate_game_state(GameState: current_game_state) -> bool:
        """
        Determines whether the current game state is valid.
        """
        pass

    def validate_move(Game: current_game_state, int: occupant_id, Tuple[int, int] new_location) -> bool:
        """
        Determines whether an occupant move is valid, by seeing whether their new_location is within reach.

        Most likely will call the _bfs() helper method.
        """
        pass

    def __bfs(GameState: current_game_state, Tuple[int, int] starting_location, Set[str] traversable_tile_types, int: movable_distance) -> Set[Tuple[int, int]]:
        """
        Optional helper method to implement:

        Does a breadth first search for movable_distance number of tiles within the current_game_state.

        note: movable_distance is the number of cardinal moves that an occupant can travel

        note: traversable_types is a set with the strings tha this occupant can walk on. Currently this would just be {" ", "K", "E", "A", "="} for players & {" ", "K", "E", "A", "=", "P"} for adversaries but in the future it could be {"W", "A", "K", "E", "=", " ", "P"} for ghosts.

        Returns a set of valid moves.

        For our implementation, we can just call:
        current_game_state.current_level_object.get_adjacent_tiles(
            starting_location, movable_distance, traversable_tile_types)
        """
        pass

```