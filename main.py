from common import *
from config import *
from process import *

with open('raw_data/keylog4.txt', 'r') as f:
    runs = split_runs(f.readlines())
    game_runs = [process_run(run) for run in runs]


if False:
    import turtle
    
    t = turtle.Turtle()
    t.tracer(False) # disable animation
    
    for run in game_runs:
        t.home()
        for i, level in enumerate(run['levels']):
            t.down()
            t.color(level_color(i)[:3])
            for move in level['events']:
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
        for i, level in enumerate(run['levels']):
            current_level_color = level_color(i)

            for move in level['events']:
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
    ax.set_axis_bgcolor('white')

    frame1 = plt.gca()
    plt.axis(frameon=False)
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    
    plt.tight_layout()
    plt.show()