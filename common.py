import math

def get_area(level):
    """Get the section of the game a current level is in."""
    if i >= 15:
        return 4
    return int(math.floor(level / 4.0))

def action_color(key):
    return COLORS[key]

def level_color(level):
    return LEVEL_COLORS[get_area(level)]


def get_x(keys):
    if LEFT in keys and RIGHT in keys:
        return 0
    elif LEFT in keys:
        return -1
    elif RIGHT in keys:
        return 1
    else:
        return 0

def get_y(keys):
    if UP in keys and DOWN in keys:
        return 0
    elif DOWN in keys:
        return -1
    elif UP in keys:
        return 1
    else:
        return 0