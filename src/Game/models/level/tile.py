import src.Game.constants as constants

class Tile:
    """
    A Tile is a single block in the game.
    It has a:
    - Parent Hallway/Room that it belongs to
    - Collection of Items
    - Collection of occupants
    - X & Y location
    """

    def __init__(self, x, y):
        self.parent = None
        self.current_item = None
        self.is_wall = False
        self.is_door = False
        self.current_occupant = None
        self.location = (x,y)

    def __str__(self):
        if self.current_occupant:
            return str(self.current_occupant)

        if self.current_item:
            return str(self.current_item)

        return self.parent.get_tile_representation(self) if self.parent else constants.VOID_STRING

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.location == other.location
        return False

    def get_adjacent_rooms(self):
        """
        Gets the rooms adjacent to a tile
        """
        return self.parent.neighbors if self.parent else set()

    def get_numerical_representation(self):
        """
        Gets the numerical representation of the tile
        for the layout JSON
        """
        if self.is_door:
            return constants.DOOR_NUMBER

        if self.is_wall or not self.parent:
            return constants.WALL_NUMBER

        return constants.WALKABLE_NUMBER