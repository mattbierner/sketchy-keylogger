# Draw each individual level in an given area
import argparse
import turtle
from common import *
from config import *
from process import *
from turtle_common import *

screen_width = 800
screen_height = 800
padding = 20
zoom = 1

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Data file path.')
parser.add_argument('--raw', action='store_true', default=False,
    help='Load a raw file instead of json?')

parser.add_argument('--animate', action='store_true', help='Use animation?')
parser.add_argument('--axis', action='store_true', help='Draw axis?')
parser.add_argument('--area', type=int, default=0, help='Which area to draw.')

args = parser.parse_args()

game_runs = load_raw_run(args.file) if args.raw else load_run(args.file)
area = args.area

# Compute the bounds
max_x = 1
max_y = 1

for run in game_runs:
    for level in run['levels']:
        if level['area'] != area:
            continue
        pos = (0, 0)
        for move in level['events']:
            if not move.get('action', False):
                keys = move['keys']
                mul = move['duration']
                dx = get_x(keys) * mul
                dy = get_y(keys) * mul
                end = (pos[0] + dx, pos[1] + dy)
                max_x = max(max_x, abs(end[0]))
                max_y = max(max_y, abs(end[1]))
                pos = end

x_scale = (screen_width / 2.0 - padding) / max_x
y_scale = (screen_width / 2.0 - padding) / max_y
scale = min(x_scale, y_scale) * zoom


# Start drawing
turtle.setup(width = screen_width, height = screen_height)

t = turtle.Turtle()

if not args.animate:
    t.tracer(False) # disable animation
    
if args.axis:
    t.color(0.5, 0.5, 0.5)
    draw_axis(t, screen_width, screen_height)

for run in game_runs:
    levels = run['levels']
    for i, level in enumerate(levels):
        if level['area'] != area:
            continue
        t.home()
        t.down()
        t.color(level_color(i)[:3])
        for move in level['events']:
            if move.get('action', False):
                key = move['key']
                t.dot(4, action_color(key)[:3])
            else:
                keys = move['keys']
                t.width(2 if SHIFT in keys else 1)
                mul = move['duration'] * scale
                x = get_x(keys) * mul
                y = get_y(keys) * mul
                t.setpos(x + t.xcor(), y + t.ycor())
        t.up()
        
        # draw death / end of game differently from advance level
        if i == len(levels) - 1:
            t.color(0, 0, 0)
        
        t.stamp()

turtle.done()
