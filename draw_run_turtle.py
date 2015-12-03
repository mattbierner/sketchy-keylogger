# Draw a full run using turtles
import argparse
import turtle
from common import *
from config import *
from process import *

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Data file path.')
parser.add_argument('--raw', action='store_true',
    help='Load a raw file instead of json?')

parser.add_argument('--animate', action='store_true',
    help='Use animation?')

args = parser.parse_args()

game_runs = load_raw_run(args.file)


# Start drawing
t = turtle.Turtle()

if not args.animate:
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
