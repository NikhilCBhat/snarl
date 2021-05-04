# Adversary Planning

## Background
Currently, communication between the `User`, `Observer`, and `GameManager` go through a `GameProxy` class.
The `GameProxy` acts as a switchboard, routing JSON messages to different objects. These implementations can be seen in `src/Game/controllers/`, `src/Game/Common`, `src/Game/Player` and `src/Game/Observer`.

Messages between `ProxyClients` have the following format:
```
{   "to": message_recipient,
    "sender": self.id,
    "type": message_type (must be one of the fields in the MessageTypes enum),
    "body": JSON_object containing message info
}
```

As the `User`, `Observer`, and `GameManager` all connect to the `GameProxy` they are subclasses of `ProxyClient`. The `User` and `Observer` also inherit `OccupantClient`.

The `GameManager` has the following methods to deal with `Users` and `Observers`:
* Registering: `__accept_player` & `__accept_observer`
* Sending State: `_send_observers_game_state` & `_send_players_game_state`
    * Note: state comes from `GameState.create_player_game_state` and `GameState.create_observer_game_state`
* Playing Moves: `__accept_player_move`

## About the Adversary Client

The `AdversaryClient` will be very similar to the `User` and `Observer`. It will also be an `OccupantClient` that connects to the `GameProxy`.

In order to support the `AdversaryClient` the `GameManager` will need `__accept_adversary`,`__accept_adversary_move`, and `_send_adversaries_game_state` methods. Something to note is that the `_send_adversaries_game_state` method should only be sent when the adversary is about to play their turn.

Additionally, our `GameState` will need a `create_adversary_game_state` method.

## Adversary Client Class

```python

class AdversaryClient(OccupantClient):

    def __init__(self, proxy: GameProxy, id: str, adversary_type: str):
        """
        1. Creates an Adversary with the GameProxy.
        2. Calls self.connect_to_server to register itself with the GameManager.
        type: connection_request
        body: "ghost" | "zombie"
        """

    def accept_game_state(self, game_state: str):
        """
        1. Accepts a JSON-like game_state from the GameProxy
        2. If it is the adversary's turn, plays a move.
        """

    def __play_adversary_move(self, availible_moves):
        """
        1. Chooses the best move from the availible ones using its own 'AI' logic.
        2. Sends the move to the proxy
        type: "adversary_move",
        body: [int, int] # this is the new location they want to move to
        """
```

## Adversary Class

The internal representation for an `AdversaryClient` will be an `Adversary` object as seen below.
This is created by the `GameManger` when an `AdversaryClient` registers with the `GameManager`.

This code has been written much earlier and can be seen in the `src/Game/models/occupants.py` file.
`Ghost` and `Zombie` inherit `Adversary`. For convenience is duplicated below:

```python
class Adversary(Occupant):

    def __init__(self, id, non_traversable_tiles, move_distance, actor_type):
        super().__init__(id, non_traversable_tiles, move_distance, actor_type)
        self.has_exited = False

    def interact_with_occupant(self, occupant):
        occupant.interact_with_adversary(self)

    def interact_with_player(self, player):
        player.expel()

    def __str__(self):
        return constants.ADVERSARY_STRING
```

# Sequence Diagram
```
+----------------------------------------------------------------------------------------------------------------------------+
|     AdversaryClient                   GameManager                    GameState                            Adversary        |
|           +                                +                              +                                  |             |
|           |                                |                              |                                  |             |
|           +--connect_to_server------------>+                              |                                  |             |
|           |                                |                              |                                  |             |
| Setup     |                                +--create_game_state---------->+----(create Adversary object)--->+|             |
|           |                                |                              |                                  |             |
|           |                                +--get_adversary_game_state--->+                                  |             |
|           |<---send_adversary_game_state---+                              |                                  |             |
|           |                                |                              |                                  |             |
+----------------------------------------------------------------------------------------------------------------------------+
|           |                                |                              |                                  |             |
|           +---send_adversary_move--------> +---update_game_state--------->----update_adversary---------->+   |             |
|           |                                |                              |                                  |             |
|           |                                |                              |                                  |             |
|Processing +<--send_move_result-------------+ <---get_move_response--------+                                  |             |
|           |                                |                              |                                  |             |
|Note: this |                                |                              |                                  |             |
|will loop  +<---send_adversary_game_state---+                              |                                  |             |
|until game |                                |                              |                                  |             |
|is over    |                                |                              |                                  |             |
+-----------+--------------------------------+------------------------------+----------------------------------+-------------+
```