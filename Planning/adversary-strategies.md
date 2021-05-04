# Adversary Strategies

## Strategies

### Zombie
As a Zombie is restricted to the room it is in, the main strategy for the Zombie is to "guard" items. If there are no items in its vicinity, it will select the tile closest to any player with its implementation of `select_move` from the `Adversary` interface.

From a list of moves its move distance, a Zombie uses `get_closes_move_to_player` from the `Adversary` class to select the destination that is closest to any player on the current level. Closeness is determined by Manhattan distance.

### Ghost
If a `Player` is in the same room as a `Ghost`, the `Ghost` selects the tile closest to any player in their room. This move selection uses the same method discussed above for a `Zombie`.

If there are no players in a ghost's current room, the `select_move` function will select a wall tile for a move. When `GameState.update()` is called, an `Adversary` of the `Ghost` type that marks a wall tile as its destination, will be teleported.
Teleporting places the `Ghost` in a blank, non-wall tile within a `Room` of the current level.

## Example Scenarios
1. ***Adversary in Room With Players***
When an adversary shares a room with a player, it will select the move from
its moveable distance that is closest to a player on the current level. `test_adversary_select_move_closer_player()` in `Snarl/tests/Game/test_occupants` demonstrates/tests this basic strategy for both `Ghost` and `Zombie` types.


2. ***Ghost in Room Without Players***
When a `Ghost` is in a room without players, it will teleport to a random, blank, non-wall tile within the current level. This is demonstrated in `test_ghost_teleports_to_closest_wall()` in `Snarl/tests/Game/test_occupants`. `g1` selects a wall as a destination. Then, `GameState.update()` teleports the ghost to a random location.


3. ***Zombie in Room Without Players***
In a room without players, a `Zombie` will take on defensive strategy of guarding items such as keys and exits. Hovering around items makes it harder for a player to acquire them. This behavior is tested in `test_zombie_guards_items()` in `Snarl/tests/Game/test_occupants`.

