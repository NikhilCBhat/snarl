# Remote Adversary

## Backward Compatibility

The previous Snarl protocol can be followed without any modification. A human can start the `snarlServer` and `snarlClient` executables and play the game exactly as before. As before, the `GameManager` will populate the game with local adversaries.

## Usage

### Updated Executable Arguments

The following **optional** arguments were added to `./snarlClient`.
* `--type`: Default to `player`, this field can also be `zombie` or `ghost`.
* `--level`: Default to `0`, this field can be any integer. It indicates the level the adversary inhabits.

### Playing the Game

Run `./snarlServer` to start the server and `./snarlClient` for each player. See `net/README.md` for details on either of those.

After the players connect, wait for the `./snarlServer` to print, "Waiting for adversaries..."

During this phase, run `./snarlClient` with the `--type` argument set to either `zombie` or `ghost` in order to create remote adversaries.

## Protocol

The goal was to mimic the player protocol as much as possible for the adversary.

### Registration
As mentioned above, adversaries connect after the players are done connecting. When they connect, they are also sent (server-welcome) and "name" messages. Just like the player, they also send back a name as a JSON string.

Unlike players, in addition to "name", adversaries are also prompted for their level when they receive a "adversary-level" message and type when they receive a "adversary-type" message. Adversaries must respond an integer for the level, and either the string "ghost" or "zombie" for the type.

After the timeout is over, the level starts.

### Level Gameplay
Just like a player, adversaries are sent updates. Their updates are in the following format:

```
{
    "type": adversary-update,
    "level_map": (level-map),
    "available_moves": [(point), (point), ...], # moves the adversary can make
    "current_location": (point),
    "player_locations": [(point), (point), ...], # locations of the players
    "position": (point)
}

A level map is a 2D array of strings providing a map of the level. The strings are as follows:
WALL_STRING = "W"
DOOR_STRING = "D"
HALLWAY_STRING = "-"
VOID_STRING = "."
PLAYER_STRING = "P"
WALKABLE_STRING = " "
KEY_STRING = "K"
EXIT_STRING = "E"
GHOST_STRING = "G"
ZOMBIE_STRING = "Z"
```

When it is their turn, adversaries are sent a "move" message, and they must sent back their move just like a player, in the following format:

```
{ "type": "move",
  "to": (maybe-point)
}
```

Note: Adversaries are only sent move & update messages when it is their level.

Just like players, adversaries get end-level and end-game messages as follows:

```
{ "type": "end-level",
  "key": (name),
  "exits": (name-list),
  "ejects": (name-list)
}

{ "type": "end-game",
  "scores": (player-score-list)
}
```

## Implementation

### Supporting Changes
In order to support remote adversaries I had to make a couple changes to my existing code.

The largest change I made was moving the Adversary AI logic from the internal adversary representation, to the external adversary client. This meant, that I had to send over the relevant information to the adversary as a JSON object. This information is what is seen in the adversary-update message above.

I updated the `StateExporter` to support creating this message. I also had to update the `LocalAdversary` to support receiving this message.

While making that change, I created an `AdversaryStrategy` interface, and corresponding implementations, and a factory. This allowed me to consolidate my code.

I also added two classes to allow me to easily create a `RemoteAdversary`:
* a `RemoteOccupant` class inherited by `RemotePlayer` and `RemoteAdversary`
* a `SnarlClient` class inherited by `SnarlPlayerClient` and `SnarlAdversaryClient`

### Remote Adversary

Once the above changes were made, supporting a remote adversary was very straightforward.
The `RemoteAdversary` class only has two method, one to provide the type of the adversary, and the other to provide the level. These are both achieved by sending the correct message, and parsing the resulting response.
