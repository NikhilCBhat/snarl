# Memorandum

To: Professor Ferd
From: Nikhil Bhat and Karmen Lu
Subject: Game States

Our game is handled by a `GameServer` which contains a `GameState`. The `GameState` has the following fields:
- self.players: Dict[int, Player] A dictionary of player_id to Player objects
- self.adversaries: Dict[int, Adversary] A dictionary of adversary_id to Adversary objects
- self.levels: List[Levels]
- self.current_level: int The current level
- self.current_player: int The player id of the current player
- self.current_adversary: int The adversary id of the current adversary
- self.game_phase: str Indicates what phase of the game we are in. Currently thinking about having this as "player_turn" or "adversary_turn" to indicate whether the players or adversaries are currently playing but this can change as we get more information.
- self.is_exit_unlocked: bool Whether or not the exit is unlocked.
The `GameServer` is responsible for updating the `GameState` fields after `Occupant` actions.

An `Occupant` has health points, attack points, isExpelled/isAlive flag, a current location, max movable distance, visible distance, current level, and a list of items.

A `Level` has a 2D array of `Tile`s. Each `Tile` has information about which `Room` or `Hallway` it belongs to, its location, items, whether it is a door or wall, and current occupants.

The `GameState` has the following methods to produce JSON-like strings to give to the Player or Adversary:
- `get_player_game_state(int: player_id) -> String`
- `get_adversary_game_state(int: adversary_id) -> String`.

Both JSONs will contain the following keys:
- occupant_id, and int describing their gameID
- current_level, an int describing the level number
- level_count, an int describing the number of levels
- is_exit_unlocked, a bool saying whether the players can leave the level
- current_location, a list of 2 ints, which is the current coordinate
- level_map, a 2D array of strings representing the *visible* area that the player/adversary can see. This is much larger for an adversary than a player. The strings are: W (wall), D (door), - (Hallway), . (not assigned), K (key), E (exit), " " (walkable space inside a room)
- possible_moves, a list of pairs of ints, which are the possible locations the player/adversary can move to.
- attack_points, an int representing how much damage they do.
- items, a list of strings describing their inventory.
- health, an int describing their current health. If health is 0 they are dead

The Adversary JSON will also have the following additional information:
- player_locations, a dictionary of player_id : Tuple(int, int), which are the locations of all players
- adversary_locations, a dictionary of adversary_id : Tuple(int, int), which are the locations of all adversaries
- player items, a dictionary of player_id : List[String], which is the inventory for each player
- game_items, a dictionary of object names to a list of locations
(ex: {"keys":[(1, 3), (3, 7)], "exits":[(50,100)]})

Other methods a `GameState` *may* have are:
- Private methods `__get_possible_player_moves(int: player_id) -> List[Tuple(int, int)]` to get the valid moves for a given player and likewise `__get_possible_adversary_moves` to do the same for adversaries.
- While a `GameServer` will directly update the fields listed above, the `GameServer` can enforce validity checks on the fields via the python @property and @.setter decorators. This might be helpful for doing validation on player turn changes.