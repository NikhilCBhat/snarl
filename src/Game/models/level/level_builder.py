import json
import functools
from typing import List

from src.Game.models.level.level import Level
from src.Game.models.level.items import item_name_to_object
import src.Game.constants as constants
from src.Game.snarl_errors import InvalidHallwayError, InvalidDoorError
from src.Game.models.level.floor_plans import Room, Hallway

class LevelBuilder:

    def create_level(self, num_columns, num_rows):
        """
        Creates an empty level of a given size
        """
        self.level = Level(num_columns, num_rows)
        return self

    def add_item(self, item_name, item_location):
        """
        Adds an item to the level
        """
        new_item = item_name_to_object[item_name]()
        self.level.items[item_name][item_location] = new_item
        self.level.get_tile(*item_location, row_column=False).current_item = new_item

        return self

    def add_room(self, origin, width, height, doors, room_layout=[]):
        """
        Adds the tiles spanned by the origin, and the given width/height to a Room.
        If layout is specefied then adds those walls.
        """
        origin = tuple(origin)
        destination = [origin[i]+v-1 for i,v in enumerate([width, height])]
        room_tiles = self.__tiles_between(origin, destination, create_walls=(not room_layout), layout=room_layout)
        self.level.room_origins_to_room[origin] = Room(origin, width, height, doors, room_tiles)

        return self

    def add_hallway(self, source, destination, waypoints=[]):
        """
        Adds the tiles between the source, destination, and waypoints to a Hallway.
        """

        source = tuple(source)
        destination = tuple(destination)

        # Halways have to connect two doors
        endpoints = self.__validate_hallway_endpoints(source, destination)

        # Get the hallway tiles
        hallway_tiles = self.__get_hallway_tiles(source, destination, waypoints)

        # Create the hallway
        self.level.hallways.append(Hallway(hallway_tiles, waypoints, endpoints))

        return self

    def add_item_from_json(self, item_json):
        """
        Adds an item using JSON format
        """
        item_name = item_json["type"]
        item_location = tuple(item_json["position"])

        return self.add_item(item_name, item_location)

    def add_room_from_json(self, room_json):
        """
        Adds a room using JSON format
        """
        origin = room_json["origin"]
        width = room_json["bounds"]["columns"]
        height = room_json["bounds"]["rows"]
        layout = room_json["layout"]

        return self.add_room(origin, width, height, [], layout)

    def add_hallway_from_json(self, hallway_json):
        """
        Adds a hallway using JSON format
        """
        from_ = hallway_json["from"]
        to = hallway_json["to"]
        waypoints = hallway_json["waypoints"]

        return self.add_hallway(from_, to, waypoints)

    def build(self) -> Level:
        """
        Builds the level
        """
        return self.level

    def create_level_from_json(self, json_level) -> Level:
        level_builder = LevelBuilder().create_level(*self.__get_level_dimensions(json_level))
        functools.reduce(lambda lb, r: lb.add_room_from_json(r), json_level["rooms"], level_builder)
        functools.reduce(lambda lb, h: lb.add_hallway_from_json(h), json_level.get("hallways", []), level_builder)
        functools.reduce(lambda lb, i: lb.add_item_from_json(i), json_level["objects"], level_builder)

        level = level_builder.build()
        return level

    @staticmethod
    def create_levels_from_levels_file(level_file) -> List[Level]:
        with open(level_file) as f:
            string_input = f.read()

        end_index = 0
        jsons = []
        decoder = json.JSONDecoder()

        while string_input and len(string_input) > end_index:
            string_input = string_input[end_index:].strip()
            valid_json, end_index = decoder.raw_decode(string_input)
            jsons.append(valid_json)

        return [LevelBuilder().create_level_from_json(swap_level(level)) for level in jsons[1:]]


    def __get_level_dimensions(self, json_level):
        """
        Gets the size of a level based off of the room locations
        """
        bottom_right_corners = [
            [room["origin"][1] + room["bounds"]["rows"],
            room["origin"][0] + room["bounds"]["columns"]]
            for room in json_level["rooms"]
        ]

        for hallway in json_level.get("hallways", []):
            bottom_right_corners.extend([x[::-1] for x in hallway["waypoints"]])

        num_rows = max(x[0] for x in bottom_right_corners)
        num_columns = max([x[1] for x in bottom_right_corners])
        return num_columns + 1, num_rows + 1

    def __validate_hallway_endpoints(self, source, destination):
        """
        Validates that a hallway's endpoints end in doors.
        """
        endpoints = []
        for endpoint in (source, destination):
            endpoint = self.level.get_tile(*endpoint, row_column=False)
            endpoints.append(endpoint)
            if not endpoint.is_door:
                raise InvalidHallwayError

        return endpoints

    def __get_hallway_tiles(self, source, destination, waypoints):
        """
        Gets the tiles encompassed by a hallway
        """
        waypoints = [source] + waypoints + [destination]
        hallway_tiles = []
        for i, d in enumerate(waypoints):
            if i:
                s = waypoints[i-1]
                tiles_along_path = self.__tiles_between(s, d, validate_hallway=True)
                for tile in tiles_along_path:
                    if tile.location not in {source, destination}:
                        if tile.is_door:
                            raise InvalidDoorError
                        hallway_tiles.append(tile)
        return hallway_tiles

    def __tiles_between(self, source, destination, create_walls=False, validate_hallway=False, layout=[]):
        """
        Given two (x,y) coordinates returns the tiles between them.
        If `create_walls` is true, then it also marks edge tiles as walls.
        If `validate_hallway` is true, then ensures waypoints are orthogonal.
        If `layout` is provided, uses that to create walls.
        """
        source_y, source_x = source
        dest_y, dest_x = destination

        left = min(source_x, dest_x)
        top = min(source_y, dest_y)

        right = max(source_x, dest_x) + 1
        bot = max(source_y, dest_y) + 1

        tiles = []

        if validate_hallway and abs(left - right)  > 1 and abs(top - bot) > 1:
            raise InvalidHallwayError

        for i in range(left, right):
            for j in range(top, bot):
                tile = self.level.get_tile(i, j)
                if create_walls and (i == left or j == top or i == right -1 or j == bot - 1):
                    tile.is_wall = True
                if layout:
                    layout_tile = layout[i-left][j-top]
                    tile.is_wall = layout_tile in {constants.WALL_NUMBER, constants.DOOR_NUMBER}
                    tile.is_door = layout_tile == constants.DOOR_NUMBER

                tiles.append(tile)

        return tiles


def swap_level(json_level):
    """
    Swaps the coordinates in the json level representation
    """

    for room in json_level["rooms"]:
        room["origin"] = room["origin"][::-1]

    for item in json_level.get("objects", []):
        item["position"] = item["position"][::-1]

    for hallway in json_level.get("hallways", []):
        hallway["from"] = hallway["from"][::-1]
        hallway["to"] = hallway["to"][::-1]
        hallway["waypoints"] = [x[::-1] for x in hallway["waypoints"]]

    return json_level