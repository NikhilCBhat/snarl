# Communication Overview

## About

We have decided to call the Milestone 4 player  `PlayerClient`
to disambiguate between the `Player` object (that is internal
to the `GameManager`) and the `PlayerClient` (that interacts with the user).

In order to not expose the internals of either the `PlayerClient`
or the `GameManager`, we are using the proxy pattern to have
an intermediary between the two.

`GameManager` and `PlayerClient` will connect to the `GameProxy` and
send and receive JSON-like strings in order to communicate.

## GameProxy Class
```python

class GameProxy

    def send_message(self, str: json_message):
        """
        Sends the message to a recipient.
        """

    def accept_message(self, str: json_message):
        """
        Accepts a message from a sender.
        """
```

## JSON Format

The JSON is sent/received in the following format.
The "sender" field will be the player/server id, and the "body" and "type" will
depend on the message. Look in `game-manager.md` or `player.md` for a description
of the body/type for various messages.

```
{
    "sender": player_id | game_manager_id,
    "type": message_type
    "body": json-like message to send
}
```

## ProxyClient

Both the `GameManager` and `PlayerClient` will connect to the `ProxyClient`.
As a result, they'll both inherit the following interface.

```python
class ProxyClient

    def __init__(self, GameProxy: proxy):
        """
        When a ProxyClient is created it will be given a GameProxy object
        that it will connect to when connect_to_server is called.

        When this is networked, the ProxyClient will instead take in
        the hostname & port of the proxy in order to connect to it via a
        network connection.
        """

    def send_message_to_server(self, str: json_message):
        """
        Sends a message to the server.
        When local this calls self.proxy.accept_message() and
        when networked this sends a message via a network connection.
        """

    def accept_message_from_server(self, str:json_message):
        """
        Accepts a message from the server.
        When local this calls self.proxy.send_message() and
        when networked this receives a message via a network connection.
        """

    def connect_to_server(self, client_id):
        """
        Sends a connect message to the server.
        {
            type: "connection_request",
            body: client_id
        }
        """
```


## Communication Diagram

Sequence Diagram of User/PlayerClient/GameManager connections.
Note, the `GameProxy` is the intermediary between the `PlayerClient` and `GameManager` and is ommitted from the diagram.

```
            User            PlayerClient                        GameManager

             +                   +                                    +
+---------------------------------------------------------------------+
|  Setup     |                   |                                    |
|            +-------------------(start manager)--------------------->+
|            |                   |                                    |
|            +--(start player)-->+                                    |
|            |                   |                                    |
|            <---get_player_name-+                                    |
|            |                   |                                    |
|            +-----(name)------->+--------accept_player-------------->+
|            |                   |                                    |
|            +----(start)------->+-------start_game----------------->+
|            |                   |                                    |
+---------------------------------------------------------------------+
|            |                   |                                    |
|            |                   +<-----send_players_game_state-------+
|            | accept_game_state |                                    |
| Processing +<---& render_state-+                                    |
|            |                   |                                    |
| note       | prompt_player_move|                                    |
| this       +<------------------+                                    |
| phase      |                   |                                    |
| repeats    |                   |                                    |
| until      +-----(move)------->+---------send_player_move---------->+
| game over  |                   |                                    |
+---------------------------------------------------------------------+
```
