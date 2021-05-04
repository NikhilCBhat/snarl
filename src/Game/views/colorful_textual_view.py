import rich
from rich.text import Text
from rich.console import Console

# Local Imports
import src.Game.constants as constants
from src.Game.views.snarl_view import SnarlView
from src.Game.views.view_utils import clear, create_printable_list

TRUE_EMOJI = ":white_heavy_check_mark:"
FALSE_EMOJI = ":x:"

class ColorfulTextualView(SnarlView):

    __excluded_table_keys = {"level_map", "available_moves",
                            "is_game_over", "layout", "actors", "objects"}

    def render_observer_state(self, state_json):
        """
        Renders a complete state JSON
        """

        # Different rendering for level over
        if state_json["is_game_over"]:
            self.render_game_over(state_json)
            return

        # Print the level + state table
        self.render_level_map(state_json["level_map"])
        rich.print(self.__create_observer_table(state_json))

    @clear
    def render_level_map(self, level_string):
        """
        Renders a level map
        """

        # Print Header
        indent = level_string.find("\n") // 2 - 8
        rich.print(" "*indent + "+-----------+")
        rich.print(" "*indent + "| Level Map |")
        rich.print(" "*indent + "+-----------+")

        # Creates colorful level
        rich_text = Text(level_string)
        for tile_type, color in constants.tiles_to_colors.items():
            rich_text.highlight_words(tile_type, style="bold rgb({},{},{})".format(*color))

        # Prints the level
        console = Console()
        console.print(rich_text, "\n")

    def render_player_update(self, player_update):
        """
        Renders a player update state.
        """
        self.render_level_map('\n'.join("".join(row) for row in self.__create_layout(player_update)))

        rich.print("\n" + player_update["message"])
        rich.print("Current Position (row,col): " + str(player_update["position"]))
        rich.print("Current Health: " + str(player_update["health"]))

    def render_game_over(self, state_json):
        """
        Renders a game over message
        """
        table = self.__create_table("\nGame Over! Information below:")

        sorted_scores = sorted(state_json["scores"],
                        key=lambda p: (p["exits"], p["keys"]), reverse=True)

        table.add_row("Player Scores", "\n".join(
                    "Player {} -- Ejects: {} Exits: {} Keys Found: {} ".\
                    format(score["name"], score["ejects"], score["exits"], score["keys"])
                    for score in sorted_scores))

        rich.print(table)

    @clear
    def render_level_over(self, state_json):
        """
        Renders a level over state that looks like
        """
        table = self.__create_table("Level Over! Information below:")
        table.add_row("Key Finders", state_json["key"])
        table.add_row("Exit Finders", create_printable_list(state_json["exits"]))
        table.add_row("Ejected Players", create_printable_list(state_json["ejects"]))
        rich.print(table)

    def __create_table(self, table_title="Game Information"):
        table = rich.table.Table(title=table_title, show_lines=True)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="tan")
        return table

    def __create_observer_table(self, state_json):
        """
        1. Create the table with game info
        2. Fills it in the table
        """
        table = self.__create_table()

        for field, value in state_json.items():
            if isinstance(value, bool):
                value = TRUE_EMOJI if value else FALSE_EMOJI

            if field not in self.__excluded_table_keys:
                table.add_row(field, str(value))

        if "available_moves" in state_json:
            table.add_row("available_moves",
                create_printable_list(state_json["available_moves"]))

        return table

    def __create_layout(self, player_update):
        """
        Creates the layout from a player update
        """
        row_adjustment = 2 - player_update["position"][0]
        col_adjustment = 2 - player_update["position"][1]

        objects = [[o["position"], constants.NAME_TO_STRING[o["type"]]]\
                for o in player_update["objects"] + player_update["actors"]] + \
                [[player_update["position"], constants.PLAYER_STRING]]

        layout = [[constants.NUMBER_TO_LETTER[number] for number in row]\
                for row in player_update["layout"]]

        for (i,j), char in objects:
            layout[i + row_adjustment][j + col_adjustment] = char

        return layout