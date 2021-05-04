## Note
Read `communication_overview.md` first.

The "body" and "type" fields of the JSON format mentioned
in `communication_overview.md` are detailed in the
comments underneath each relevant function.
The `sender` field will be "server".

## GameManager Class
``` python
class GameManager(ProxyClient):

    def __init__(self, GameProxy: proxy, List[Level]: levels):
        """
        1. Creates a Game Manager with a list of levels and a GameProxy
            Note: While the assignment states the manager only needs 'a single level',
            we use a list to provide more flexibility if this changes to multiple
            levels in the future.
        2. Connects to the server.
        """
        super().__init(proxy)

    def accept_player(self, PlayerClient: player):
        """
        1. Receives a message from the GameProxy with the new player.
        This message will be sent by the GameProxy after a player
        connects to the server with the format
        {
            type: "occupant_creation"
            body: "player_name"
        }

        2. Creates and store an internal representation of a player
        corresponding the provided player name.

        3. Responds:
        {
            type: "occupant_creation",
            body: bool # true or false depending on whether player was successfully created
        }
        """

    def start_game(self):
        """
        Starts the game with the accepted players
        """

    def send_players_game_state(self):
        """
        Updates all players with the current game state.
        {
            type: "game_state",
            body: (see below)
        }

        The sent game state will be a JSON containing information about
        - the current_player_id
        - the visible tiles that they can see
        - their location, health,
        - whether or not the exit is unlocked
        - actions they can take (empty list if its not their turn)
        """

    def accept_player_move(self):
        """
        1. Receive actions from player_name in the format outlined
        in PlayerClient.send_player_move. The action is a tuple
        indicating the desired position of the player.

        2. Updates the GameState based on the player action.

        3. Responds:
        {
            type: "player_move",
            body: bool # true or false depending on whether player was successfully moved
        }
        """
```