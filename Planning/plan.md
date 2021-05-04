# Milestone 1
## Part 1
**Pieces that make up a player and an automated adversary:** An `Occupant` can include: avatar, health points, attack points, isExpelled/isAlive flag, a current location, max movable distance, visible distance, and a list of items. `Player` and `Adversary` are subclasses of `Occupant` with different values for Occupant fields. For example, Adversaries can view the entire gameboard while Players have a limited visable distance.

**Pieces that make up the game software:** Game Software consists of a `GameServer` and a `GameClient.` A Server contains collections of `Levels` and `Occupants`. A `Level` consists of `TileConfigs`. `TileConfigs` may be `Rooms` or `Hallways`. `TileConfigs` contain `Tiles` which may hold `Items` that `Players` interact with. Some `Tiles` may be exits that allow `Players` to leave the `Room`, `Hallway`, or `Level`. A `Key` is an `Item` that allows `Players` to exit a `Level`. Users interact with `GameClient`. The client communicates with the server to send user actions and retreives game data to render.

**Common knowledge/Communication:** The game state is sent from the server to the client. State includes what the current room looks like as well as other player and game data that would be helpful for a user. When a user performs an action, the client forwards the action to the server, and the server returns an updated state. A player gets information about their surrounding tiles, their current level number, and whether the level exit is unlocked while adversaries gets information about the whole level. On the server-side, the user action updates the `Level` and `Player` objects based on a player's new position and any `Items`/`Adversaries` at that location. Once the players actions are completed, the adversaries move. After the adversaries' turns, the server evaluates the game state: the game ends, the players progress to the next level, or the players remain at the current level.  
## Part 2  
**Milestone 1: Foundation** 
Define interfaces and class stubs that are descriptive enough to be outsourced.

**Milestone 2: Background Components** 
Implement `GameServer` interface and setting/background components for Snarl. Background components may include `Level`, `Room`, `Tile`,  and `Item`. The background components create the areas where and things with which players and adversaries interact. The programmer should demo/print that the server maintains information on these background components.

**Milestone 3: Player & Adversary**
Implement Snarl actors: `Player` and `Adversary` interfaces. Add support for moves/interactions for actors. Allow support for multiple players.  The programmer should demo/print that interactions between `Players`, `Adversaries`, and the game via CLI or integration tests. 

**Milestone 4: Networking**
Build out infrastructure for the user to interact with the client, and then the client to interact with the server. The programmer should demo network-based interactions between a user, the client, and the server. 

**Milestone 5: UI** 
Choose UI framework. Develop client-side interface. The programmer should demo a polished user interface for interacting with the game.
_Note: Milestone 5 may take 2 weeks._ 

**Extra Milestones:** Level generation, smart adversaries, and other extra features are stretch goals that could be additional milestones after the above milestones are completed. 

