import argparse
import matplotlib.pyplot as plt
from matplotlib import collections as mc

from common import *
from config import *
from process import *

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Data file path.')
parser.add_argument('--raw', action='store_true', default=False,
    help='Load a raw file instead of json?')
   
parser.add_argument('--axis', action='store_true', help='Draw axis?')
 
args = parser.parse_args()

game_runs = load_raw_run(args.file) if args.raw else load_run(args.file)

# Plot run
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
                widths.append(2 if SHIFT in keys else 1)
                movement_colors.append(current_level_color)
                mul = move['duration']
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

if args.axis:
    plt.axhline(0, color=(0.5, 0.5, 0.5))
    plt.axvline(0, color=(0.5, 0.5, 0.5))

plt.tight_layout()
plt.show()