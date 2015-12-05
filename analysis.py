# Super hacky scripts used to analyse some basic Spelunky data.
# Plenty of copy+paste and all the good stuff.

import argparse
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

args = parser.parse_args()

game_runs = load_raw_run(args.file) if args.raw else load_run(args.file)


def is_death_level(i, levels):
    return i != 15 and i == len(levels) - 1

def no_deaths(levels):
    """Filter out level plays where the player died."""
    for i, level in enumerate(levels):
        if is_death_level(i, levels):
            continue
        yield (i, level)

def keycode_to_name(code):
    if code == SPRINT:
        return 'sprint'
    if code == UP:
        return 'up'
    if code == DOWN:
        return 'down'
    if code == LEFT:
        return 'left'
    if code == RIGHT:
        return 'right'
    if code == JUMP:
        return 'jump'
    if code == BOMB:
        return 'bomb'
    if code == WHIP:
        return 'whip'
    if code == USE:
        return 'use'
    if code == BUY:
        return 'buy'
    if code == ROPE:
        return 'rope'
    return str(code)

def print_key_code_pair(k, v, format = "%s: %s"):
    print(format % (keycode_to_name(k), v))

def print_key_map(map, line = "%s: %s"):
    for k, v in map.iteritems():
        print_key_code_pair(k, v, format=line)

def process_run_data(raw_levels):
    levels = []
    for i, raw_level in enumerate(raw_levels):
        level = []
        state = {}
        for command in raw_level:
            code = command['code']
            end = command['date']
            if command['up'] and code in state:
                start = state[code]
                del state[code]
                level.append({
                    'start': end,
                    'end': end,
                    'duration': end - start,
                    'key': code
                })
            elif not command['up'] and not code in state:
                state[code] = end
        
        levels.append({
            'area': get_area(i),
            'start': level[0]['start'],
            'end': level[-1]['end'],
            'duration': level[-1]['end'] - level[0]['start'],
            'events': level
        })
    
    # Remove initial actions before movement (pressed to skip transition)
    for level in levels:
        events = level['events']
        while len(events) > 0 and events[0]['key'] in ACTIONS:
            del events[0]
    
    return {
        'start': levels[0]['start'],
        'end': levels[-1]['end'],
        'duration': levels[-1]['end'] - levels[0]['start'],
        'levels': levels
    }
    

def load_raw_run_data(path):
    with open(path, 'r') as f:
        runs = split_runs(f.readlines())
    return [process_run_data(run) for run in runs]

# Build a list of just keypresses
all_run_data = load_raw_run_data('raw_data/combined.txt')

if True:
    print("\nAvg duration of movement keypresses:")
    counts = {}
    total_times = {}
    
    for run in all_run_data:
        levels = run['levels']
        for i, level in enumerate(levels):
            for evt in level['events']:
                key = evt['key']
                if not key in MOVEMENTS:
                    continue
                if not key in counts:
                    counts[key] = 0
                    total_times[key] = 0
                counts[key] += 1
                total_times[key] += evt['duration'].total_seconds()

    avgs = {}

    for key, sum in total_times.iteritems():
        avgs[key] = float(sum) / counts[key]
    
    print("counts")
    print_key_map(counts)
    print('\navgs')
    print_key_map(avgs)

if True:
    print("\nAvg duration of movement keypresses per area:")
    counts = [{}, {}, {}, {}, {}]
    total_times = [{}, {}, {}, {}, {}]
    
    for run in all_run_data:
        levels = run['levels']
        for i, level in enumerate(levels):
            area = get_area(i)
            for evt in level['events']:
                key = evt['key']
                if not key in MOVEMENTS:
                    continue
                if not key in counts[area]:
                    counts[area][key] = 0
                    total_times[area][key] = 0
                counts[area][key] += 1
                total_times[area][key] += evt['duration'].total_seconds()

    for area, keys in enumerate(total_times):
        avgs = {}
        for key, sum in keys.iteritems():
            avgs[key] = float(sum) / counts[area][key]
    
        print(area)
        print_key_map(avgs)
        print("")


if False:
    print("\nDeath duration data")
    
    target_area = 2
    
    for run in all_run_data:
        levels = run['levels']
        for i, level in enumerate(levels):
            area = get_area(i)
            #if area != target_area:
            #    continue
            if not is_death_level(i, levels):
                continue
            print("%s, %s" % (area, level['duration'].total_seconds()))
            
if True:
    print("\nAvg actions per area (no death):")
    counts = [0] * 5
    moves = [0] * 5

    for run in game_runs:
        levels = run['levels']
        for i, level in no_deaths(levels):
            area = level['area']
            counts[area] += 1 
            moves[area] += len([x for x in level['events'] if 'action' in x and x['key']== ROPE])

    for i, sum in enumerate(moves):
         print("%s: %s" % (i, float(sum) / counts[i]))

if True:
    print("\nEvents per level:")
    counts = {}
    moves = {}

    for run in game_runs:
        levels = run['levels']
        for i, level in no_deaths(levels):
            area = level['area']
            counts[area] = counts.get(area, 0) + 1
            moves[area] = moves.get(area, 0) + len([x for x in level['events']])

    for i, sum in moves.iteritems():
        print("%s: %s" % (i, float(sum) / counts[i]))

if False:
    print("\nMin events per level:")
    min_run = 0
    min_level = 0
    min_x = 100;
    for r, run in enumerate(game_runs):
        levels = run['levels']
        for i, level in no_deaths(levels):
            if len(level['events']) < min_x:
                min_x = len(level['events'])
                min_run = r
                min_level = i
           
    print (min_run, min_level, min_x)
    print len(game_runs[min_run]['levels'][min_level]['events'])

if True:
    print("\nShortest run:")
    min_run = 0
    min_x = 100000;
    for r, run in enumerate(game_runs):
        if run['duration'] < min_x:
            min_x = run['duration'] 
            min_run = r
           
    print(min_run, min_x)
    
if True:
    print("\nLongest run:")
    min_run = 0
    max_x = 0;
    for r, run in enumerate(game_runs):
        if run['duration'] > max_x:
            max_x = run['duration'] 
            min_run = r
           
    print(min_run, max_x)

if True:
    print("\nAvg moves per area (no death)")
    counts = [0] * 5
    moves = [{}] * 5

    for run in game_runs:
        levels = run['levels']
        for i, level in no_deaths(levels):
            area = level['area']
            counts[area] += 1
            for event in level['events']:
                if 'keys' in event:
                    for key in event['keys']:
                        moves[area][key] = moves[area].get(key, 0) + 1

    for i, move in enumerate(moves):
        print("%s:" %i)
        for key, count in move.iteritems():
            print_key_code_pair(key, float(count) / counts[i])



if True:
    print("\nAvg time per area (no death):")
    counts = [0] * 5
    dur = [0] * 5

    for run in game_runs:
        levels = run['levels']
        for i, level in no_deaths(levels):
            area = level['area']
            counts[area] +=  1
            dur[area] += level['duration']

    out_moves = {}
    for i, sum in enumerate(dur):
        out_moves[i] = float(sum) / counts[i]

    print_key_map(out_moves)
    

if True:
    print("\nAvg time per level (no death):")
    counts = [0] * 16
    dur = [0] * 16

    for run in game_runs:
        levels = run['levels']
        for i, level in no_deaths(levels):
            counts[i] += 1
            dur[i] += level['duration']

    out_moves = {}
    for i, sum in enumerate(dur):
        out_moves[i] = float(sum) / counts[i]

    print("\n".join("%s, %s" %(k, v) for k, v in out_moves.iteritems()))