# Observer Design

## General Notes

In the previous assignment, we outlined communciation between the `PlayerClient` and the `GameManager` to go through a `GameProxy` class. Both the `PlayerClient` and `GameManager` are subclasses of `ProxyClient`. Those implementations are in `src/Game/controllers` and the files are `player_client.py`, `proxy_client.py` and `game_manager.py`.

The `Observer` will also be a `ProxyClient` that connects to the `GameProxy`.
The `GameProxy` will need an `__accept_observer` method similar to the `__accept_player` method it currently has. Currently, the `GameManager` updates the players after each player moves with their specefic state JSON. Now, `GameManager` will _also_ update the `Observer` after each player move. The `Observer` will get the global game state which has more information than the player state JSON.

This state will be created by the `GameState` similar to the `GameState.create_player_game_state` method.

## Observer Class
```python

class Observer(ProxyClient):

    def __init__(self, proxy: GameProxy, view: SnarlView):
        """
        Creates an Observer with a GameProxy.
        """
        super().__init__(proxy)

    def __accept_game_state(self, game_state: str):
        """
        1. Accepts a JSON-like game_state from the GameProxy
        2. Renders the game state
        """

    def __render_game_state(self, game_state: str):
        """
        Renders the game state to the observer.
        """

```

## Sequence Diagram

Similar to the Player in the diagram seen in `communication_overview` the `Observer` will receive the game state from the `GameManager`. Its interactions are even more simple than the player, as it does not need to communicate moves to the `GameManager`, it only accepts and renders the state.

```
   User                        Observer             GameProxy                     GameManager

    +                            +                      +                              +
    |                            |                      |                              |
    |                            |                      |<---connect_to_server---------+
    |                            |                      |                              |
    +---(create observer)------> +--connect_to_server-->|                              |
    |                            |                      |                              |
    |                            |                      |<-accept_messages_from_server-|
    |                            |                      |                              |
    |                            |                      |--(observer connect request)->|
    |                            |                      |                              |
    +<-----render_game_state---+ +<--accept_game_state--+<---send_observers_game_state-+
    |                            |                      |                              |
    +                            +                      +                              +
```

## UI Mockup

The `render_game_state` method will produce a screen or terminal output that looks something like what is seen below.
The `Observer` will see the Player, Adversary, and General Level information in a table, and then also a map of the level.

```
+--------------------------------------------------------------------+
|                                                                    |
|    +-----------------------------------------------------------+   |
|    |                                                           |   |
|    |                       Level Map                           |   |
|    |                                                           |   |
|    +-----------------------------------------------------------+   |
|                                                                    |
|    +-----------------+----------------------+------------------+   |
|    |                 |                      |                  |   |
|    |  Player Info    |  Adversary Info      |   General Info   |   |
|    |                 |                      |                  |   |
|    +-----------------------------------------------------------+   |
+--------------------------------------------------------------------+
```