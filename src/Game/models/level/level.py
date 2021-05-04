import json

# Local imports
from src.Game.models.level.tile import Tile
import src.Game.constants as constants

class Level:
    """
    A Level holds a 2D grid of tiles which may belong to rooms and hallways.
    An example level can be found in this file & more examples can be seen in
    test_level.py
    """

    def __init__(self, num_columns, num_rows):
        # Creates tiles
        self.tiles = [[Tile(x,y) for x in range(num_columns)] for y in range(num_rows)]

        # Empty collections for rooms, hallways, items
        self.room_origins_to_room = {}
        self.hallways = []
        self.items = {constants.KEY_NAME:{}, constants.EXIT_NAME:{}}

    def __str__(self):
        """
        A string representation of a level.
        """
        return "\n".join("".join(str(tile) for tile in row) for row in self.tiles)

    @property
    def json_item_locations(self):
        json_locations = []
        for item_name, locations in self.items.items():
            for location in locations:
                json_locations.append({"type": item_name, "position": location[::-1]})

        return json_locations

    @property
    def num_rows(self):
        return len(self.tiles)

    @property
    def num_cols(self):
        return len(self.tiles[0])

    def get_possible_moves(self, occupant):
        """
        Returns the list of locations an occupant can move to.
        """
        moves = [occupant.current_location]

        if occupant.is_active:
            moves.extend(self.get_adjacent_tiles(occupant.current_location,
                                    occupant.move_distance,
                                    non_traversable_tiles=occupant.non_traversable_tiles,
                                    tiles_to_filter_out=occupant.tiles_to_filter_out,
                                    tiles_in_same_room=occupant.actor_type == constants.ZOMBIE_ACTOR_TYPE,
                                    remove_doors=occupant.actor_type == constants.ZOMBIE_ACTOR_TYPE))

        return moves

    def get_adjacent_tiles(self, origin, num_moves,
                                non_traversable_tiles={constants.WALL_STRING,
                                                        constants.VOID_STRING},
                                tiles_in_same_room=False,
                                tiles_to_filter_out={},
                                remove_doors=False):
        """
        Gets the locations of tiles adjacent to the origin, reachable in num_moves.
        """
        fringe = self.__get_neighbors(origin, non_traversable_tiles, tiles_in_same_room)
        adjacent_tiles = []
        visited = set()

        for _ in range(num_moves):
            old_fringe = [x for x in fringe if x not in visited]
            fringe = []
            for loc in old_fringe:
                visited.add(loc)
                adjacent_tiles.append(loc)
                fringe.extend(self.__get_neighbors(loc, non_traversable_tiles, tiles_in_same_room))

        return [t for t in adjacent_tiles if \
            str(self.get_tile(*t, False)) not in tiles_to_filter_out and \
            (not remove_doors or not self.get_tile(*t, False).is_door)]

    def __get_neighbors(self, origin, non_traversable_tiles, tiles_in_same_room, include_diagonals=False):
        """
        Gets locations of neighboring tiles from the origin.
        """
        def is_valid_neighbor(loc):
            try:
                tile = self.get_tile(*loc, False)
            except IndexError:
                return False

            return (str(tile) not in non_traversable_tiles) and\
                   (not tiles_in_same_room or tile.parent == self.get_tile(*origin, False).parent)

        i, j = origin
        possible_neighbors = [(i, j-1), (i-1, j), (i+1, j), (i, j+1)]
        if include_diagonals:
            possible_neighbors.extend([(i+1, j+1), (i-1, j+1), (i+1, j-1), (i-1, j-1)])

        return [x for x in possible_neighbors if is_valid_neighbor(x)]

    def get_tile(self, i, j, row_column=True):
        """
        Helper function to get the Tile at a location.
        """
        if row_column:
            return self.tiles[i][j]
        return self.tiles[j][i]


    def crop(self, center, visible_distance):
        """
        Returns the 2D layout of tiles that are visible_distance away from the center tile location.
        """
        x, y = center
        def safe_get_tile(i,j):
            if i < 0 or j < 0:
                return None
            try:
                return self.get_tile(i,j)
            except:
                return None

        return [[safe_get_tile(i, j) for j in range(x-visible_distance, x+visible_distance+1)] for i in range(y-visible_distance, y+visible_distance+1)]

    def find_available_room(self, origin):
        """
        Returns the closest room to a given origin.
        """

        def closest_room_criteria(point):
            manhattan_distance = sum(abs(o - p) for o, p in zip(origin, point))
            return (manhattan_distance, point[0])

        return self.room_origins_to_room[min(self.room_origins_to_room, key=closest_room_criteria)]

    def remove_item(self, item_type, item_location):
        """
        Removes the item from the game
        """

        # Remove this item from the Tile
        self.get_tile(*item_location, False).current_item = None

        # Remove this item from item_locations
        del self.items[item_type][item_location]

    def to_json(self, as_json=True):
        """
        Creates a JSON representation of a level
        """
        json_dict = {
                "type": "level",
                "rooms": [r.to_json() for r in self.room_origins_to_room.values()],
                "hallways": [h.to_json() for h in self.hallways],
                "objects": self.json_item_locations}

        return json.dumps(json_dict) if as_json else json_dict

