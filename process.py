# Spelunky keylog processing
import datetime
import json
import re
from time import mktime
from config import *

def process_line(line):
    """Parse a single line in the keylog."""
    match = re.match('(.+?)\s+(UP|DOWN)\s+(\d+)', line)
    date = None
    try:
        date = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
    except:
        date = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
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
    """Convert raw key up and key downs into actions and movements."""
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
                            'start': start,
                            'end': end,
                            'duration': end - start,
                            'keys': list(state)
                        })
                    state.remove(code)
                elif not command['up'] and not code in state:
                    if len(state):
                        level.append({
                            'start': start,
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
    
    return {
        'levels': levels
    }

def default_json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return int(mktime(obj.timetuple()))
    elif isinstance(obj, datetime.timedelta):
        return float(obj.total_seconds())
    else:
        return json.JSONEncoder().default(obj)


if __name__ == "__main__":
    # Simple command line usage to convert raw key logs to json.
    import argparse        
    
    parser = argparse.ArgumentParser(description='Convert raw keylog to json.')
    parser.add_argument('in_file', help='Raw input data file to process.')
    parser.add_argument('out_file', help='File to write json results to.')
    
    args = parser.parse_args()
    
    with open(args.in_file, 'r') as f:
        runs = split_runs(f.readlines())
        game_runs = [process_run(run) for run in runs]
    
    with open(args.out_file, 'w') as outfile:
        json.dump(game_runs, outfile, indent = 4,
            default = default_json_serializer)
    
