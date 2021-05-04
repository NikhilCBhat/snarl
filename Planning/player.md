# Player Client

## Note
Read `communication_overview.md` first.

The "body" and "type" fields of the JSON format mentioned
in `communication_overview.md` are detailed in the
comments underneath each relevant function.
The `sender` field will be the player name.

## PlayerClient Class
```python
class PlayerClient(ProxyClient):

    def __init__(self, GameProxy: proxy):
        """
        Creates a PlayerClient with a GameProxy.
        """
        super().__init__(proxy)

    def get_player_name(self):
        """
        1. Prompts the user for their name.
        2. Calls connect_to_server(player_name)
        3. The server should then send message to the GameManager
        notifying them of the new player.
        """

    def __render_game_state(self, List[List[str]]: level_map):
        """
        Renders the level map to the user.
        """

    def start_game(self):
        """
        1. Prompts the player whether they want to start game (in a loop)
        2. When the player says yes, sends a start_game message to the server.
        {
            type: "start_game",
            body: player_name
        }
        """

    def send_player_move(self):
        """
        1. Prompts the player for their move
        2. Sends the move to the proxy
        {
            type: "player_move",
            body: [int, int] # this is the new location they want to move to
        }
        """

    def accept_game_state(self, str: game_state):
        """
        1. Accepts a JSON-like game_state from the GameProxy
        2. Renders the level map
        """

```

