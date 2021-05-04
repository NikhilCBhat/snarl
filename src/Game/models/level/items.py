import src.Game.constants as constants

class Item:
    """
    An Item is an interactable object in the game.
    """

    def __init__(self, ascii_representation, item_name):
        self.ascii_representation = ascii_representation
        self.item_name = item_name

    def __str__(self):
        return self.ascii_representation

class Key(Item):
    """
    A Key is an item type that allows the user to unlock the exit.
    """

    def __init__(self):
        super().__init__(constants.KEY_STRING, constants.KEY_NAME)

class Exit(Item):
    """
    An Exit is an item that that allows the user to leave the level.
    """

    def __init__(self):
        super().__init__(constants.EXIT_STRING, constants.EXIT_NAME)

item_name_to_object = {constants.KEY_NAME: Key,
                        constants.EXIT_NAME: Exit}