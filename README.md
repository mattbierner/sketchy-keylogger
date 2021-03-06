# Sketchy Keylogger

Plotting keyboard input of [Spelunky][] gameplay for fun and profit.

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/matplot-run.png" alt="turtle" />
</div>


## Overview
Player keyboard input is recorded during a game of Spelunky and then reconstructed into an abstract drawing. Player movement with the arrow keys moves the pencil around the canvas, while actions, such as using a bomb, are drawn as little circles on the movement paths. 

### Movement
Player movement with the arrow keys is used for drawing. Moving left with the left arrow draws a line to the left, while holding both the up and right arrows draws a diagonal line towards the upper right. The length of the line is determined by how long the key was pressed.

Movements lines are colored based on game level:
 
* Mines - tan
* Jungle - green
* Ice - blue
* Temple - orange
* Boss - red

Sprinting draws a line that is twice as thick as normal movement.

### Actions
Actions are plotted individually as little dots:

* Z = Jump - Gray
* X = Whip - Light brown
* A = Bomb - Red
* S = Rope - Dark brown
* C = Use - Black
* P = Buy - Gold

### Meta Keys
The following keys are used within the key log itself to understand where runs and levels start and end:

* T = Start new game (press at least twice in a row)
* I = End current game (press at least twice in a row)
* K = Advance one level

For example, a run where you make it to the third level before dying would look like this (let `~` be any number of game inputs):

```
ttttt~~k~~k~~iiiii
```

Anything before `tt` or after `ii` is ignored.

Level durations are taken from first movement key to last key press before `k`. This allows you to press the `X` key to skip the tunnel transition (just don't press any arrow keys to skip).


## Scripts

### `keylogger.py`
Super simple Python2.7 keylogger for windows. Records all key up and key down data while running and writes this data to a file.

Requires [pywin32](http://sourceforge.net/projects/pywin32/) and [pyhook](http://sourceforge.net/projects/pyhook/).


### `process.py`
Convert keylog to json for processing.

```sh
$ python process.py in/file/keylog.txt --out out/file.json
```

You can also combine multiple files.

```sh
$ python process.py in/file/keylog1.txt in/file/keylog2.txt --out out/file.json
```

### `draw_run_turtle.py DATA_FILE`
Draw a complete set of runs using the [Python turtle module][turtle]. Resets drawing to (0, 0) after each death.

* `DATA_FILE` - File to draw.
* `--axis` - Draw axis.
* `--raw` - Load and process raw keylog data instead of json. 
* `--animate` - By default, does not animate drawing. Use `--animate` to watch turtle draw.

```sh
$ python draw_run_turtle.py runs/spelunky-combined.json
```

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/turtle-run.png" alt="turtle" />
</div>


### `draw_run_matplot.py DATA_FILE`
Draw a complete set of runs using the [Python turtle module][turtle]. Resets drawing to (0, 0) after each death.

* `DATA_FILE` - File to draw.
* `--axis` - Draw axis.
* `--raw` - Load and process raw keylog data instead of json. 

```sh
$ python draw_run_matplot.py runs/spelunky-combined.json
```

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/matplot-run.png" alt="turtle" />
</div>

Produced plot should be interactive unlike the turtle one, but animation is not supported.

### `draw_area_turtle.py DATA_FILE --area AREA`
Draw all level runs in a given area using the [Python turtle module][turtle]. Resets drawing to (0, 0) after each level.

* `DATA_FILE` - File to draw.
* `--area AREA` - Which area of the game to draw (mines, jungle, ...). Zero indexed.
* `--axis` - Draw axis.
* `--raw` - Load and process raw keylog data instead of json. 
* `--animate` - By default, does not animate drawing. Use `--animate` to watch turtle draw.


```sh
$ python draw_area_turtle.py runs/spelunky-combined.json --area 2 --axis
```

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/turtle-area2.png" alt="turtle" />
</div>



[turtle]: https://docs.python.org/2/library/turtle.html
[spelunky]: http://www.spelunkyworld.com