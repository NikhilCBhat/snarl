import src.Game.constants as constants


def clear(func):
    """
    Decorator to clear the screen,
    before performing a view function
    """
    def clear_then_run(*args, **kwargs):
        print(constants.CLEAR_SCREEN)
        func(*args, **kwargs)
    return clear_then_run


def create_printable_list(list_of_item):
    """
    Creates a numbered list of items
    """
    return "\n".join("{}. {}".format(i, item)
                     for i, item in enumerate(list_of_item, 1))
