from datetime import datetime
import math
import re
from config import *

# Style
COLORS = {
    JUMP: (1, 0, 0, 0.5),
    WHIP: (0, 1, 0, 0.5),
    BOMB: (0, 0, 1, 0.5),
    ROPE: (1, 1, 0, 0.5),
    USE: (1, 0, 1, 0.5),
    BUY: (0, 1, 1, 0.5),
}

LEVEL_COLORS = [
    (0, 0, 0, 0.5), # Mine
    (0, 1, 0, 0.5), # Jungle
    (0, 0, 1, 0.5), # Ice
    (1, 0, 0, 0.5), # Temple
    (1, 0, 1, 0.5), # Boss 
]

DEFAULT_COLOR = (0, 0, 0, 1)


def get_area(level):
    """Get the section of the game a current level is in."""
    if i >= 15:
        return 4
    return int(math.floor(level / 4.0))

def action_color(key):
    return COLORS.get(key, DEFAULT_COLOR)

def level_color(level):
    return LEVEL_COLORS[get_area(level)]


def process_line(line):
    """Parse a single line in the keylog."""
    match = re.match('(.+?)\s+(UP|DOWN)\s+(\d+)', line)
    date = None
    try:
        date = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
    except:
        date = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
    return {
        'date': date,
        'up': match.group(2) == 'UP',
        'code': int(match.group(3))
    }

def split_runs(data):
    """Split a keylog into individual runs."""
    in_group = False
    buckets = []
    bucket = []
    for line in data:
        line = process_line(line)
        code = line['code']
        if code == END:
            in_group = False
            buckets.append(bucket)
            bucket = []
        elif code == START:
            in_group = True
        else:
            if code in GAME_KEYS or code == LEVEL:
                if in_group:
                    bucket.append(line)
    
    buckets.append(bucket)
    return [split_levels(x) for x in buckets if len(x) > 5]

def split_levels(data):
    """Split raw run data into levels."""
    levels = []
    level = []
    for line in data:
        code = line['code']
        if code == LEVEL:
            levels.append(level)
            level = []
        else:
            if code in GAME_KEYS:
                level.append(line)
    
    levels.append(level)
    return [x for x in levels if len(x) > 5]

def process_run(raw_levels):
    """ """
    levels = []
    for raw_level in raw_levels:
        level = []
        start = raw_level[0]['date']
        state = []
        for command in raw_level:
            code = command['code']
            end = command['date']
            if code in ACTIONS:
                if command['up'] == False:
                    level.append({
                        'action': True,
                        'end': end,
                        'key': code
                    })
            elif code in MOVEMENTS:
                if command['up'] and code in state:
                    if len(state):
                        level.append({
                            'state': start,
                            'end': end,
                            'duration': end - start,
                            'keys': list(state)
                        })
                    state.remove(code)
                elif not command['up'] and not code in state:
                    if len(state):
                        level.append({
                            'state': start,
                            'end': end,
                            'duration': end - start,
                            'keys': list(state)
                        })
                    state.append(code)   
                start = end
        levels.append(level)
    
    # Remove initial actions before movement (pressed to skip transition)
    for level in levels:
        while len(level) > 0 and level[0].get('action', False):
            del level[0]

    print (len(levels), [len(x) for x in levels])
    return levels            


with open('raw_data/keylog4.txt', 'r') as f:
    runs = split_runs(f.readlines())
    game_runs = [process_run(run) for run in runs]



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

if True:
    import turtle
    
    t = turtle.Turtle()
    t.tracer(False) # disable animation
    
    for run in game_runs:
        t.home()
        for i, level in enumerate(run):
            t.down()
            t.color(level_color(i)[:3])
            for move in level:
                if move.get('action', False):
                    key = move['key']
                    t.dot(None, action_color(key)[:3])
                else:
                    keys = move['keys']
                    duration = move['duration']
                    t.width(2 if SHIFT in keys else 1)
                    mul = duration.total_seconds() * 20
                    x = get_x(keys) * mul
                    y = get_y(keys) * mul
                    t.setpos(x + t.xcor(), y + t.ycor())
            t.up()

        t.stamp()
    turtle.done()
    
else:
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D                        
    from matplotlib import collections  as mc
    
    fig, ax = plt.subplots()
    
    for run in game_runs:
        pos = [0, 0]
        dotsx = []
        dotsy = []
        lines = []
        widths = []
        movement_colors = []
        action_colors = []
        for i, level in enumerate(run):
            current_level_color = level_color(i)

            for move in level:
                if move.get('action', False):
                    key = move['key']
                    dotsx.append(pos[0])
                    dotsy.append(pos[1])
                    action_colors.append(action_color(key))
                else:
                    keys = move['keys']
                    duration = move['duration']
                    widths.append(2 if SHIFT in keys else 1)
                    movement_colors.append(current_level_color)
                    mul = duration.total_seconds()
                    x = get_x(keys) * mul
                    y = get_y(keys) * mul
                    new_pos = [pos[0] + x, pos[1] + y]
                    lines.append([pos, new_pos])
                    pos = new_pos
    
        lc = mc.LineCollection(lines, color=movement_colors, linewidths=widths)
        ax.add_collection(lc)
        plt.scatter(dotsx, dotsy, color=action_colors, s=20.0)

    ax.autoscale()
    plt.axis('equal')

    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)

    plt.show()