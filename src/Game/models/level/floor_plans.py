import src.Game.constants as constants
from src.Game.snarl_errors import FloorPlanOverlapError, InvalidDoorError, InvalidRoomError

class FloorPlan:
    """
    A FloorPlan is a collection of Tile objects.
    """
    def __init__(self, tiles, neighbors):
        self.tiles = tiles
        self.neighbors = neighbors

    @property
    def tiles(self):
        return self.__tiles

    @tiles.setter
    def tiles(self, tiles):
        """
        Setter for the tiles field.
        Note: This enforces that rooms/hallways don't overlap.
        """
        for tile in tiles:
            if tile.parent and tile.parent != self:
                raise FloorPlanOverlapError
            tile.parent = self

        self.__tiles = tiles

    def get_tile_representation(self, tile):
        """
        Gets the string representation for a given tile.
        """
        pass

    def to_json(self):
        """
        creates a JSON representation of the FloorPlan
        """
        pass

class Room(FloorPlan):
    """
    A Room is a collection of tiles.
    It has:
    - An upper-left Cartesian position,
    - Boundary dimensions (or size)
    - A layout of tiles
    - One or more doors.
    Objects, like the key and the exit, may be inside of a room.
    """

    def __init__(self, origin, width, height, doors, tiles=[]):
        super().__init__(tiles, [])
        self.origin = origin
        self.width = width
        self.height = height
        self.doors = {tile.location for tile in self.tiles if tile.is_door} | set(doors)
        self.__room_layout = None

    @property
    def doors(self):
        return self.__doors

    @doors.setter
    def doors(self, doors):
        tile_locations = {t.location for t in self.tiles}

        # Enforces that doors are within the room
        if any(door not in tile_locations for door in doors):
            raise InvalidDoorError

        # Enforces that doors are at the
        # boundary dimensions of the room
        for tile in self.tiles:
            if tile.location in doors:
                if not tile.is_wall:
                    raise InvalidDoorError
                tile.is_wall = False
                tile.is_door = True

        # Enforces that there is at least 1 door
        if not len(doors):
            raise InvalidRoomError

        self.__doors = doors

    @property
    def layout(self):
        if self.__room_layout:
            return self.__room_layout

        room_layout = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for tile in self.tiles:
            j, i = tile.location
            oj, oi = self.origin
            room_layout[i-oi][j-oj] = tile.get_numerical_representation()

        self.__room_layout = room_layout
        return room_layout

    def get_tile_representation(self, tile):
        if tile.is_door:
            return constants.DOOR_STRING
        return constants.WALL_STRING if tile.is_wall else constants.WALKABLE_STRING

    def place_occupant(self, occupant):
        """
        Places an occupant in the first empty tile.
        """
        for tile in self.tiles:
            if str(tile) == constants.WALKABLE_STRING:
                occupant.move(tile)
                return True
        return False

    def __str__(self):
        return constants.ROOM_NAME

    def to_json(self):
        return {"type" : "room", "origin" : self.origin[::-1],
                "bounds" : {"rows": self.height, "columns": self.width},
                "layout" : self.layout}

class Hallway(FloorPlan):
    """
    A Hallway is a collection of tiles.
    It has:
    - A list of waypoints.
    A hallway is valid if a line comprised of the waypoints connects the two rooms.
    """
    def __init__(self, tiles=[], waypoints=[], endpoints=[]):
        super().__init__(tiles, [])
        self.waypoints = waypoints
        self.endpoints = [endpoint.location for endpoint in endpoints]
        self.__add_neighbors(endpoints)

    def __add_neighbors(self, endpoints):
        """
        Updates the neighbors of the hallway & the rooms it connects.
        """
        source_room, dest_room = [t.parent for t in endpoints]
        source_room.neighbors.append(dest_room.origin)
        dest_room.neighbors.append(source_room.origin)
        self.neighbors.extend([source_room.origin, dest_room.origin])

    def get_tile_representation(self, tile):
        return constants.HALLWAY_STRING

    def __str__(self):
        return constants.HALLWAY_NAME

    def to_json(self):
        from_point, to_point = [x[::-1] for x in self.endpoints]

        return {"type" : "hallway",
                "from": from_point,
                "to": to_point,
                "waypoints": [x[::-1] for x in self.waypoints]
            }
