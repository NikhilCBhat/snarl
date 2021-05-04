class FloorPlanOverlapError(Exception):
    """
    Thrown when hallways or rooms overlap.
    """
    pass

class InvalidDoorError(Exception):
    """
    Thrown when a door is not at the boundary dimensions of a room
    """
    pass

class InvalidHallwayError(Exception):
    """
    Thrown when a hallway is invalid. i.e:
    - not bounded by doors or
    - not made up of vertical/horizontal segments
    """
    pass

class InvalidRoomError(Exception):
    """
    Thrown when a room does not have a door
    """
    pass

class InvalidOccupantIdError(Exception):
    """
    Thrown when an occupant ID does not exist in the game.
    """
    pass

class InvalidDestinationError(Exception):
    """
    Thrown when the destination is not valid.
    """
    pass

class InvalidLevelCountError(Exception):
    """
    Thrown when there is not at least one level.
    """
    pass

class InvalidCurrentLevelError(Exception):
    """
    Thrown when current level is invalid.
    """
    pass

class InvalidPlayerCountError(Exception):
    """
    Thrown when the player number is under the minimum
    or over the maximum.
    """
    pass

class GameAlreadyOverError(Exception):
    """
    Thrown when a move is attempted after a game has ended.
    """
    pass

class OccupantMismatchError(Exception):
    """
    Thrown when occupant id list does not match keys for occupant dictionary.
    """
    pass

class NonTraversableTileError(Exception):
    """
    Thrown when an occupant moves onto a non-traversable tile.
    """
    pass

class InvalidOccupantTurnOrder(Exception):
    """
    Thrown when a move is made out of order.
    """
    pass

class PlayerOutofMovesError(Exception):
    """
    Thrown when a player has no more moves.
    """
    pass

class MissingUserInputError(Exception):
    """
    Thrown when a user does not provide any input.
    """
    pass