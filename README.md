# Sketchy Keylogger

Plotting keyboard input of [Spelunky][] gameplay for fun and profit.


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

[spelunky]: http://www.spelunkyworld.com