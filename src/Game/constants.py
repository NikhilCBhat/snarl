## Communicaton Constants

# Message Types
WELCOME_MESSAGE = "welcome"
UPDATE_MESSAGE = "player-update"
MOVE_MESSAGE = "move"
END_LEVEL_MESSAGE = "end-level"
END_GAME_MESSAGE = "end-game"
PLAYER_SCORE_MESSAGE = "player-score"
START_LEVEL_MESSAGE = "start-level"
NAME_MESSAGE = "name"
ADVERSARY_UPDATE_MESSAGE = "adversary-update"
ADVERSARY_TYPE_MESSAGE = "adversary-type"
ADVERSARY_LEVEL_MESSAGE = "adversary-level"

## View Constants

# Representation Strings
WALL_STRING = "W"
DOOR_STRING = "D"
HALLWAY_STRING = "-"
VOID_STRING = "."
PLAYER_STRING = "P"
ADVERSARY_STRING = "A"
WALKABLE_STRING = " "
KEY_STRING = "K"
EXIT_STRING = "E"
GHOST_STRING = "G"
ZOMBIE_STRING = "Z"

# Tiles to colors
tiles_to_colors = {
    WALL_STRING: (132, 132, 130),
    DOOR_STRING: (254, 111, 94),
    VOID_STRING: (59, 68, 75),
    HALLWAY_STRING: (193, 154, 107),
    PLAYER_STRING: (23, 114, 69),
    ADVERSARY_STRING: (169, 32, 62),
    KEY_STRING: (242, 133, 0),
    EXIT_STRING: (153, 85, 187),
    GHOST_STRING: (140, 190, 214),
    ZOMBIE_STRING: (164, 0, 0)
}

# Clear Screen
CLEAR_SCREEN = "\033c\033[3J"

## Values for JSON formatting

# Representation Numbers
WALL_NUMBER = 0
WALKABLE_NUMBER = 1
DOOR_NUMBER = 2

# Room & Hallway Names
ROOM_NAME = "room"
HALLWAY_NAME = "hallway"

# Item Names
KEY_NAME = "key"
EXIT_NAME = "exit"

## Values for Occupant Parameters

# Occupant Types
OBSERVER_TYPE = "observer"
PLAYER_ACTOR_TYPE = "player"
GHOST_ACTOR_TYPE = "ghost"
ZOMBIE_ACTOR_TYPE = "zombie"

# Occupant Strengths
PLAYER_HIT_STRENGTH = 15
GHOST_HIT_STRENGTH = 5
ZOMBIE_HIT_STRENGTH = 10

# Occupant Starting Health
PLAYER_HEALTH = 50
GHOST_HEALTH = 30
ZOMBIE_HEALTH = 55

# Occupant Movement
PLAYER_MOVE_DISTANCE = 2
PLAYER_VISIBLE_DISTANCE = 2
ADVERSARY_MOVE_DISTANCE = 1

# Result Types
OK_RESULT = "OK" # meaning “the move was valid, nothing happened”
UNLOCKED_RESULT = "Key" # meaning “the move was valid, player collected the key”
EXITED_RESULT = "Exit" # meaning “the move was valid, player exited”
EJECTED_RESULT = "Eject" #  meaning “the move was valid, player was ejected”
INVALID_RESULT = "Invalid" # meaning “the move was invalid”

# Strategy Names
STAY_IN_PLACE_STRATEGY = "in place"

## Misc Constants

# State validity
MIN_PLAYERS = 1
MAX_PLAYERS = 4

# Misc Mappings
NAME_TO_STRING = {
    KEY_NAME: KEY_STRING, EXIT_NAME: EXIT_STRING,
    PLAYER_ACTOR_TYPE: PLAYER_STRING, ZOMBIE_ACTOR_TYPE: ZOMBIE_STRING, GHOST_ACTOR_TYPE: GHOST_STRING
}

NUMBER_TO_LETTER = {
    WALL_NUMBER: WALL_STRING,
    WALKABLE_NUMBER: WALKABLE_STRING,
    DOOR_NUMBER: DOOR_STRING
}