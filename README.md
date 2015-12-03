# Sketchy Keylogger

Plotting keyboard input of [Spelunky][] gameplay for fun and profit.

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/matplot-run.png" alt="turtle" />
</div>


## Gameplay Logging
Keylogger record the following in game actions (targeting Spelunky classic):

* Arrow Keys = Movement
* Shift = Sprint
* Z = Jump
* X = Whip
* A = Bomb
* S = Rope
* C = Use
* P = Buy

The following keys are used within the key log itself to understand where runs and levels start and end:

* T = Start new game (press at least twice in a row)
* I = End current game (press at least twice in a row)
* K = Advance one level


## Scripts

#### `keylogger.py`
Super simple Python2.7 keylogger for windows. Records all key up and key down data while running and writes this data to a file.

Requires [pywin32](http://sourceforge.net/projects/pywin32/) and [pyhook](http://sourceforge.net/projects/pyhook/).


#### `process.py`
Convert keylog to json for processing.

```sh
$ python process.py in/file/keylog.txt --out out/file.json
```

You can also combine multiple files.

```sh
$ python process.py in/file/keylog1.txt in/file/keylog2.txt --out out/file.json
```

#### `draw_run_turtle.py`
Draw a complete set of runs using the [Python turtle module][turtle]. Resets drawing to (0, 0) after each death.

```sh
$ python draw_run_turtle.py runs/spelunky1.json
```

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/turtle-run.png" alt="turtle" />
</div>


By default, does not animate drawing. Use `--animate` to watch turtle draw.

```sh
$ python draw_run_turtle.py --animate runs/spelunky1.json
```

#### `draw_run_matplot.py`
Draw a complete set of runs using the [Python turtle module][turtle]. Resets drawing to (0, 0) after each death.

```sh
$ python draw_run_matplot.py runs/spelunky1.json
```

<div align="center" >
    <img src="https://raw.githubusercontent.com/mattbierner/sketchy-keylogger/master/documentation/matplot-run.png" alt="turtle" />
</div>

Produced plot should be interactive unlike the turtle one, but animation is not supported.



[turtle]: https://docs.python.org/2/library/turtle.html
[spelunky]: http://www.spelunkyworld.com