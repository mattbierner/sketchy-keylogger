import math
from config import *

def get_area(level):
    """Get the section of the game a current level is in."""
    if level >= 15:
        return 4
    return int(math.floor(level / 4.0))

def action_color(key):
    return COLORS[key]

def level_color(level):
    return LEVEL_COLORS[get_area(level)]


def get_x(keys):
    diag = UP in keys or DOWN in keys
    if LEFT in keys and RIGHT in keys:
        return 0
    elif LEFT in keys:
        return -0.707 if diag else -1
    elif RIGHT in keys:
        return 0.707 if diag in keys else 1
    else:
        return 0

def get_y(keys):
    diag = LEFT in keys or RIGHT in keys
    if UP in keys and DOWN in keys:
        return 0
    elif DOWN in keys:
        return -0.707 if diag else -1
    elif UP in keys:
        return 0.707 if diag in keys else 1
    else:
        return 0